from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status, viewsets, filters, exceptions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, UserSerializer
from .pagination import UserPagination
from .permissions import AdminReadOnlyPermissions, AdminWriteOnlyPermissions

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
        if self.action == 'list':
            return (AdminReadOnlyPermissions(),)
        elif self.action == 'create':
            return (AdminWriteOnlyPermissions(),)
        elif self.action == 'retrieve':
            return (AdminReadOnlyPermissions(),)
        elif self.action == 'partial_update':
            return (AdminWriteOnlyPermissions(),)
        elif self.action == 'destroy':
            return (AdminWriteOnlyPermissions(),)
        elif self.action == 'update':
            raise exceptions.PermissionDenied('Do not allow PUT request')
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
