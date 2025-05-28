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
