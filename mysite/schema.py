import graphene
from todolist.types import TodoType
from todolist.models import Todo
from todolist.schema import CreateTodo, UpdateTodo, DeleteTodo
from omok.models import Room
from omok.schema import UpdateRoom, RoomType, CreateRoom
from toy_auth.models import User
from toy_auth.schema import SignIn, SignInGuest, UpdateUser, DeleteUser
from toy_auth.types import UserInput


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
    
    def resolve_todos(self, info, **kwargs):
        _user = kwargs.get('user')
        return Todo.objects.filter(user_id = _user.id).all()

    def resolve_rooms(self, info, user):
        if User.objects.isAuthenticated(info, user.id):
            return Room.objects.all()
        else:
            return Room.objects.none()

    def resolve_room(self, info, **kwargs):
        user = kwargs.get('user')
        rid = kwargs.get('id')
        password = kwargs.get('password')
        if User.objects.isAuthenticated(info, user.id):
            return Room.objects.filter(pk=rid, password=password).first()
        else:
            raise Exception("Unauthenticated Access")
 
   

class Mutation(graphene.ObjectType):
    sign_in = SignIn.Field()
    sign_in_guest = SignInGuest.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    
    

schema = graphene.Schema(query=Query, mutation=Mutation)
