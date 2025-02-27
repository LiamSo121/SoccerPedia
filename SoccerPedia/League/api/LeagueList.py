from django.shortcuts import render, redirect
from League.models import League
from django.contrib import messages
from League.League_Helpers import League_Helper
from League.Standings import Standings
from League.Serializers import LeagueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from League.League_Helpers import League_Helper
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

helper = League_Helper()



class LeagueList(APIView):
    authentication_classes = [JWTAuthentication]

    def get_premissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []


    @swagger_auto_schema(operation_description='Get All Leagues',
                         operation_summary='Get All Leagues',
                         operation_id='Get Leagues',
                         responses={200:LeagueSerializer})
    def get(self,request):
        leagues = League.objects.all()
        serializer = LeagueSerializer(leagues, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new League",
        operation_id="Create New League",
        request_body=LeagueSerializer,
        responses={
            201: openapi.Response(
                description="League successfully created",
                schema=LeagueSerializer()
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
        serializer = LeagueSerializer(data = request.data)
        if serializer.is_valid():
            league = serializer.save()
            if 'logo' in request.FILES:
                file_obj = request.FILES['logo']
                file_obj.seek(0)
                object_key = s3.upload_photo(file_obj,'league')
                if object_key:
                    fixed_url = helper.fix_url(object_key)
                    league.logo = fixed_url
                    league.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)