from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import NoteSerializer, UserSerializer
from .models import Note
from django.contrib.auth.models import User

# Create your views here.
class NoteListView(generics.ListAPIView):
  serializer_class = NoteSerializer
  permission_classes = [permissions.AllowAny]
  queryset = Note.objects.all()

  def get_queryset(self):
    return Note.objects.all()


