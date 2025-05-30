from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ["title", "content", "author", "created_at"]
