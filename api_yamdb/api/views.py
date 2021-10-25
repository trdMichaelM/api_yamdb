from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import status, viewsets, filters, mixins
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed 
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
    ReviewCreateSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
)
from .pagination import CommentsPagination, ReviewsPagination, UserPagination
from .permissions import (
    AdminReadOnlyPermissions,
    AdminWriteOnlyPermissions,
    IsOwnerPermission,
    IsAdminPermission,
    IsModeratorPermission,
    ReadOnlyOrAdminPermission
)
from .filters import TitleFilter

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if not User.objects.filter(**request.data).exists():
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    username = request.data.get('username')
    email = request.data.get('email')
    user = User.objects.get(username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        '',
        confirmation_code,
        settings.EMAIL_ADMIN,
        [email],
        fail_silently=False
    )
    response = {
        'email': email,
        'username': username
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if username is not None and confirmation_code is not None:
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            access_token = RefreshToken.for_user(user)
            response = {'token': str(access_token.access_token)}
            return Response(response, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # http_method_names = ['get', 'post', 'patch', 'delete']
    # тесты статус 405 не пропускают, требуют 403

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
        data = request.data.copy()
        if request.method == 'PATCH':
            if user.role == 'user' and 'role' in data:
                data['role'] = 'user'
            serializer = self.get_serializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ReadOnlyOrAdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ReadOnlyOrAdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (ReadOnlyOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerPermission | IsAdminPermission | IsModeratorPermission,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = ReviewsPagination
    ordering_fields = ('pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action == 'update':
            raise MethodNotAllowed('Do not allow PUT request')
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerPermission | IsAdminPermission | IsModeratorPermission,)
    pagination_class = CommentsPagination

    def get_permissions(self):
        if self.action == 'update':
            raise MethodNotAllowed('Do not allow PUT request')
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
