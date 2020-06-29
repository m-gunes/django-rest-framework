from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'post'

urlpatterns = [
    path('list/', cache_page(60*1)(views.PostListAPIView.as_view()), name='list'),
    path('detail/<slug>', views.PostDetailAPIView.as_view(), name='detail'),
    path('update/<slug>', views.PostUpdateAPIView.as_view(), name='update'),
    path('delete/<slug>', views.PostDeleteAPIView.as_view(), name='delete'),
    path('create/', views.PostCreateAPIView.as_view(), name='create')
]