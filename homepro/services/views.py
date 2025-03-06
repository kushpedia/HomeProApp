from django.shortcuts import render
from django.http.response import HttpResponse
from.models import Service,ServiceCategory
from .models import ServiceCategory
# Create your views here.

def services(request):
    categories = ServiceCategory.objects.all()
    context ={
        'categories' : categories
    }
    return render(request, 'services/all_services.html', context)

def category(request, pk):
    
    projectObject = ServiceCategory.objects.get(id=pk)
    context = {"category":projectObject}
    return render(request, 'services/single-category.html', context)