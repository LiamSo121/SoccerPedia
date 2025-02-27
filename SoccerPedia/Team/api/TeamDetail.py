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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from SoccerPedia.S3 import S3
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

s3 = S3()

class TeamDetail(APIView):
    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated()]
        return []

    @swagger_auto_schema(
        operation_description='Get Team by ID',
        operation_summary='Get Team by ID',
        operation_id='Get Team By Id',
        responses={200:TeamSerializer, 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self,request,id):
        try:
            team = Team.objects.get(id=id)
            serializer = TeamSerializer(team)
            return Response(serializer.data)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a team",
        operation_id="Delete a team by ID",
        operation_description="Deletes a team based on the provided ID.",
        responses={
            204: openapi.Response(description="Team deleted successfully"),
            404: openapi.Response(description="Team not found")
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )

    def delete(self, request, id):
        try:
            team = get_object_or_404(Team, id=id)
            s3.delete_photo(team.logo)
            team.delete()
            return Response({"message": "Team deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Team.DoesNotExist:
            return Response({'detail': 'Team Not Found'},status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update a Team by ID",
        operation_id="Update a Team by ID",
        operation_description="Update a Team by ID",
        request_body=TeamSerializer,
        responses={
            200: openapi.Response(description="Team updated successfully."),
            400: openapi.Response(description="Bad Request: Invalid data provided."),
            404: openapi.Response(description="Review not found."),
        }
    )
    def put(self, request, id):
        try:
            # Fetch the review by ID
            team = Team.objects.get(id=id)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)