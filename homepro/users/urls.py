from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('register/',views.userRegistration, name='register'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('account/', views.userAccount, name='account'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'), 
    path('profile/', views.profile, name='profile'), 
    
]