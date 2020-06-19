from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('me/', views.ProfileAPIView.as_view(), name='me'),
]