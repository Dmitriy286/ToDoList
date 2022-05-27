from django.shortcuts import render
from rest_framework.generics import ListAPIView

from to_do.models import ToDoNote

from . import serializers

class ToDoNotesAPIView(ListAPIView):
    queryset = None
    serializer_class = serializers.