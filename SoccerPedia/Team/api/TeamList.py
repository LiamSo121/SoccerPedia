from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from Team.models import Team,YoutubeVideo,Review
from Team.Team_Helpers import Team_Helper
from Team.TeamForm import TeamForm, YoutubeVideoFormSet,ReviewForm, VideoForm
from Team.Serializers import TeamSerializer,ReviewSerializer,YoutubeVideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from SoccerPedia.S3 import S3
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


s3 = S3()
helper = Team_Helper()

class TeamList(APIView):

    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        """Require authentication for POST, PUT, DELETE but allow GET"""
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    @swagger_auto_schema(operation_description='Get All Teams',
                         operation_summary="Get All Teams",
                         operation_id='Get Teams',
                         responses={200:TeamSerializer})
    def get(self,request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_summary="Create a new team",
        operation_id="Create New Team",
        request_body=TeamSerializer,
        responses={
            201: openapi.Response(
                description="Team successfully created",
                schema=TeamSerializer()
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "name": ["This field is required."],
                        "description": ["Ensure this field has no more than 255 characters."]
                    }
                }
            ),
        }
    )
    def post(self,request):
        serializer = TeamSerializer(data = request.data)
        if serializer.is_valid():
            team = serializer.save()
            if 'logo' in request.FILES:
                file_obj = request.FILES['logo']
                file_obj.seek(0)
                object_key = s3.upload_photo(file_obj,'team')
                if object_key:
                    fixed_url = helper.fix_url(object_key)
                    team.logo = fixed_url
                    team.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)