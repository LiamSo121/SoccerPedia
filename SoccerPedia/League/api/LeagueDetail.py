from League.models import League
from League.Serializers import LeagueSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from SoccerPedia.S3 import S3
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

s3 = S3()

class LeagueDetail(APIView):

    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        """Require authentication for POST, PUT, DELETE but allow GET"""
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated()]
        return []


    @swagger_auto_schema(
        operation_description='Get League by ID',
        operation_summary='Get League by ID',
        operation_id='Get League by ID',
        responses={200:LeagueSerializer, 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self,request,id):
        try:
            team = League.objects.get(id=id)
            serializer = LeagueSerializer(team)
            return Response(serializer.data)
        except League.DoesNotExist:
            return Response({'error': 'League not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a League",
        operation_id="Delete a League by ID",
        operation_description="Deletes a League based on the provided ID.",
        responses={
            200: openapi.Response(description="League deleted successfully", schema=LeagueSerializer()),
            404: openapi.Response(description="League not found")
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Item ID", type=openapi.TYPE_INTEGER)
        ]
    )

    def delete(self, request, id):
        try:
            league = get_object_or_404(League, id=id)
            deleted_league_data = LeagueSerializer(league).data
            s3.delete_photo(league.logo)
            league.delete()
            return Response(
        {"message": "League deleted successfully", "deleted_league": deleted_league_data},
        status=status.HTTP_200_OK  # Changed from 204 to 200 to return data
            )
        except League.DoesNotExist:
            return Response({'detail': 'Team Not Found'},status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update a League by ID",
        operation_id="Update a League by ID",
        operation_description="Update a League by ID",
        request_body=LeagueSerializer,
        responses={
            200: openapi.Response(description="League updated successfully."),
            400: openapi.Response(description="Bad Request: Invalid data provided."),
            404: openapi.Response(description="League not found."),
        }
    )
    def put(self, request, id):
        try:
            league = League.objects.get(id=id)
        except League.DoesNotExist:
            return Response({"error": "League not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LeagueSerializer(league, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)