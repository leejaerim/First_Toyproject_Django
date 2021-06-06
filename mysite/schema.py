import graphene
from graphene_django.debug import DjangoDebug
from graphene_django import DjangoObjectType
from todolist.models import Todo
from omok.models import User, Room


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        field = ("id", "text", "isCompleted")


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        field = ("id", "title", "hasPassword", "isAvailable")
        exclude_fields = [
            'password',  #it worked          
        ]


class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = ("id", "name")


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType, id=graphene.ID())
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())
    rooms = graphene.List(RoomType)
    room = graphene.Field(RoomType, id=graphene.ID())
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_rooms(self, info, **kwargs):
        return Room.objects.all()

    def resolve_room(self, info, id):
        return Room.objects.get(pk=id)

    def resolve_todos(self, info, **kwargs):
        return Todo.objects.all()

    def resolve_todo(self, info, id):
        return Todo.objects.get(pk=id)


class CreateTodo(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        isCompleted = graphene.Int(required=False)

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Int()

    def mutate(self, info, text, isCompleted=None):
        todo = Todo.objects.create(text=text, isCompleted=isCompleted)
        todo.save()
        return CreateTodo(id=todo.id, text= text, isCompleted=isCompleted)


class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()
        isCompleted = graphene.Int()

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Int()

    def mutate(self, info, id, text=None, isCompleted=None):
        todo = Todo.objects.get(pk=id)
        todo.text = text if text is not None else todo.text
        todo.isCompleted = isCompleted if isCompleted is not None else todo.isCompleted
        todo.save()
        return UpdateTodo(id=id, text = text, isCompleted=isCompleted)


class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        todo = Todo.objects.get(pk=id)
        if todo is not None:
            todo.delete()
        return DeleteTodo(id=id)



class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
