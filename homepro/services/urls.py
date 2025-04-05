from django.urls import path
from . import views
urlpatterns = [
    path("",views.services,name="services"),
    path("category/<str:pk>/",views.category,name="single-category"),
    path("register-service/",views.register_service,name="register-service"),   
    path("load-services/",views.load_services,name="load_services"),
    
]
