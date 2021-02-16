from django.contrib.auth import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    #Login Page
    path('', views.role, name='role'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/register.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('receive_list/', views.receive_list, name='receive_list'),
    ]