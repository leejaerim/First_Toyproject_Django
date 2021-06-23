import graphene
from toy_auth.middleware import checkToken, superUserRequired
from todolist.types import TodoType
from todolist.models import Todo
from todolist.schema import CreateTodo, UpdateTodo, DeleteTodo
from omok.models import Room
from omok.schema import UpdateRoom, CreateRoom, DeleteRoom
from omok.types import RoomType
from toy_auth.models import User
from toy_auth.types import UserType
from toy_auth.schema import SignIn, SignInGuest, UpdateUser, DeleteUser


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    todos = graphene.List(TodoType)
    rooms = graphene.List(RoomType)
    room = graphene.Field(
        RoomType,
        id=graphene.ID(),
        password=graphene.String(),
    )
    
    @superUserRequired
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @checkToken
    def resolve_todos(self, info, **kwargs):
        return Todo.objects.filter(user_id = info.context.uid).all()

    @checkToken
    def resolve_rooms(self, info, **kwargs):
        return Room.objects.filter(user_id = info.context.uid).all()

    @checkToken
    def resolve_room(self, info, **kwargs):
        rid = kwargs.get('id')
        password = kwargs.get('password')
        return Room.objects.filter(pk=rid, password=password).first()
   

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
    delete_room = DeleteRoom.Field()
    
    

schema = graphene.Schema(query=Query, mutation=Mutation)
