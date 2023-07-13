from django.forms import FloatField
from django.db.models import Max, F, ExpressionWrapper, FloatField
from bc.models import Stuff, StuffRecord, VacationRecord, Setting
from datetime import date


class Helper:
    def calculate_average_for_user(self, username, month, year):
        vacation_days = VacationRecord.objects.filter(
            player__username=username,
            taken_on__month=month,
            taken_on__year=year
        ).values_list('taken_on__day', flat=True)

        stuff_records = StuffRecord.objects.filter(
            player__username=username,
            done_on__month=month,
            done_on__year=year,
        ).values('done_on__day', 'value', 'record__points').annotate(
            product=ExpressionWrapper(
                F('value') * F('record__points'), output_field=FloatField())
        ).values('done_on__day', 'product')

        averages = {}
        for stuff in stuff_records:
            if stuff['done_on__day'] not in vacation_days:
                if stuff['done_on__day'] not in averages:
                    averages[stuff['done_on__day']] = 0.0
                averages[stuff['done_on__day']] += stuff['product']
        days = len(averages)

        return {
            "average": (sum(averages.values()) / days) if days else 0.0,
            "days": days,
        }

    def get_setting(self, what):
        return Setting.objects.filter(active=True, what=what).first()


helper = Helper()
