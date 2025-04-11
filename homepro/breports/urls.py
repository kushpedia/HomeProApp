from django.urls import path
from .views import BookingsOverviewReport

urlpatterns = [
    path('', BookingsOverviewReport.as_view(), name='bookings_report'),
]