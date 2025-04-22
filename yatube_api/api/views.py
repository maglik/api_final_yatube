from rest_framework import viewsets, mixins, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Follow, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
)
from .permissions import OwnerOrReadOnly
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly,)

    def get_permissions(self):
        if self.action == "create":
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_permissions(self):
        if self.action == "create":
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()


class FollowViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
