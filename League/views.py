from itertools import count
from django.shortcuts import render, redirect
from .LeagueForm import LeagueForm
from .models import League
from django.contrib import messages
from League.League_Helpers import League_Helper
from League.Standings import Standings
from .Serializers import LeagueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required
from SoccerPedia.S3 import S3
from asgiref.sync import sync_to_async  # For async rendering
import asyncio


s3 = S3()
@sync_to_async
def async_render(request,template_name,context):
    return render(request,template_name=template_name,context=context)

@sync_to_async
def get_countries():
    countries = list(League.objects.values_list('country',flat=True))
    return countries

def present_leagues(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        exists = League.objects.filter(country=country).exists()
        if exists:
            return redirect(f'{country}/')
        else:
            messages.error(request, f"No league found for {country}. Please try again.")
            return redirect('present_leagues')
    elif request.method == 'GET':
        helper = League_Helper()
        countries_dict = {}
        # countries = await get_countries()
        countries = League.objects.values_list('country',flat=True)
        for country in countries:
            countries_dict[country] = League_Helper.get_country_flag_url(League_Helper,country)
        # countries_dict = await helper.get_flags(countries)
        # return await async_render(request,"league/get_league.html",{'countries_dict': countries_dict})
        return render(request,"league/get_league.html",{'countries_dict': countries_dict})


def league_details_by_country(request, country):
    league = League.objects.filter(country=country).first()
    if league:
        return render(request, "league/league.html", {"league": league})


def get_news(request, country):
    helper = League_Helper()
    league_news = helper.get_league_news(country)
    return render(request, 'league/league_news.html',
        {'news': league_news})

def get_league_standings(request,country):
    stats = Standings()
    standings = stats.get_standings(country)
    return render(request, "league/standings.html", {"standings": standings})

@login_required
def create_league(request):
    if request.method == 'POST':
        form = LeagueForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            league = form.save()
            if 'logo' in request.FILES:
                print(request.FILES['logo'])
                file_obj = request.FILES['logo']
                file_obj.seek(0)
                object_key = s3.upload_photo(file_obj,'league')
                if object_key:
                    league.logo = object_key
                else:
                    print("something went wrong")
            return redirect('present_leagues')
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = LeagueForm()
        return render(request, 'league/create_league.html', {'form': form})