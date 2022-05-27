from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from django.db import models

def dateTimePoint():
    return datetime.now() + timedelta(days=1)

class ToDoNote(models.Model):
    title = models.CharField(max_length=255, verbose_name="Задача")
    task_description = models.TextField(default="", verbose_name="Описание задачи")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    time_point = models.DateTimeField(default=dateTimePoint, blank=True, verbose_name="Время обновления") #todo add calender
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # status = models.



    def __str__(self):
        return f'Задача: {self.title} № {self.id}'

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")