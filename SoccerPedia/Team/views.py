from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Team,YoutubeVideo
from Team.Team_Helpers import Team_Helper

# Create your views here.
def team_list(request):
    main_teams_names = ['Hapoel Tel Aviv','Manchester United','Tottenham Hotspur','Manchester City','Chelsea','Inter']
    teams = Team.objects.filter(name__in=main_teams_names)
    return render(request,'team/team_list.html',{'teams': teams})

def selected_team(request,team):
    selected_team = get_object_or_404(Team,name=team)
    return render(request,'team/team_details.html',{'team': selected_team})


def get_team_info(request,team_name):
    helper = Team_Helper()
    news_data = helper.get_news_by_team_id(team_name)
    team = get_object_or_404(Team, name=team_name)
    youtube_links = YoutubeVideo.objects.filter(team=team)
    video_data = [{'title': video.title, 'url': video.url.replace('watch?v=', 'embed/')} for video in youtube_links]
    context = {'news': news_data,
        'video_data': video_data,}
    return render(request,'team/team_info.html', context= context)





