from rest_framework import generics
from .serializers import NoteSerializer
from .models import Note


# Create your views here.
class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        return Note.objects.all()
