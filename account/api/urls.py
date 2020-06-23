from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('profile/me/', views.ProfileAPIView.as_view(), name='me'),
    path('update-password/', views.UpdatePassword.as_view(), name='update-password'),
    path('register/', views.CreateUserView.as_view(), name='register')
]