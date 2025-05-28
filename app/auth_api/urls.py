from django.urls import path
from .views import (
    CreateUserView,
    CustomObtainTokenView,
    CustomRefreshTokenView,
    NoteListCreateView,
    NoteDeleteView,
    RetrieveUserView,
    CustomLogoutView,
)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", CustomObtainTokenView.as_view(), name="login"),
    path("refresh/", CustomRefreshTokenView.as_view(), name="refresh"),
    path("api/note/", NoteListCreateView.as_view(), name="list_create_note"),
    path("api/note/delete/<int:pk>/", NoteDeleteView.as_view(), name="delete_note"),
    path("api/", RetrieveUserView.as_view(), name="get_user"),
    path("logout/", CustomLogoutView.as_view(), name="logout_user"),
]
