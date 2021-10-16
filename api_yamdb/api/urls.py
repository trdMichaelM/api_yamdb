from django.urls import path, include
from rest_framework import routers

from .views import signup, token, UserViewSet, ReviewViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'v1/users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token')
]
