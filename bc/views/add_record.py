from bc.models import *
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

SCORE_REDUCER_PRECENTAGE = 0.08


class StuffRecordApiView(APIView):
    def post(self, request):
        try:
            data = request.data
            for username, records in data.items():
                user = User.objects.get(username=username)
                for record_data in records:
                    stuff_id, done_on, value = record_data
                    if value in ['', None, 'f', 'F', 'n', 'no']:
                        value = 0
                    value = float(value)
                    stuff = Stuff.objects.get(id=stuff_id)
                    done_on = timezone.datetime.strptime(
                        done_on, "%Y-%m-%d").date()

                    # Check if StuffRecord entry already exists for the given user and stuff
                    stuff_record = StuffRecord.objects.filter(
                        record=stuff,
                        player__username=username,
                        done_on=done_on,
                    ).first()
                    if stuff_record:
                        if value:
                            print("INFO: updating existing record", stuff_record)
                            stuff_record.value = value
                            stuff_record.save()
                        else:
                            print("INFO: deleting existing record", stuff_record)
                            stuff_record.delete()
                    elif value:
                        print("INFO: creating new record",
                              stuff, user, value, done_on)
                        reduction = self.calculate_reduced(stuff, done_on)
                        StuffRecord.objects.create(
                            record=stuff,
                            player=user,
                            value=value*reduction,
                            done_on=done_on,
                            reduction=reduction,
                        )

            return Response({"message": "StuffRecord entries successfully stored/updated."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("ERROR", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_reduced(self, stuff: Stuff, done_on: date) -> float:
        setting = Setting.objects.filter(
            active=True,
            what='enable_points_reduction',
        ).first()
        if setting and setting.value == 'on':
            due_date = stuff.last_done.__add__(timedelta(stuff.frequency))
            if not stuff.frequency or done_on <= due_date:
                return 1

            days_passed = (done_on - due_date).days
            if days_passed > 7:
                # TODO: reduce 1 vacation point for each day passed from each user
                days_passed = 7
            rection_multiplier = 1 - (days_passed * SCORE_REDUCER_PRECENTAGE)
            print(
                f"INFO: days_passed detected reducing score :( to {rection_multiplier}%")
            return rection_multiplier
        return 1
