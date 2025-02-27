from django.urls import path
from . import views
from .AI_Generator import AI

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('ai/team',views.team_ai,name='team_ai'),
    path('generate-team/', views.generate_team, name='generate_team'),
    path('ask-team-question/', views.ask_team_question, name='ask_team_question'),
    path('generate-league/',views.generate_league,name='generate_league'),
    path('ask-league-question/',views.ask_league_question,name='ask_league_question'),
    path('ai/league',views.league_ai,name='league_ai'),
    path('ai/league/create',views.create_league_by_prompt,name='create_league_by_prompt'),
    path('ai/generateimage/',views.generate_image,name='generate_image'),
]



