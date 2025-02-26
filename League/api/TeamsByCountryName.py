from League.models import League
from League.Serializers import LeagueSerializer
from Team.models import Team
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from Team.Serializers import TeamSerializer


class TeamsByCountryName(APIView):
    @swagger_auto_schema(
        operation_summary="Get all teams by country name",
        operation_id="Get all teams by country name",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'country_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the country to fetch teams for"
                )
            },
            required=['country_name']))
    def post(self,request):
        country_name = request.data.get('country_name')
        if not country_name:
            return Response(
                {"error": "Country name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        league = get_object_or_404(League, country=country_name)
        teams = Team.objects.filter(league=league)
        serialized_videos = TeamSerializer(teams, many=True)
        return Response(serialized_videos.data, status=status.HTTP_200_OK)