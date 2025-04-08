from django.shortcuts import render,redirect
from homepro import settings
from users.models import Profile,Booking, BookingAttachment
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .forms import BidForm
from django.db import transaction
from django.urls import reverse
from .models import Bid
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


class BookingBidsView(LoginRequiredMixin, ListView):
    template_name = 'bids/booking_bids.html'
    context_object_name = 'bids'
    
    def get_queryset(self):
        self.booking = get_object_or_404(
            Booking, 
            id=self.kwargs['pk'],  # This will now accept UUID
            user=self.request.user.profile
        )
        return self.booking.booking_bid_s.all().order_by('price')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        return context
    
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, booking__user=request.user.profile)
    
    with transaction.atomic():
        # Update booking status and provider
        booking = bid.booking
        booking.status = 'confirmed'
        booking.provider = bid.provider
        booking.save()
        
        # Optionally: Reject all other bids for this booking
        booking.booking_bid_s.exclude(id=bid_id).update(status='rejected')
        
        # Send notifications
        send_bid_accepted_notification(bid)
        
    messages.success(request, f"You've accepted the bid from {bid.provider.full_name}")
    return redirect('booking_history')

def send_bid_accepted_notification(bid):
    subject = f"Your bid for {bid.booking.service.name} has been accepted!"
    message = f"""
    Congratulations {bid.provider.full_name},
    
    Your bid of {bid.price} Ksh for {bid.booking.service.name} has been accepted!
    
    Booking Details:
    -Customer : {bid.booking.user.first_name}
    -Phone : {bid.booking.user.phone}
    - Booking Date: {bid.booking.date}
    - Location: {bid.booking.user.location}
    - Special Instructions: {bid.booking.special_instructions or 'None'}
    
    Please contact the client to confirm details.
    """
    
    email = EmailMessage(
        subject=subject,
        body=message.strip(),
        from_email=settings.EMAIL_HOST_USER,
        to=[bid.provider.email],
    )

    
    email.cc = [bid.booking.user.email]

    email.send(fail_silently=False)