from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Stadium.models import Stadium
from Stadium.Serializers import StadiumSerializer
from drf_yasg.utils import swagger_auto_schema



class StadiumList(APIView):
    @swagger_auto_schema(operation_description='Get All Stadiums',
                         operation_summary='Get All Stadiums',
                         operation_id='Get Stadiums',
                         responses={200:StadiumSerializer})
    def get(self, request):
        stadiums = Stadium.objects.all()
        serializer = StadiumSerializer(stadiums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)