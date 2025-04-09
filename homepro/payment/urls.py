from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.subscribe,name='subscribe'),
    # path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
    path('options/', views.payment_options, name='payment_options'),
    path('process/', views.process_payment, name='process_payment'),
    
]