from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Team,YoutubeVideo,Review
from Team.Team_Helpers import Team_Helper
from .TeamForm import TeamForm, YoutubeVideoFormSet,ReviewForm, VideoForm
from .Serializers import TeamSerializer,ReviewSerializer,YoutubeVideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from SoccerPedia.S3 import S3
import asyncio
from asgiref.sync import sync_to_async  # For async rendering


s3 = S3()

@sync_to_async
def async_render(request,template_name,context):
    return render(request,template_name=template_name,context=context)

@sync_to_async
def get_teams():
    return Team.objects.all

async def team_list(request):
    teams = await get_teams()
    context = {'teams': teams}
    return await async_render(request,'team/team_list.html',context)

@sync_to_async
def get_team(team):
    selected_team = get_object_or_404(Team, name=team)

def selected_team(request,team):
    selected_team = get_object_or_404(Team, name=team)
    context = {'team': selected_team}
    # return await async_render(request,'team/team_details.html',context)
    return render(request,'team/team_details.html',{'team': selected_team})

@sync_to_async
def get_team_by_name(team_name):
    return get_object_or_404(Team, name=team_name)

@sync_to_async
def get_videos_by_team(team:Team):
    return list(YoutubeVideo.objects.filter(team=team))

async def get_team_info(request, team_name):
    # Fetching news data asynchronously
    helper = Team_Helper()
    news_data = await helper.get_news_by_team_id(team_name)
    team = await get_team_by_name(team_name)
    youtube_links = await get_videos_by_team(team)
    video_data = [{'title': video.title, 'url': video.url.replace('watch?v=', 'embed/')} for video in youtube_links]
    context = {
        'news': news_data,
        'video_data': video_data,
    }
    return await async_render(request, 'team/team_info.html', context)

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            review = form.save()
            if 'image' in request.FILES:
                file_obj = request.FILES['image']
                file_obj.seek(0)
                object_key = s3.upload_photo(file_obj,'review')
                if object_key:
                    review.image = object_key
                else:
                    print("something went wrong")

            return redirect('team_list')
        else:
            return HttpResponse(form.errors)
    else:
        form = ReviewForm()
        return render(request, 'team/create_review.html', {'form': form})

@login_required
def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse(form.errors)
    else:
        form = VideoForm()
        return render(request, 'team/create_video.html', {'form': form})

@login_required()
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        formset = YoutubeVideoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            team = form.save()
            if 'logo' in request.FILES:
                file_obj = request.FILES['logo']
                file_obj.seek(0)
                object_key = s3.upload_photo(file_obj,'team')
                if object_key:
                    team.logo = object_key
                else:
                    print("something went wrong")


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
    context = {'form': form, 'formset': formset}
    # return await async_render(request,'team/create_team.html',context)
    return render(request, 'team/create_team.html', {'form': form, 'formset': formset})

