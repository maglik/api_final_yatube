from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (PostViewSet, CommentViewSet,
                    FollowViewSet, GroupViewSet)

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comments')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register('groups', GroupViewSet, basename='group')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    # path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('v1/', include('djoser.urls.jwt')),
]
