from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from bc.choices import WHERE_CHOICES_IDS


class RoomsApiView(APIView):
    def get(self, request, *args, **kwargs):
        choices = [
            {"id": id, "name": name}
            for id, name in WHERE_CHOICES_IDS.items()
        ]
        return Response(choices, status=status.HTTP_200_OK)
