from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title

from .serializers import (
    SignupSerializer,
    UserSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
)
from .pagination import CommentsPagination, ReviewsPagination, UserPagination
from .permissions import (
    AdminReadOnlyPermissions,
    AdminWriteOnlyPermissions,
    AdminReadOnlyPermissionsWithOutSuperuser,
    AdminOrReadOnly,
)
from .filters import TitleFilter

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        send_mail(
            '',
            user.confirmation_code,
            'admin@yamdb.blog',
            [email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if username is not None and confirmation_code is not None:
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            access_token = RefreshToken.for_user(user)
            response = {'token': str(access_token.access_token)}
            return Response(response, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer

    lookup_field = 'username'

    pagination_class = UserPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_permissions(self):
        if self.action in ('list', 'retrieve',):
            return (AdminReadOnlyPermissions(),)
        elif self.action in ('create', 'partial_update', 'destroy',):
            return (AdminWriteOnlyPermissions(),)
        elif self.action == 'update':
            raise PermissionDenied('Do not allow PUT request')
        return super().get_permissions()

    @action(methods=['GET', 'PATCH'], detail=False)
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('pk')
    serializer_class = CategorySerializer
    permission_classes = (AdminReadOnlyPermissionsWithOutSuperuser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('pk')
    serializer_class = GenreSerializer
    permission_classes = (AdminReadOnlyPermissionsWithOutSuperuser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='genre_slug'
    )
    def get_genre(self, request, slug):
        genre = self.get_object()
        serializer = GenreSerializer(genre)
        genre.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('pk')
    permission_classes = (AdminReadOnlyPermissionsWithOutSuperuser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = ReviewsPagination

    def get_permissions(self):
        if self.action == 'update':
            raise PermissionDenied('Do not allow PUT request')
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all().order_by('pk')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = CommentsPagination

    def get_permissions(self):
        if self.action == 'update':
            raise PermissionDenied('Do not allow PUT request')
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        return review.comments.all().order_by('pk')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
