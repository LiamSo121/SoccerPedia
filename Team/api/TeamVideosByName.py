from django.shortcuts import get_object_or_404
from Team.models import Team,YoutubeVideo
from Team.Serializers import YoutubeVideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TeamVideosByName(APIView):
    @swagger_auto_schema(
        operation_summary="Get all videos for a team by name",
        operation_id="Get all videos by team name",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'team_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the team to fetch videos for"
                )
            },
            required=['team_name']))
    def post(self,request):
        team_name = request.data.get('team_name')
        if not team_name:
            return Response(
                {"error": "Team name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        team = get_object_or_404(Team, name=team_name)
        videos = YoutubeVideo.objects.filter(team=team)
        serialized_videos = YoutubeVideoSerializer(videos, many=True)
        return Response(serialized_videos.data, status=status.HTTP_200_OK)