from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadedImage
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate,login,logout



def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        additional_info = request.POST.get('additional_info')
        if username and email and password:
            user = User.objects.create_user(username=username,email=email,password=password)
            Profile.objects.create(user=user,additional_info=additional_info)
        return redirect('home')


    elif request.method == 'GET':
        return render(request,'app/register_user.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'app/login_user.html',{'error': 'invalid username or password'})

    return render(request,'app/login_user.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')