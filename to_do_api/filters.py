from typing import Optional
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters

from to_do.models import ToDoNote


def author_id_filter(queryset: QuerySet, author_id: Optional[int]):
    if author_id is not None:
        return queryset.filter(author_id=author_id)
    else:
        return queryset

class ToDoNoteFilter(filters.FilterSet):
    # public = filters.BooleanFilter(
    #     field_name="public",
    #     help_text = "Публичная",
    # )

    class Meta:
        model = ToDoNote
        fields = ['public', 'important', 'status',]
