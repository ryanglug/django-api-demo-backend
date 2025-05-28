import graphene
from graphene_django import DjangoObjectType
from api.models import Note
from django.core.paginator import Paginator
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class Query(graphene.ObjectType):
    notes = graphene.List(NoteType, page=graphene.Int(), per_page=graphene.Int())

    def resolve_notes(self, info, page=1, per_page=5):
        paginator = Paginator(Note.objects.all(), per_page)

        return paginator.page(page).object_list


# class Mutation(graphene.ObjectType):


schema = graphene.Schema(query=Query)
