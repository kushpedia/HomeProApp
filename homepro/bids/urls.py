from django.urls import path
from . import views
# from . views import BookingBidsView, accept_bid
urlpatterns = [
    path('', views.bidding_opportunities, name='available_bids'),
    path('bid/<str:booking_id>', views.create_bid, name='create_bid'),
    path('post-bid/', views.post_bid, name='post_bid'),
    path('bookings/<uuid:pk>/bid/', views.BookingBidsView.as_view(), name='booking_bids'),
    path('<uuid:bid_id>/accept/', views.accept_bid, name='accept_bid'),
]