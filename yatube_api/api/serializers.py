from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model


from posts.models import Comment, Post, Follow, Group


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post', 'created_at')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post_id = self.context['view'].kwargs.get('post_id')
        validated_data['post'] = Post.objects.get(id=post_id)
        return super().create(validated_data)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        required=False,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
