from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Note


# Create your tests here.
class NoteApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="user", password="userpass")
        self.url = reverse("get-all-notes")
        self.page_size = 3
        for i in range(9):
            Note.objects.create(
                title=f"title {i}", content=f"content {i}", author=self.user
            )
        self.note = Note.objects.create(
            title="test title", content="test content", author=self.user
        )

    def test_correct_data(self):
        response = self.client.get(self.url)
        data = response.data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.note.title)
        self.assertEqual(data["content"], self.note.content)
        self.assertEqual(data["author"]["username"], self.user.username)
        self.assertEqual(response.data["count"], 10)

    def test_pagination(self):
        response = self.client.get(self.url, {"page_size": self.page_size})
        data = response.data["results"]
        self.assertEqual(len(data), self.page_size)
        response = self.client.get(self.url, {"page_size": self.page_size, "page": 2})
        newData = response.data["results"]
        self.assertNotEqual(data[0]["title"], newData[0]["title"])

    def test_only_get_method_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
