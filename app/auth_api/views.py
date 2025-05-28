from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.response import Response


from rest_framework import generics
from rest_framework.views import APIView
from .serializers import NoteSerializer
from api.models import Note

from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests

from django.conf import settings


# Create your views here.
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        notes = Note.objects.filter(author=self.request.user)
        return notes

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDeleteView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


# Create your views here.
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomObtainTokenView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if not response.data:
            return response

        refresh_token = response.data.get("refresh")

        response.data.pop("refresh", None)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="Strict",
            secure=False,
            max_age=24 * 60 * 60,
        )

        return response


class CustomRefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error", "Refresh Token Cookie Missing"}, status=400)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"error": "No id token supplied"}, status=400)

        # Verify token
        userInfo = google_id_token.verify_oauth2_token(
            id_token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )

        email = userInfo["email"]
        # Create or get the user
        user, created = User.objects.get_or_create(
            email=email, defaults={"username": email.split("@")[0]}
        )

        # Create tokens
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        response = Response({"access": access_token}, status=200)

        response.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            httponly=True,
            secure=False,
            samesite="Strict",
            max_age=24 * 60 * 60,
        )

        return response


class CustomLogoutView(APIView):
    # Blacklist refresh token and delete cookie
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")

        except Exception:
            print(Exception)
            pass

        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({"message": "Logged out successfully"}, status=200)

        response.delete_cookie("refresh_token")

        return response
