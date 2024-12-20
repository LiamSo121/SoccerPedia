from django.shortcuts import render
from django.http import HttpResponse
from .models import UploadedImage

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

