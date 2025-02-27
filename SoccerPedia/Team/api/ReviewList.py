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

class ReviewList(APIView):
    @swagger_auto_schema(operation_description='Get All Reviews',
                         operation_summary="Get All Reviews",
                         operation_id='Get Reviews',
                         responses={200: openapi.Response('A list of reviews', ReviewSerializer(many=True))})
    def get(self,request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new Review",
        operation_id="Create New Review",
        request_body=ReviewSerializer,
        responses={
            201: openapi.Response(
                description="Review successfully created",
                schema=ReviewSerializer()
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
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)