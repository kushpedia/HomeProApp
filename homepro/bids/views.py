from django.shortcuts import render

from users.models import Profile,Booking
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def bidding_opportunities(request):
    # Get bookings that:
    # 1. Are in 'bidding' status
    # 2. Match the provider's services
    # 3. Haven't been bid on by this provider yet
    bookings = Booking.objects.filter(
        status='bidding',
        service__in=request.user.profile.services.all()
    ).exclude(
        provider=request.user.profile
    ).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'title': 'Available Tasks for Bidding'
    }
    return render(request, 'services/available_bids.html', context)