import graphene
from graphene_django import DjangoObjectType
from .models import Room
from toy_auth.models import User
from toy_auth.schema import UserInput, UserType


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        field = ("id", "title", "hasPassword", "isAvailable", "user")
        exclude = ["password"]


class CreateRoom(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        password = graphene.String(required=False)
        user = graphene.Argument(UserInput)

    id = graphene.ID()

    def mutate(self, info, title, user, password=None):
        try:
            _user = User.objects.get(id=user.id)
            _hasPassword = 0 if password is None else 1
            room = Room.objects.create(title=title,
                                       password=password,
                                       isAvailable=True,
                                       hasPassword=_hasPassword,
                                       user=_user)
            return CreateRoom(id=room.id)
        except User.DoesNotExist:
            raise Exception('Unauthenticated User Access')


class UpdateRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        password = graphene.String(required=False)
        user = graphene.Argument(UserInput)
        isAvailable = graphene.Boolean()

    id = graphene.ID()
    title = graphene.String()
    isAvailable = graphene.Boolean()
    hasPassword = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, id, title, user, isAvailable, password=None):
        try:
            room = Room.objects.get(pk=id)
            if room.user.id is int(user.id):
                room.title = title
                room.password = password
                room.isAvailable = isAvailable
                room.save()
                _hasPassword = 0 if password is None else 1

                return UpdateRoom(id=id,
                          title=title,
                          isAvailable=isAvailable,
                          hasPassword=_hasPassword,
                          user= user)
            else:
                raise Exception('Unauthenticated User Access')
        except Room.DoesNotExist:
            raise Exception('Invalid Object')
      
