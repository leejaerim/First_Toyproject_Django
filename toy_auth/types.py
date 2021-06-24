from graphene_django import DjangoObjectType
from toy_auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = ("id", "name")

