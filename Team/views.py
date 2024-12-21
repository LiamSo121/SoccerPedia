from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Team,YoutubeVideo
from Team.Team_Helpers import Team_Helper
from .TeamForm import TeamForm, YoutubeVideoFormSet
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

# Create your views here.
def team_list(request):
    # main_teams_names = ['Hapoel Tel Aviv','Manchester United','Tottenham Hotspur','Manchester City','Chelsea','Inter']
    teams = Team.objects.all()
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


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        formset = YoutubeVideoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Save the team instance first
            team = form.save()

            # Save the related YouTube video instances
            youtube_videos = formset.save(commit=False)
            for video in youtube_videos:
                video.team = team  # Associate the video with the team
                video.save()

            return redirect('team_list')
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = TeamForm()
        formset = YoutubeVideoFormSet()

    return render(request, 'team/create_team.html', {'form': form, 'formset': formset})

