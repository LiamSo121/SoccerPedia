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


class YoutubeVideoDetail(APIView):
    @swagger_auto_schema(
        operation_description='Get Video by ID',
        operation_summary="Get Video By ID",
        operation_id='Get Video By Id',
        responses={
            200: openapi.Response('A review by ID', YoutubeVideoSerializer),  # Proper Response object
            404: 'Not Found'
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self,request,id):
        try:
            video = YoutubeVideo.objects.get(id=id)
            serializer = YoutubeVideoSerializer(review)
            return Response(serializer.data)
        except YoutubeVideo.DoesNotExist:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a Video by ID",
        operation_id="Delete a Video by ID",
        operation_description="Deletes a Video based on the provided ID.",
        responses={
            204: openapi.Response(description="Video deleted successfully"),
            404: openapi.Response(description="Video not found")
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )

    def delete(self, request, id):
        try:
            video = get_object_or_404(YoutubeVideo, id=id)
            video.delete()
            return Response({"message": "Video deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except YoutubeVideo.DoesNotExist:
            return Response({'detail': 'Video Not Found'},status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update a video by ID",
        operation_id="Update a video by ID",
        request_body=YoutubeVideoSerializer,
        responses={
            200: openapi.Response(description="Video updated successfully."),
            400: openapi.Response(description="Bad Request: Invalid data provided."),
            404: openapi.Response(description="Video not found."),
        }
    )
    def put(self, request, id):
        try:
            # Fetch the review by ID
            video = YoutubeVideo.objects.get(id=id)
        except YoutubeVideo.DoesNotExist:
            return Response({"error": "Video not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = YoutubeVideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)