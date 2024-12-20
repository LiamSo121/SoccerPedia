from django.urls import path
from . import views

urlpatterns = [
    path('', views.present_leagues, name='present_leagues'),
    path('<str:country>/', views.league_details_by_country, name='league_details_by_country'),
    path('<str:country>/news', views.get_news, name='get_news'),
    path('<str:country>/standings',views.get_league_standings,name='get_league_standings'),

]