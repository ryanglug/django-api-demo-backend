from rest_framework import generics

from .models import Note
from .pagination import CustomPageSizePagination
from .serializers import NoteSerializer


# Create your views here.
class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Note.objects.all()
