from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import routers

from api.views import UserViewSet
from api.views import ReviewViewSet, CommentViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]