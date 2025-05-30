# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Note
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class NoteAuthTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("list_create_note")

        self.user = User.objects.create_user(username="user", password="password")
        self.user_2 = User.objects.create_user(username="user-2", password="password")

        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.token_2 = str(RefreshToken.for_user(self.user_2).access_token)

        self.note = Note.objects.create(
            title="title_1", content="content_1", author=self.user
        )
        self.note_2 = Note.objects.create(
            title="title_2", content="content_2", author=self.user_2
        )

    def test_get_users_notes(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = response.data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.note.title)
        self.assertEqual(data["content"], self.note.content)
        self.assertEqual(data["author"]["username"], self.user.username)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_creates_note(self):
        response = self.client.post(
            self.url,
            data={"title": "new_title", "content": "new_content"},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        newResponse = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        newData = newResponse.data["results"][0]

        self.assertEqual(len(newResponse.data["results"]), 2)
        self.assertEqual(newData["title"], data["title"])
        self.assertEqual(newData["content"], data["content"])
        self.assertEqual(newData["author"]["username"], data["author"]["username"])

    def test_user_inputs_bad_data(self):
        response = self.client.post(
            self.url,
            data={"turtle": "new_title", "content": "new_content"},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(
            self.url, HTTP_AUTHORIZATION="Bearer sdjf98shf9sdhf9s9d8fa9"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(
            self.url, HTTP_AUTHORIZATION="Bearer fdysh9a78dsf897sf9s"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
