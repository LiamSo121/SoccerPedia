from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list,name='team_list'),
    path('<str:team>/', views.selected_team, name='selected_team'),
    path('create/team',views.create_team,name='create_team'),
    path('news/<str:team_name>',views.get_team_info,name='get_team_info'),

]