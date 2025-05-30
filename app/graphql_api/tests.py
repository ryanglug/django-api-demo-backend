from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Note

PER_PAGE = 5


GETS_NOTES_QUERY = f"""
query {{
    notes(page: 1, perPage: {PER_PAGE}) {{
        notes {{
            id
            title
            content
        }}
        hasNext
    }}
}}
"""


USER_GETS_NOTES_QUERY = f"""
  query {{
      userNotes(page: 1, perPage: {PER_PAGE}) {{
          notes {{
              title
              content
              author{{
                  username
              }}
          }}
          hasNext
      }}
  }}
  """

USER_CREATES_NOTE_MUTATION = """
mutation ($title: String!, $content: String!) {
    createNote(title: $title, content: $content) {
        note {
          id
          title
          content
          createdAt
          author {
            username
          }
      }
  }
}
"""
USER_DELETES_NOTE_MUTATION = """
mutation DeleteNote($noteId: ID!){
  deleteNote(noteId: $noteId) {
    success
  }
}
"""


class GraphQLNoteTest(APITestCase):
    def setUp(self):
        self.url = reverse("graphql_api")
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="password123"
        )

        self.token = str(RefreshToken.for_user(self.user).access_token)

        # Notes for both users
        for i in range(15):
            Note.objects.create(
                title=f"Note {i}",
                content="Lorem ipsum",
                author=self.user if i % 2 == 0 else self.other_user,
            )

    def test_notes_query(self):
        response = self.client.get(self.url, data={"query": GETS_NOTES_QUERY})
        data = response.json()["data"]["notes"]
        self.assertTrue(data["hasNext"])
        self.assertEqual(len(data["notes"]), PER_PAGE)

    def test_user_gets_notes(self):
        response = self.client.get(
            self.url,
            data={"query": USER_GETS_NOTES_QUERY},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        data = response.json()["data"]["userNotes"]
        notes = data["notes"]
        self.assertTrue(data["hasNext"])
        self.assertEqual(len(notes), PER_PAGE)
        for i in range(PER_PAGE):
            self.assertEqual(notes[i]["author"]["username"], self.user.username)

    def test_invalid_user(self):
        response = self.client.get(
            self.url,
            data={"query": USER_GETS_NOTES_QUERY},
            HTTP_AUTHORIZATION="Bearer saj9gj89aujg98ajs9g",
        )

        data = response.json()["data"]["userNotes"]

        self.assertEqual(data, None)

    def test_create_note(self):
        title = "New title"
        content = "New Content"
        response = self.client.post(
            self.url,
            data={
                "query": USER_CREATES_NOTE_MUTATION,
                "variables": {"title": title, "content": content},
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        response_data = response.json()["data"]["createNote"]["note"]

        self.assertEqual(response_data["title"], title)
        self.assertEqual(response_data["content"], content)
        self.assertEqual(response_data["author"]["username"], self.user.username)

        fetch_response = self.client.get(
            self.url,
            data={"query": USER_GETS_NOTES_QUERY},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        data = fetch_response.json()["data"]["userNotes"]["notes"]

        self.assertEqual(data[0]["title"], title)

    def test_user_delete_note(self):
        title = "New title"
        content = "New Content"
        response = self.client.post(
            self.url,
            data={
                "query": USER_CREATES_NOTE_MUTATION,
                "variables": {"title": title, "content": content},
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        data = response.json()["data"]["createNote"]["note"]

        response = self.client.post(
            self.url,
            data={
                "query": USER_DELETES_NOTE_MUTATION,
                "variables": {"noteId": data["id"]},
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        data = response.json()["data"]["deleteNote"]

        self.assertEqual(data["success"], True)
