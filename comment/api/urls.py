from django.urls import path

from . import views

app_name = 'comment'

urlpatterns = [
    path('create/', views.CommentCreateAPIView.as_view(), name='create'),
    # path('detail/<slug>', views.PostDetailAPIView.as_view(), name='detail'),
]