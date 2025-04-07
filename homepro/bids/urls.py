from django.urls import path
from . import views

urlpatterns = [
    path('', views.bidding_opportunities, name='available_bids'),
]