import graphene
from graphene_django import DjangoObjectType
from api.models import Note
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class NoteConnection(graphene.ObjectType):
    notes = graphene.List(NoteType)
    has_next = graphene.Boolean()


class Query(graphene.ObjectType):
    notes = graphene.Field(NoteConnection, page=graphene.Int(), per_page=graphene.Int())
    user_notes = graphene.Field(
        NoteConnection, page=graphene.Int(), per_page=graphene.Int()
    )

    def resolve_notes(self, info, page=1, per_page=10):
        paginator = Paginator(Note.objects.all(), per_page)
        current_page = paginator.get_page(page)

        return NoteConnection(
            notes=current_page.object_list, has_next=current_page.has_next()
        )

    @login_required
    def resolve_user_notes(self, info, page=1, per_page=10):
        user = info.context.user
        notes = Note.objects.filter(author=user)

        paginator = Paginator(notes, per_page)
        current_page = paginator.get_page(page)
        return NoteConnection(
            notes=current_page.object_list, has_next=current_page.has_next()
        )


class CreateNoteMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    note = graphene.Field(NoteType)

    @login_required
    def mutate(self, info, title, content):
        user = info.context.user
        note = Note.objects.create(title=title, content=content, author=user)

        return CreateNoteMutation(note=note)  # type: ignore


class DeleteNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        try:
            note = Note.objects.get(id=id)

            note.delete()

            return DeleteNoteMutation(success=True)  # type: ignore

        except Note.DoesNotExist:
            raise Exception("Note not found")


class Mutation(graphene.ObjectType):
    create_note = CreateNoteMutation.Field()
    delete_note = DeleteNoteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
