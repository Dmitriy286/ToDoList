"""ToDoList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/about/', views.IndexView.as_view()),
    path('api/v1/todolist/', views.ToDoNotesAPIView.as_view()),
    # path('api/v1/todolist/', views.ToDoNoteListAPIView.as_view()),
    # path('api/v1/todolist/', views.ToDoNoteListAPIViewWithFilters.as_view()),
    path('api/v1/todolist/public/', views.ToDoNotesPublicAPIView.as_view()),
    path('api/v1/todolist/<int:pk>/', views.ToDoNotesDetailGenericAPIView.as_view()),
    # path('api/v1/todolist/<int:pk>/', views.ToDoNotesDetailDeleteGenericAPIView.as_view()),
    path('api/v1/comments/', views.CommentListCreateAPIView.as_view()),
    # path('api/v1/comments/<int:pk>/', views.CommentDetailAPIView.as_view()),
]
