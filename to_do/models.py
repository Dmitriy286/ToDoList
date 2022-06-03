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
    public = models.BooleanField(default=False, verbose_name="Опубликовать") #todo публичные должны видеть все пользователи
    important = models.BooleanField(default=False, verbose_name="Важность")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    time_point = models.DateTimeField(default=dateTimePoint, blank=True, verbose_name="Срок выполнения") #todo add calender
    author = models.ForeignKey(User, on_delete=models.CASCADE)





    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")


    class Status(models.IntegerChoices):
        ACTIVE = 0, _('Активно')
        POSTPONED = 1, _('Отложено')
        PERFORMED = 2, _('Выполнено')


    status = models.IntegerField(default=Status.ACTIVE, choices=Status.choices, verbose_name="Статус")

    def __str__(self):
        return f'Задача: {self.title}'

class Comment(models.Model):
    todonote = models.ForeignKey(ToDoNote, on_delete=models.CASCADE, related_name='todocomments')
    message = models.TextField(default="", verbose_name="Комментарий")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Комментарий к задаче {self.todonote.title}, от {self.author}'