from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from comment.models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer
from .permissions import isOwner

# Create your views here.
class CommentCreateAPIView(CreateAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentCreateSerializer

   def perform_create(self, serializer):
      serializer.save(user=self.request.user) # comment'i atan user'i kayit ediyoruz. selectboxtan secilen user degil



class CommentListAPIView(ListAPIView):
   # queryset = Comment.objects.all()
   serializer_class = CommentListSerializer

   def get_queryset(self):
      return Comment.objects.filter(parent=None)


class CommentDeleteAPIView(DestroyAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentDeleteUpdateSerializer
   lookup_field = 'pk'
   permission_classes = [IsAuthenticated, isOwner]


class CommentUpdateAPIView(RetrieveUpdateAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentDeleteUpdateSerializer
   lookup_field = 'pk'
   permission_classes = [isOwner]
   