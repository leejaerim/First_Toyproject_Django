import graphene
from graphene_django.debug import DjangoDebug
from todolist.models import Todo
from todolist.schema import TodoType, CreateTodo, UpdateTodo, DeleteTodo
from omok.models import User, Room
from omok.schema import UpdateRoom, UpdateUser, UserType, RoomType, CreateRoom, DeleteRoom


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType, id=graphene.ID())
    #users = graphene.List(UserType)
    #user = graphene.Field(UserType, id=graphene.ID())
    rooms = graphene.List(RoomType)
    room = graphene.Field(RoomType,
                          id=graphene.ID(),
                          password=graphene.String(),
                          user_id=graphene.String())
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_rooms(self, info, **kwargs):
        return Room.objects.all()

    def resolve_room(self, info, **kwargs):
        uid = kwargs.get('user_id')
        rid = kwargs.get('id')
        password = kwargs.get('password')

        if info.context.session.exists(uid):
            try:
                return Room.objects.get(pk=rid, password=password)
            except Room.DoesNotExist:
                return Room.objects.none()
            
        else:
            return Room.objects.none()

    def resolve_todos(self, info, **kwargs): 
        return Todo.objects.all()

    def resolve_todo(self, info, id):
        return Todo.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    update_user = UpdateUser.Field()
    delete_room = DeleteRoom.Field()
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
