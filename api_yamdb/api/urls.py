from django.urls import path, include
from rest_framework import routers

from .views import signup, token, UserViewSet

router = routers.DefaultRouter()
router.register(r'v1/users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token')
]
