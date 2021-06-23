from toy_auth.middleware import checkToken, passTokenTest, superUserRequired
import graphene
import requests
import json

from toy_auth.models import User, GuestUser, KakaoUser


class SignIn(graphene.Mutation):
    class Arguments:
        token = graphene.String()

    id = graphene.ID()
    name = graphene.String()
    token = graphene.String()

    def mutate(self, info, token):
        profile_url = "https://kapi.kakao.com/v2/user/me"
        response = requests.request('get', profile_url, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        info = json.loads(response.content)
        print(info)
        if  info.get('id') is not None :
            user = KakaoUser.objects.signIn(kakao_id=info['id'])
            return SignIn(
                id=user.id,
                name=user.name,
                token=user.token
            )
        else:
            raise Exception('Invalid Access Token')


class SignInGuest(graphene.Mutation):

    id = graphene.ID()
    name = graphene.String()
    token = graphene.String()

    def mutate(self, info):
        token = info.context.headers.get('authorization')
        user = GuestUser.objects.signIn(token=token)
        return SignInGuest(id=user.id, name=user.name, token=user.token)


class UpdateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    @checkToken
    def mutate(self, info, name):
        print('user id is')
        print(info.context.uid)
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