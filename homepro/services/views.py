from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from.models import Service,ServiceCategory
from .models import ServiceCategory
from users.models import Profile
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