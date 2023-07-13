from datetime import datetime, timedelta
from bc.models import *
from bc.serializers import *
from bc.choices import WHERE_CHOICES_IDS
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

DEFAULT_WEEK = [
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
]


class HistoryApiView(APIView):
    def get(self, request, *args, **kwargs):
        where = request.query_params.get('where')
        week = request.query_params.get('week')

        if not week or not where:
            return Response(data="bad request, provide where/week value", status=status.HTTP_400_BAD_REQUEST)

        where = WHERE_CHOICES_IDS[int(where)]
        stuffs = Stuff.objects.filter(where=where).order_by('frequency')
        start_date, end_date, days = self.calc_start_end_dates(2023, int(week))

        # Filter the StuffRecord objects for the specified week
        stuffrecords = StuffRecord.objects.filter(
            record__where=where, done_on__range=(start_date, end_date)
        ).order_by('done_on')

        data = {
            s['name']: {
                "id": s['id'],
                "where": s['where'],
                "points": s['points'],
                "last_done": self.days_since_today(s['last_done']),
                "frequency": s['frequency'],
                "efforts": {
                    "total_week": [0, 0],
                    "points": DEFAULT_WEEK.copy(),
                },
            }
            for s in StuffSerializer(stuffs, many=True).data
        }

        for record in StuffRecordSerializer(stuffrecords, many=True).data:
            data = self.make_data_entry(record, data)

        data = self.calc_totals(data, days)
        return Response(data=data, status=status.HTTP_200_OK)

    def make_data_entry(self, record, data):
        data[record['record']]['efforts'][record['done_on'][-2:]] = record['aggregated_value'] if (record['done_on'][-2:] not in data[record['record']]['efforts']) else tuple(map(
            sum,
            zip(
                data[record['record']]['efforts'][record['done_on'][-2:]],
                record['aggregated_value'],
            ),
        ))
        return data

    def calc_start_end_dates(self, year, week_number):
        # Create a datetime object for the specified year and week number
        first_day_of_year = datetime(year, 1, 1)
        first_day_of_week = first_day_of_year + \
            timedelta(days=((week_number-1)*7) - first_day_of_year.weekday())

        # Calculate the start date (Monday) and end date (Sunday) of the week
        start_date = first_day_of_week
        end_date = first_day_of_week + timedelta(days=7)
        days = [(first_day_of_week + timedelta(days=i)).day for i in range(7)]

        return start_date, end_date, days

    def calc_totals(self, data, days):
        data['total'] = [0, 0]
        for stuff in data:
            if stuff == 'total':
                continue
            dates = [int(day) for day in data[stuff]['efforts']
                     if day not in ['points', 'total_week']]
            for idx, date in enumerate(days):
                if date in dates:
                    val = ('0' + str(date)) if date <= 9 else str(date)
                    data[stuff]['efforts']['points'][idx] = data[stuff]['efforts'][val]
                    del data[stuff]['efforts'][val]

            data[stuff]['efforts']['total_week'] = [
                sum((row[0] * data[stuff]['points'])
                    for row in data[stuff]['efforts']['points']),
                sum((row[1] * data[stuff]['points'])
                    for row in data[stuff]['efforts']['points'])
            ]

            data['total'][0] += data[stuff]['efforts']['total_week'][0]
            data['total'][1] += data[stuff]['efforts']['total_week'][1]

        data['total_day'] = DEFAULT_WEEK.copy()
        for i in range(7):
            s1, s2 = 0, 0
            for stuff in data:
                if stuff not in 'total_day':
                    s1 += data[stuff]['efforts']['points'][i][0] * \
                        data[stuff]['points']
                    s2 += data[stuff]['efforts']['points'][i][1] * \
                        data[stuff]['points']
            data['total_day'][i] = [s1, s2]

        return data

    def days_since_today(self, target_date):
        today = timezone.datetime.now()
        target_date = timezone.datetime.strptime(
            target_date, '%Y-%m-%d').replace(hour=today.hour)

        if target_date > today:
            return 0
        return (today - target_date).days
