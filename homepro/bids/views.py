from django.shortcuts import render,redirect
from homepro import settings
from users.models import Profile,Booking, BookingAttachment

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .forms import BidForm
from django.db import transaction
from django.urls import reverse
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
        user =request.user.profile
    ).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'title': 'Available Tasks for Bidding'
    }
    return render(request, 'services/available_bids.html', context)

# create a biding

@login_required(login_url='login')
def create_bid(request, booking_id):
    booking = get_object_or_404(Booking.objects.prefetch_related('booking_bid_s'), 
                                id=booking_id,
                                status='bidding',
        service__in=request.user.profile.services.all())
    

    form = BidForm()
    
    context = {
        'booking': booking,
        'form': form,
        'title': 'Submit Bid'
    }
    return render(request, 'services/create_bid.html', context)
def post_bid(request):
    if request.method == 'POST':
        
        booking_id = request.POST['booking_id']
        booking = get_object_or_404(
        Booking,
        id=booking_id,
        # status='pending',
        service__in=request.user.profile.services.all()
    ) 
        form = BidForm(request.POST)        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Validate form first
                    if not form.is_valid():
                        raise ValueError("Invalid form data")
                    bid = form.save(commit=False)
                    bid.booking = booking
                    bid.provider = request.user.profile
                    # Ensure required fields exist
                    if not all([bid.booking, bid.provider, form.cleaned_data.get('price')]):
                        raise ValueError("Missing required bid information")
                    
                    
                    bid.price = form.cleaned_data['price']
                    bid.comment = form.cleaned_data['comment']
                    bid.save()
                    # Send notification
                    subject = f"New Bid for {booking.service.name}"
                    message = f"""
                    Hello {booking.user.first_name},
                    
                    You've received a new bid for your booking:{booking.service.name}
                    
                    - Service: {booking.service.name}
                    - Bidder: {bid.provider.full_name}
                    - Price: ${bid.price}
                    - Comments: {bid.comment}
                    
                    View all bids: {request.build_absolute_uri(reverse('booking_history'))}
                    """
                    
                    email = EmailMessage(
                        subject,
                        message.strip(),
                        settings.EMAIL_HOST_USER,
                        [booking.user.email]
                    )
                    email.send(fail_silently=False)
                    
                messages.success(request, 'Your bid has been submitted successfully!')
                return redirect('available_bids')
            except Exception as e:
                messages.error(request, f'Error submitting bid: {str(e)}')
        
    return redirect('available_bids')
        # form = BidForm(request.POST)        
        # if form.is_valid():
        #     try:
        #         with transaction.atomic():
        #             # Validate form first
        #             if not form.is_valid():
        #                 raise ValueError("Invalid form data")
        #             bid = form.save(commit=False)
        #             bid.booking = booking
        #             bid.provider = request.user.profile
        #             # Ensure required fields exist
        #             if not all([bid.booking, bid.provider, form.cleaned_data.get('price')]):
        #                 raise ValueError("Missing required bid information")
                    
                    
        #             bid.price = form.cleaned_data['price']
        #             bid.comment = form.cleaned_data['comment']
        #             bid.save()
                    
        #             # Send notification
        #             subject = f"New Bid for {booking.service.name}"
        #             message = f"""
        #             Hello {booking.user.first_name},
                    
        #             You've received a new bid for your booking:
                    
        #             - Service: {booking.service.name}
        #             - Provider: {bid.provider.full_name}
        #             - Price: ${bid.price}
        #             - Comments: {bid.comment}
                    
        #             View all bids: {request.build_absolute_uri(reverse('available_bids', args=[booking.id]))}
        #             """
                    
        #             email = EmailMessage(
        #                 subject,
        #                 message.strip(),
        #                 settings.EMAIL_HOST_USER,
        #                 [booking.user.email]
        #             )
        #             email.send(fail_silently=False)
                    
        #         messages.success(request, 'Your bid has been submitted successfully!')
        #         return redirect('available_bookings')
        #     except Exception as e:
        #         messages.error(request, f'Error submitting bid: {str(e)}')