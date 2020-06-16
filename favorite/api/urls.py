from django.urls import path

from . import views

app_name = 'favorite'

urlpatterns = [
    path('list-create/', views.FavoriteListCreateAPIView.as_view(), name='list-create'),
    path('test/<pk>', views.FavoriteAPIView.as_view(), name='test')
]