from django.urls import path
from . import views
urlpatterns = [
    path("",views.services,name="services"),
    path("category/<str:pk>/",views.category,name="single-category"),
    
]
