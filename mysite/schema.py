import graphene
from todolist.models import Todo
from todolist.schema import TodoType, CreateTodo, UpdateTodo, DeleteTodo
from omok.models import Room
from omok.schema import UpdateRoom, RoomType, CreateRoom
from toy_auth.models import User
from toy_auth.schema import CreateUser, UpdateUser, DeleteUser, UserInput, UserType


class Query(graphene.ObjectType):
    todos = graphene.List(
        TodoType,
        user = graphene.Argument(UserInput)
    )
    rooms = graphene.List(
        RoomType,
        user = graphene.Argument(UserInput)
    )
    room = graphene.Field(
        RoomType,
        id=graphene.ID(),
        password=graphene.String(),
        user=graphene.Argument(UserInput),
    )

    def resolve_rooms(self, info, user):
        try:
            user = User.objects.get(pk=user.id)
            return Room.objects.all()
        except User.DoesNotExist:
            return Room.objects.none()

    def resolve_room(self, info, **kwargs):
        user = kwargs.get('user')
        rid = kwargs.get('id')
        password = kwargs.get('password')
        try:
            user = User.objects.get(pk=user.id)
            return Room.objects.get(pk=rid, password=password)
        except User.DoesNotExist:
            return Room.objects.none()
        except Room.DoesNotExist:
            return Room.objects.none()
 
    def resolve_todos(self, info, **kwargs):
        _user = kwargs.get('user')
        return Todo.objects.filter(user_id = _user.id).all()


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
