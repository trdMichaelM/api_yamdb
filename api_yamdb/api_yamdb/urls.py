from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework import routers

from api.views import UserViewSet
from api.views import ReviewViewSet, CommentViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/', include(router.urls)),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
