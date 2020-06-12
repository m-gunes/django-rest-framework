from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from comment.models import Comment
from .serializers import CommentCreateSerializer

# Create your views here.
class CommentCreateAPIView(CreateAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentCreateSerializer