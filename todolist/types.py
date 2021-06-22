from graphene_django import DjangoObjectType
from .models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        field = ("id", "text", "isCompleted", "user")
