from django.contrib.auth import get_user_model
import unittest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.utils import json

from to_do.models import ToDoNote

User = get_user_model()


class TestToDoNoteListCreateAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test@test.ru")

    def test_empty_list_objects(self):
        url = "/todolist/"
        resp = self.client.get(url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        expected_data = []
        self.assertEqual(response_data, expected_data)

    def test_list_objects(self):
        ToDoNote.objects.create(title="Test title", author_id=1)
        test_user = User.objects.get(username="test@test.ru")
        ToDoNote.objects.create(title="Test title", author=test_user)

        url = "/todolist/"
        resp = self.client.get(url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        self.assertEqual(2, len(response_data))


    def test_create_object(self):
        new_title = "test_title"
        url = "/todolist/"
        data = {
            "title": new_title,
            "author": 1
        }
        resp = self.client.post(url, json.dumps(data), content_type="application/json")
        # json.dumps(data)
        # self.response = self.c.post('/pipeline-endpoint', json_data, content_type="application/json")
        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)
        expected_title = new_title
        self.assertEqual(expected_title, resp.data["title"])

    def test_delete_all(self):
        ToDoNote.objects.create(title="Test title", author_id=1)
        test_user = User.objects.get(username="test@test.ru")
        ToDoNote.objects.create(title="Test title", author=test_user)

        url = "/todolist/"
        resp = self.client.get(url)
        response_data = resp.data
        self.assertEqual(2, len(response_data))

        resp = self.client.delete(url)
        # expected_response = "Все записи удалены"
        # self.assertEqual(expected_response, resp)

        resp = self.client.get(url)
        response_data = resp.data
        self.assertEqual(0, len(response_data))
        self.assertEqual([], response_data)



class TestNoteDetailAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test@test.ru")
        test_user = User.objects.get(username="test@test.ru")
        new_title = "Test title"
        ToDoNote.objects.create(title=new_title, author=test_user)


    def test_object_view(self):
        # test_user = User.objects.get(username="test@test.ru")
        # new_title = "Test title"
        # note = Note.objects.create(title=new_title, author=test_user)
        todonote_pk = 1
        url = f"/todolist/{todonote_pk}/"
        resp = self.client.get(url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        # self.assertEqual(note.title, response_data["title"])
        # self.assertEqual(note.id, response_data["id"])
        data = {
            "id": 1,
            "title": "Test title",
            "task_description": "",
            "public": False,
            "author": 1
        }
        self.assertDictEqual(data, response_data)


    def test_object_does_not_exist_view(self):
        url = "/todolist/10/"
        resp = self.client.get(url)
        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

    def test_update_object_view(self):
        test_user = User.objects.get(username="test@test.ru")
        title = "Test title"
        new_title = "New title"
        todonote_pk = 1
        url = f"/todolist/{todonote_pk}/"
        new_data = {
            "title": new_title,
        }
        resp = self.client.put(url, json.dumps(new_data), content_type="application/json")
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)
        self.assertEqual(new_data["title"], resp.data["title"])

    def test_update_does_not_exist_view(self):
        url = "/todolist/1/"
        new_title = "New title"
        new_data = {
            "title": new_title,
        }
        resp = self.client.put(url, json.dumps(new_data), content_type="application/json")
        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

# class ToDoNoteRetrieveUpdateDestroyAPIView(APITestCase):
#     USER_1 = dict(
#         username="username_1",
#         password="fake_password",
#     )
#     USER_2 = dict(
#         username="username_2",
#         password="fake_password",
#     )
#
#     @classmethod
#     def setUpTestData(cls):
#         """
#         Делаем двух пользователей в БД.
#         Каждому из них назначаем по записи.
#         """
#         users = [
#             User(**cls.USER_1),
#             User(**cls.USER_2),
#         ]
#         User.objects.bulk_create(users)
#         cls.db_user_1 = users[0]
#
#         tasks = [
#             ToDoNote(title="title_1", author=users[0]),
#             ToDoNote(title="title_2", author=users[1]),
#         ]
#         ToDoNote.objects.bulk_create(tasks)
#
#     def setUp(self) -> None:
#         """При каждом тестовом методе, будем делать нового клиента и авторизовать его."""
#         self.auth_user_1 = APIClient()
#         self.auth_user_1.force_authenticate(user=self.db_user_1)  # так как не интересуют сами механизмы авторизации, авторизуем нашего пользователя принудительно
#
#     def test_get(self):
#         todonote_pk = 1
#         url = f"/api/v1/todolist/{todonote_pk}/"
#         resp = self.auth_user_1.get(url)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#
#     def test_partial_update_other_task(self):
#         todonote_pk = 2
#         url = f"/api/v1/todolist/{todonote_pk}/"
#         resp = self.auth_user_1.patch(url)
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_update_other_task(self):
#         todonote_pk = 2
#         data = {
#             "title": "fake_title",
#         }
#         url = f"/api/v1/todolist/{todonote_pk}/"
#         resp = self.auth_user_1.put(url, data=data)
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)