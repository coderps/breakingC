from bc.models import *
from bc.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class StuffApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        where_param = request.query_params.get('where')
        stuffs = Stuff.objects.filter(
            where=where_param) if where_param else Stuff.objects.all()
        serializer = StuffSerializer(stuffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = StuffSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
