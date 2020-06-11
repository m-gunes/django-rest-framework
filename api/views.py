from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView,
    RetrieveUpdateAPIView
)
from post.models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all() # ?- detail de neden .all() diyoruz?
    serializer_class = PostSerializer # ?- detail post serializer tanimlanabilir mi?
    lookup_field = 'slug'
    # lookup_field = 'pk'
    # note: lookup_field hic yazilmazsa default ta pk yani id ile calisiyor. url kismina detail/<pk> seklinde yazilmali


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(modified_by_user=self.request.user)
        # update islemi yapan user'i eklemak icin


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
