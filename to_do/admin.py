from django.contrib import admin
from .models import ToDoNote

@admin.register(ToDoNote)
class ToDoNoteAdmin(admin.ModelAdmin):
    pass