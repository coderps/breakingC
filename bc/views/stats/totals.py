from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.models import User
from bc.models import StuffRecord
from django.db.models import Sum, F


class TotalAPIView(APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if month is None:
            month = "all"
        if year is None:
            year = timezone.now().year

        response_data = {
            'airin': self.calculate_total_for_user('airin', month, year),
            'prax': self.calculate_total_for_user('prax', month, year)
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def calculate_total_for_user(self, username, month, year):
        user = User.objects.get(username=username)
        stuff_records = StuffRecord.objects.filter(player=user)

        if month != "all":
            stuff_records = stuff_records.filter(
                done_on__month=month, done_on__year=year)
            total = stuff_records.annotate(
                total_value=F('value') * F('record__points')
            ).aggregate(Sum('total_value'))['total_value__sum']
            return float("{:.2f}".format(total)) or 0

        month_totals = stuff_records.annotate(
            month=ExtractMonth('done_on'),
            year=ExtractYear('done_on')
        ).values('month').annotate(
            total=Sum(F('value') * F('record__points'))
        ).order_by('month').values_list('total', flat=True)

        return [float("{:.2f}".format(total)) or 0 for total in month_totals]
