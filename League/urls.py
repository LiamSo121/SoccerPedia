from django.urls import path
from . import views
from .api.LeagueList import LeagueList
from .api.LeagueDetail import LeagueDetail
from .api.TeamsByCountryName import TeamsByCountryName

urlpatterns = [
    path('', views.present_leagues, name='present_leagues'),
    path('create/',views.create_league,name='create_league'),
    path('<str:country>/', views.league_details_by_country, name='league_details_by_country'),
    path('<str:country>/news', views.get_news, name='get_news'),
    path('<str:country>/standings',views.get_league_standings,name='get_league_standings'),
    path('data/api/', LeagueList.as_view(), name='example'),
    path('data/api/<int:id>', LeagueDetail.as_view(), name='league_by_id'),
    path('teams/data/api',TeamsByCountryName.as_view(),name='teams_by_league')
]