from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView,
    RetrieveUpdateAPIView
)
from post.models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
#custom permission
from .permissions import isOwnerOrSuperUser

class PostListAPIView(ListAPIView):
    # queryset = Post.objects.all() # tumunu cekiyor
    serializer_class = PostSerializer
    
    #arama
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    # SearchFilter /api/post/list/?search=es
    # OrderingFilter /api/post/list/?search=es&ordering=title (ordering=-title : ters siralama | reverse orderings)

    # filtreleme
    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset
    #__note: once data filtrelenip gonderiliyor ve search yapildiginda bu filtre dikkate aliniyor
    


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
    permission_classes = [isOwnerOrSuperUser]

    def perform_update(self, serializer):
        serializer.save(modified_by_user=self.request.user)
        # update islemi yapan user'i eklemak icin


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, isOwnerOrSuperUser]


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
