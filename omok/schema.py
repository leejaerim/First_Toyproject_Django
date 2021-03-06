from omok.types import RoomType
import graphene
from .models import Room
from toy_auth.models import User
from toy_auth.middleware import checkToken, superUserRequired


class OmokQuery(graphene.ObjectType):
    rooms = graphene.List(RoomType)
    room = graphene.Field(
        RoomType,
        id=graphene.ID(),
        password=graphene.String(),
    )

    @checkToken
    def resolve_rooms(self, info, **kwargs):
        return Room.objects.all()

    @checkToken
    def resolve_room(self, info, **kwargs):
        rid = kwargs.get('id')
        password = kwargs.get('password')
        return Room.objects.filter(pk=rid, password=password).first()


class CreateRoom(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        password = graphene.String(required=False)
 
    id = graphene.ID()

    @checkToken
    def mutate(self, info, title, password=None):
        user = User.objects.get(id=info.context.uid)
        _hasPassword = 0 if password is None else 1
        room = Room.objects.create(title=title,
                                    password=password,
                                    isAvailable=True,
                                    hasPassword=_hasPassword,
                                    user=user)
        return CreateRoom(id=room.id)
        

class UpdateRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        password = graphene.String(required=False)
        isAvailable = graphene.Boolean()

    id = graphene.ID()
    title = graphene.String()
    isAvailable = graphene.Boolean()
    hasPassword = graphene.Boolean()
    
    def mutate(self, info, id, title, isAvailable, password=None):
        try:
            room = Room.objects.get(pk=id)
            if room.user.id is info.context.uid:
                room.title = title
                room.password = password
                room.isAvailable = isAvailable
                room.save()
                _hasPassword = 0 if password is None else 1

                return UpdateRoom(id=id,
                          title=title,
                          isAvailable=isAvailable,
                          hasPassword=_hasPassword)
        except Room.DoesNotExist:
            raise Exception('Invalid Room Object')
      

class DeleteRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    @superUserRequired
    def mutate(self, info, id):
        try:
            user = Room.objects.get(pk=id)
            user.delete()
            return DeleteRoom(id=id)
        except Room.DoesNotExist:
            raise Exception('Invalid Room Object')


class OmokMutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    delete_room = DeleteRoom.Field()
    