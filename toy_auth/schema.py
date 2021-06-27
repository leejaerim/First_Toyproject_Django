import graphene
import requests
import json

from toy_auth.middleware import checkToken, superUserRequired
from toy_auth.models import User, GuestUser, KakaoUser
from toy_auth.types import UserType


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType, access_token=graphene.String(required=False))
    users = graphene.List(UserType)
    
    def resolve_user(self, info, access_token=None):
        if access_token is None :
            app_token = info.context.headers.get('authorization')
            return GuestUser.objects.signIn(token=app_token)
        else :
            profile_url = "https://kapi.kakao.com/v2/user/me"
            response = requests.request('get', profile_url, headers={
                'Authorization': 'Bearer {}'.format(access_token)
            })
            info = json.loads(response.content)
            if  info.get('id') is not None :
                return KakaoUser.objects.signIn(kakao_id=info['id'])
            else:
                raise Exception('Invalid Access Token')

    @superUserRequired
    def resolve_users(self, info, **kwargs):
        return User.objects.all()


class UpdateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    @checkToken
    def mutate(self, info, name):
        user = User.objects.get(pk=info.context.uid)
        user.name = name
        user.save()
        return UpdateUser(id=user.id, name=name)
        

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    @superUserRequired
    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUser(id=id)
    

class UserMutation(graphene.ObjectType):
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()