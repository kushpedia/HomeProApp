from django.shortcuts import render, get_object_or_404,redirect
from django.http.response import HttpResponse
from.models import Service,ServiceCategory
from users.models import Profile
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q, Avg
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import BookingForm
from users.models import Booking, BookingAttachment
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
timezone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratelimit.decorators import ratelimit

# Create your views here.

def services(request):
    categories = ServiceCategory.objects.all()
    
    context ={
        'categories' : categories
    }
    return render(request, 'services/all_services.html', context)

def category(request, pk):
    category = get_object_or_404(ServiceCategory, id=pk)
    # Get all users who offer services under this category
    users = Profile.objects.filter(services__category=category).distinct()
    
    
    context = {
        "category": category,
        "users": users
    }
    return render(request, 'services/single-category.html', context)

# user register for services . become a service provider
@login_required(login_url='login')
def register_service(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure user is logged in
    
    if request.method == 'POST':
        profile = request.user.profile
        selected_services = request.POST.getlist('services')
        
        # Set the user's role to service provider
        # Update role to 'service_provider' if currently 'customer'
        if profile.role == 'customer':
            profile.role = 'provider'
            profile.save()
        # Only add services that aren't already registered
        new_services = [s for s in selected_services if s not in 
                        profile.services.values_list('id', flat=True)]
        
        if new_services:
            profile.services.add(*new_services)
            messages.success(request, f'Successfully registered {len(new_services)} new service(s)!')
        else:
            messages.info(request, 'No new services selected to register')
            
        return redirect('profile')  # Redirect back to the same page
    
    # GET request - show the form
    categories = ServiceCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'services/register_service.html', context)
@login_required(login_url='login')
# load services
def load_services(request):
    category_id = request.GET.get('category')
    services = Service.objects.filter(category=category_id)
    
    # Get the user's currently registered services
    user_services = []
    if request.user.is_authenticated:
        user_services = request.user.profile.services.values_list('id', flat=True)
    
    context = {
        'services': services,
        'user_services': user_services
    }
    
    return render(request, 'services/services_partial.html', context)

def category(request, pk):
    category = get_object_or_404(ServiceCategory, id=pk)
    users = Profile.objects.filter(services__category=category).distinct().prefetch_related('services')
    services = Service.objects.filter(category=category).distinct()
    
    context = {
        "category": category,
        "users": users,
        "services": services,
    }
    return render(request, 'services/single-category.html', context)


# Bookings
# @ratelimit(key='user', rate='2/day', method='POST', block=True)
@login_required(login_url='login')
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    available_providers = Profile.objects.filter(
        services=service,
        is_available=True
    ).annotate(
        avg_rating=Avg('reviews__rating'),
    ).order_by('-avg_rating')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        # print("request.FILES:", request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user.profile
            booking.service = service
            booking.date = form.cleaned_data['date']
            
            # Handle provider assignment
            preferred_provider_id = request.POST.get('provider')
            if preferred_provider_id:
                try:
                    booking.provider = Profile.objects.get(
                        id=preferred_provider_id,
                        services=service
                    )
                except Profile.DoesNotExist:
                    messages.warning(request, 'Selected provider not available')
            
            # Save the booking first
            booking.save()
            # Send confirmation email
            send_booking_confirmation(booking)
            # Handle file uploads

            if 'attachments' in request.FILES:
                print("Attachments found")
                for file in request.FILES.getlist('attachments'):
                    BookingAttachment.objects.create(
                        booking=booking,
                        file=file
                    )
            
            messages.success(request, 'Booking confirmed!')
            return redirect('homepage')
        
        else:
            messages.error(request, 'Error in booking form. Please check your inputs.')
            print("Form errors:", form.errors)
    else:
        form = BookingForm(initial={
            'date': timezone.now() + timedelta(days=1)
        })
    
    context = {
        'service': service,
        'form': form,
        'available_providers': available_providers,
        'today': timezone.now().date()
    }
    return render(request, 'services/booking_form.html', context)
def send_booking_confirmation(booking):
    subject = f"Booking Confirmation for {booking.service.name}"
    message = f"""
    Hello {booking.user.first_name},
    
    Your booking for {booking.service.name} has been Received.
    
    Details:
    - Date: {booking.date.strftime("%A, %B %d %Y at %I:%M %p")}
    - Provider: 'To be assigned'
    - Special Instructions: {booking.special_instructions or 'None'}
    
    Thank you for choosing our services!
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [booking.user.email],
        fail_silently=False,
    )
    

# booking history
class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'services/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user.profile).order_by('-date')
    
class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'services/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user.profile)