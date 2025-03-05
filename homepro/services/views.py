from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.

def service(request):
    return HttpResponse("This is services page")