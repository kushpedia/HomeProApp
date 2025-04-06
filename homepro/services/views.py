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
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import BookingForm
from users.models import Booking
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz
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
@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    available_providers = Profile.objects.filter(
        Q(services=service)     
    ).distinct()
    # debugging
    # for provider in available_providers:
    #     print(provider.first_name)
    #     print(provider.id)
    #     print(provider.average_rating)
        
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Auto-assign least busy provider
            booking = form.save(commit=False)
            booking.user = request.user.profile
            booking.service = service
            
            # Provider assignment logic
            if available_providers.exists():
                # Get provider with fewest bookings at this time
                from django.db.models import Count
                provider = available_providers.annotate(
                    booking_count=Count(
                        'bookings_received',
                        filter=models.Q(
                            bookings_received__date=booking.date,
                            bookings_received__status__in=['pending', 'confirmed']
                        )
                    )
                ).order_by('booking_count').first()
                booking.provider = provider

            booking.save()
            
            # Send confirmation email
            # send_booking_confirmation(booking)
            
            messages.success(request, 'Your booking has been confirmed!')
            return redirect('homepage')
    else:
        form = BookingForm()
    

    context = {
        'service': service,
        'form': form,
        'available_providers': available_providers
    }
    return render(request, 'services/booking_form.html', context)
    

    

# def send_booking_confirmation(booking):
#     subject = f"Booking Confirmation for {booking.service.name}"
#     message = f"""
#     Hello {booking.user.first_name},
    
#     Your booking for {booking.service.name} has been confirmed.
    
#     Details:
#     - Date: {booking.date.strftime("%A, %B %d %Y at %I:%M %p")}
#     - Provider: {booking.provider.user.get_full_name() if booking.provider else 'To be assigned'}
#     - Special Instructions: {booking.special_instructions or 'None'}
    
#     Thank you for choosing our services!
#     """
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [booking.user.email],
#         fail_silently=False,
#     )
    