from rest_framework import views, status
from rest_framework.response import Response
from bc.models import Vacation
from django.utils import timezone


class VacationAPIView(views.APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if month is None:
            month = timezone.now().month
        if year is None:
            year = timezone.now().year

        queryset = Vacation.objects.filter(month=month, year=year)
        ap = queryset.filter(player__username='airin')[0].points
        pp = queryset.filter(player__username='prax')[0].points
        return Response((ap, pp), status=status.HTTP_200_OK)
