from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User

from to_do.models import ToDoNote, Comment

from . import serializers, filters


class ToDoNotesAPIView(APIView):
    def get(self, request: Request) -> Response:
        todonotes = ToDoNote.objects.all()
        serializer = serializers.ToDoNotesAPIViewSerializer(instance=todonotes, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = serializers.NoteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request: Request) -> Response:
        todonotes = ToDoNote.objects.all()
        todonotes.delete()

        return Response("Все задачи удалены")



class ToDoNoteListAPIView(ListAPIView):
    queryset = ToDoNote.objects.all()
    serializer_class = serializers.NoteSerializer

    # def get_queryset(self):
    #     print(self.request.query_params)
    #     queryset = super().get_queryset()
    #     return queryset


    def filter_queryset(self, queryset):
        query_params = serializers.QueryParamsCommentFilterSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        list_status = query_params.data.get("status")
        if list_status:
            queryset = queryset.filter(status__in=query_params.data["status"])

        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author=author)

        public = self.request.query_params.get("public")
        if public:
            queryset = queryset.filter(public=True)

        important = self.request.query_params.get("important")
        if important:
            queryset = queryset.filter(important=True)


        return queryset



class ToDoNoteListAPIViewWithFilters(ListAPIView):
    queryset = ToDoNote.objects.all()
    serializer_class = serializers.NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ToDoNoteFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset #\
            # .filter(public=True) \
            # .order_by("-create_at") \
            # .prefetch_related("authors", "comments")




class ToDoNotesPublicAPIView(ListAPIView):
    queryset = ToDoNote.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(public=True)


class ToDoNotesDetailGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ToDoNote.objects.all()
    serializer_class = serializers.NoteSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CommentListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        comments = Comment.objects.all()
        return Response([serializers.serialize_comment_created(comment) for comment in comments])

    def post(self, request: Request) -> Response:
        data = request.data

        comment = Comment(todonote_id=data["todonote"], message=data["message"], author=request.user)
        # comment.save(force_insert=True)
        # return Response(serializers.serialize_comment_created(comment), status=status.HTTP_201_CREATED)
        if comment.todonote.public:
            comment.save(force_insert=True)
            return Response(serializers.serialize_comment_created(comment), status=status.HTTP_201_CREATED)
        else:
            return Response("Запись не публичная")



