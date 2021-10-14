from django.urls import path, include
from rest_framework import routers

from .views import (
    signup,
    token,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

router = routers.DefaultRouter()
router.register(r'v1/users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token')
]
