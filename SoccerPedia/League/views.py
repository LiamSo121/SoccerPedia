from django.shortcuts import render, redirect
from .models import League
from django.contrib import messages
from League.League_Helpers import League_Helper
from League.Standings import Standings

# Create your views here.
def present_leagues(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        exists = League.objects.filter(country=country).exists()
        if exists:
            return redirect(f'{country}/')
        else:
            messages.error(request, f"No league found for {country}. Please try again.")
            return redirect('present_leagues')

    return render(request,"league/get_league.html")


def league_details_by_country(request, country):
    league = League.objects.get(country=country)
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


