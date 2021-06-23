from graphene_django import DjangoObjectType
from .models import Room


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        field = ("id", "title", "hasPassword", "isAvailable", "user")
        exclude = ["password"]

