from django.urls import path
from . import views

urlpatterns = [
  path("note/", views.NoteListView.as_view(), name="get-all-notes"),
]