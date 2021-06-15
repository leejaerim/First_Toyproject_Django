import graphene
from graphene_django import DjangoObjectType
from .models import User, Room


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        field = ("id", "title", "hasPassword", "isAvailable")
        exclude = ("password", "user")


class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = ("id", "name")


class UserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info, name):
        user = User.objects.create(name=name)
        user.save()
        return CreateUser(id=user.id, name=name)


class CreateRoom(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        password = graphene.String(required=False)
        user = graphene.Argument(UserInput)

    id = graphene.ID()

    def mutate(self, info, title, user, password=None):
        if info.context.session.exists(user.id):
            _hasPassword = 0 if password is None else 1
            _user = User(id=user.id, name=user.name)
            room = Room.objects.create(title=title,
                                       password=password,
                                       isAvailable=True,
                                       hasPassword=_hasPassword,
                                       user=_user)
            return CreateRoom(id=room.id)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info, id, name):
        user = User.objects.get(pk=id)
        user.name = name
        return UpdateUser(id=id, name=name)


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
        _hasPassword = 0 if password is None else 1
        _user = User(id=user.id, name=user.name)
        room = Room.objects.get(pk=id)
        room.title = title
        room.password = password
        room.user = _user
        room.isAvailable = isAvailable
        return UpdateRoom(id=id,
                          title=title,
                          isAvailable=isAvailable,
                          hasPassword=_hasPassword,
                          user=_user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        if user is not None:
            user.delete()
        return DeleteUser(id=id)


class DeleteRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        userId = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id, userId):
        room = Room.objects.get(pk=id)
        if room is not None and room.user.id is userId:
            room.delete()
            return DeleteRoom(id=id)
        else:
            print('delete fail')
