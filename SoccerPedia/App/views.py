from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .AI_Generator import AI
import json
# from App.CustomUserForm import CustomUserForm

ai = AI()
User = get_user_model()

# -------------Operational Views--------------#
def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

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
    if request.method == "GET":
        logout(request)
        return redirect('home')
    return JsonResponse({"error": "Method not allowed"}, status=405)


def register(request):
    # if request.method == 'POST':
    #     form = LeagueForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         league = form.save()
    # else:
    #     form = CustomUserForm()
    #     return render(request, 'app/create_user.html', {'form': form})


    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        additional_info = request.POST.get('additional_info')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'app/register_user.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('home')

        except IntegrityError as e:
            if 'username' in str(e):
                messages.error(request, "Username already exists. Please choose another one.")
            elif 'email' in str(e):
                messages.error(request, "Email already exists. Please use another one.")
            else:
                messages.error(request, "An error occurred while creating your account.")

    return render(request, 'app/register_user.html')


# -------------AI Views--------------#


def team_ai(request):
    return render(request,'app/team_ai_gen.html')

async def generate_team(request):
    team_summary = await ai.generate_random_team_summary()
    return JsonResponse({'team_summary': team_summary})

async def ask_team_question(request):
    question = request.GET.get('question')
    answer = await ai.ask_team_follow_up_question(question)
    return JsonResponse({'answer': answer})

def league_ai(request):
    return render(request,'app/league_ai_gen.html')

async def generate_league(request):
    league_summary = await ai.generate_random_league_summary()
    return JsonResponse({'league_summary': league_summary})

async def ask_league_question(request):
    question = request.GET.get('question')
    answer = await ai.ask_league_follow_up_question(question)
    return JsonResponse({'answer': answer})

def create_league_by_prompt(request):
    answer = ai.create_league_by_prompt()
    return answer

def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        image_url = ai.generate_image(prompt)
        print(image_url)
        return render(request,'app/generate_image.html', {'image_url': image_url})

    return render(request, 'app/generate_image.html')


