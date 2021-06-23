import graphene
from graphene_django import DjangoObjectType
from toy_auth.models import User

class UserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = ("id", "name")

