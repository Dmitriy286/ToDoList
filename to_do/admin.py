from django.contrib import admin
from .models import ToDoNote, Comment

@admin.register(ToDoNote)
class ToDoNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_description', 'public', 'important', 'time_point', 'status')

    fields = (('title', 'public'), ('time_point', 'create_at'), 'task_description', 'important', 'status')

    readonly_fields = ['create_at']

    search_fields = ('status', 'important', 'public')

    search_help_text = "Фильтр по состоянию, важности и публичности"

    list_filter = ['public']

    # sortable_by = ['create_at', 'important']

    ordering = ('create_at', 'important')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass