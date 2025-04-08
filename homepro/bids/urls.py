from django.urls import path
from . import views

urlpatterns = [
    path('', views.bidding_opportunities, name='available_bids'),
    path('bid/<str:booking_id>', views.create_bid, name='create_bid'),
    path('post-bid/', views.post_bid, name='post_bid'),
]