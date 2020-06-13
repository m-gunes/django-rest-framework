from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from comment.models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer
from .permissions import isOwner
from .paginations import CommentPagination

# Create your views here.
class CommentCreateAPIView(CreateAPIView):
   queryset = Comment.objects.all()
   serializer_class = CommentCreateSerializer

   def perform_create(self, serializer):
      serializer.save(user=self.request.user) # comment'i atan user'i kayit ediyoruz. selectboxtan secilen user degil



class CommentListAPIView(ListAPIView):
   # queryset = Comment.objects.all()
   serializer_class = CommentListSerializer
   pagination_class = CommentPagination


   def get_queryset(self):
      queryset = Comment.objects.filter(parent=None)
      query = self.request.GET.get('id')
      if query:
         # post'a yapilan yorumlari getiriyoruz
         # http://127.0.0.1:8000/api/comment/list/?id=10
         # id'si 10 olan post'un yorumlarini getir
         queryset = queryset.filter(post=query)
      return queryset
      
   
      


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
   