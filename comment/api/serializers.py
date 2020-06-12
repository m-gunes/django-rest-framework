from rest_framework.serializers import ModelSerializer
from comment.models import Comment


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at']