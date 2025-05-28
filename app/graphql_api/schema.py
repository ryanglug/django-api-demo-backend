import graphene
from graphene_django import DjangoObjectType
from api.models import Note
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class Query(graphene.ObjectType):
    notes = graphene.List(NoteType, page=graphene.Int(), per_page=graphene.Int())
    user_notes = graphene.List(NoteType, page=graphene.Int(), per_page=graphene.Int())

    def resolve_notes(self, info, page=1, per_page=5):
        paginator = Paginator(Note.objects.all(), per_page)

        return paginator.page(page).object_list

    @login_required
    def resolve_user_notes(self, info, page=1, per_page=5):
        user = info.context.user
        print("user", user)
        notes = Note.objects.filter(author=user)

        paginator = Paginator(notes, per_page)
        return paginator.page(page).object_list


class Mutation(graphene.ObjectType):
    # Add JWT authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
