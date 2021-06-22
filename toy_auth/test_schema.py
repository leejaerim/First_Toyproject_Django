import graphene
from toy_auth.models import User, isAuthenticated
from toy_auth.schema import SignIn, SignInGuest, UpdateUser, DeleteUser
from toy_auth.types import UserType, UserInput


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id = graphene.ID()
    )

    def resolve_user(self, info, **kwargs):
        uid = kwargs.get('id') 
        if isAuthenticated(headers = info.context['headers'], uid=uid) :
            return User.objects.get(pk=uid)
        else:
            raise Exception('Unauthenticated Access')


class Mutation(graphene.ObjectType):
    sign_in = SignIn.Field()
    sign_in_guest = SignInGuest.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
 
schema = graphene.Schema(query=Query, mutation=Mutation)
