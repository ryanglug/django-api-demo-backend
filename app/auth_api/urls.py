from django.urls import path

from .views import (
    CreateUserView,
    CustomLogoutView,
    CustomObtainTokenView,
    CustomRefreshTokenView,
    GoogleLoginView,
    NoteDeleteView,
    NoteEditView,
    NoteListCreateView,
    RetrieveUserView,
)

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", CustomObtainTokenView.as_view(), name="login"),
    path("login/google/", GoogleLoginView.as_view(), name="google_login"),
    path("refresh/", CustomRefreshTokenView.as_view(), name="refresh"),
    path("api/note/", NoteListCreateView.as_view(), name="list_create_note"),
    path("api/note/edit/", NoteEditView.as_view(), name="note_edit"),
    path("api/note/delete/<int:pk>/", NoteDeleteView.as_view(), name="delete_note"),
    path("api/", RetrieveUserView.as_view(), name="get_user"),
    path("logout/", CustomLogoutView.as_view(), name="logout_user"),
]
