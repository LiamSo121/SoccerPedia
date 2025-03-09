from .StadiumList import StadiumList
from django.urls import path
from django.shortcuts import redirect
from .models import Stadium
from . import views

urlpatterns = [
    path('api/data/', StadiumList.as_view(),name='get_stadiums'),
    path('map/',views.redirect_to_map,name='redirect_to_map')

]