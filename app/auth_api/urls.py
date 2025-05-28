from django.urls import path
from .views import (
    CreateUserView,
    CustomObtainTokenView,
    CustomRefreshTokenView,
    NoteListCreateView,
)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", CustomObtainTokenView.as_view(), name="login"),
    path("refresh/", CustomRefreshTokenView.as_view(), name="refresh"),
    path("api/note/", NoteListCreateView.as_view(), name="list_create_note"),
]
