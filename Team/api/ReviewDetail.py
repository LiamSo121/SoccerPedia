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

class ReviewDetail(APIView):
    @swagger_auto_schema(
        operation_description='Get Review by ID',
        operation_summary="Get Review By ID",
        operation_id='Get Review By Id',
        responses={
            200: openapi.Response('A review by ID', ReviewSerializer),  # Proper Response object
            404: 'Not Found'
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self,request,id):
        try:
            review = Review.objects.get(id=id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a Review",
        operation_id="Delete a Review",
        operation_description="Deletes a Review based on the provided ID.",
        responses={
            200: openapi.Response(
                description="Review deleted successfully",
                examples={
                    "application/json": {
                        "message": {
                            "id": 1,
                            "content": "This is the deleted review",
                            "rating": 5
                        }
                    }
                }
            ),
            404: openapi.Response(description="Review not found"),
        },
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="Review ID", type=openapi.TYPE_INTEGER
            )
        ]
    )
    def delete(self, request, id):
        review = get_object_or_404(Review, id=id)
        serialized_review = ReviewSerializer(review).data
        review.delete()
        return Response({"message": serialized_review}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a review by ID",
        operation_id="Update a review by ID",
        operation_description="Updates the content, stars, and/or image of the review by the specified review ID.",
        request_body=ReviewSerializer,
        responses={
            200: openapi.Response(description="Review updated successfully."),
            400: openapi.Response(description="Bad Request: Invalid data provided."),
            404: openapi.Response(description="Review not found."),
        }
    )
    def put(self, request, id):
        try:
            # Fetch the review by ID
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)