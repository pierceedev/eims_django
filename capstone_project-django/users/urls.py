from django.urls import path
from django.shortcuts import redirect
from . import views

from .views import (

        UserListView, UserCreateView, UserUpdateView
)

app_name = 'users'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('user/', UserCreateView.as_view(), name='new-user'),
    path('user/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('my-redirect/', lambda request: redirect('admin:index'), name='my-redirect'),

]