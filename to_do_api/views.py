from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from to_do.models import ToDoNote

from . import serializers

class ToDoNotesAPIView(APIView):
    def get(self, request: Request) -> Response:
        todonotes = ToDoNote.objects.all()
        serializer = serializers.ToDoNotesAPIViewSerializer(instance=todonotes, many=True)

        return Response(serializer.data)





    # queryset = ToDoNote.objects.all()
    # serializer_class = serializers.ToDoNotesAPIView
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(public=True)
    #
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)