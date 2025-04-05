from django.shortcuts import render, get_object_or_404,redirect
from django.http.response import HttpResponse
from.models import Service,ServiceCategory
from .models import ServiceCategory
from users.models import Profile
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


# Get all users who offer services under this category
    