from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list,name='team_list'),
    path('<str:team>/', views.selected_team, name='selected_team'),
    # path('request', views.activate_standing_function, name='activate_standing_function'),
    path('news/<str:team_name>',views.get_team_info,name='get_team_info')
]