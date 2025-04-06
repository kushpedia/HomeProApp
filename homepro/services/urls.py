from django.urls import path
from . import views
urlpatterns = [
    path("",views.services,name="services"),
    path("category/<str:pk>/",views.category,name="single-category"),
    path("register-service/",views.register_service,name="register-service"),   
    path("load-services/",views.load_services,name="load_services"),
    
    # bookings
    path('book/<str:service_id>/', views.book_service, name='book_service'),
    path('history/', views.BookingHistoryView.as_view(), name='booking_history'),
    path('bookings/<uuid:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
]
