from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from comment.models import Comment
from django.contrib.auth.models import User
from post.models import Post


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at']

    def validate(self, attrs):
        if attrs['parent']:
            if attrs['parent'].post != attrs['post']:
                raise serializers.ValidationError('something went wrong')
        return attrs



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']



class PostSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'user', 'username']
    
    def get_username(self, obj):
        return obj.user.username
        


class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
        # depth = 1 # ForeignKey li olan herseyin icin aciyor


    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many=True).data
            

class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']