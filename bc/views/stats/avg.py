from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from bc.helpers import helper


class AvgAPIView(APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if month is None:
            month = timezone.now().month
        if year is None:
            year = timezone.now().year

        response_data = {
            'airin': helper.calculate_average_for_user('airin', month, year),
            'prax': helper.calculate_average_for_user('prax', month, year)
        }
        return Response(response_data, status=status.HTTP_200_OK)
