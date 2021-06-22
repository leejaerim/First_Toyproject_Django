import graphene
import requests
import json

from toy_auth.models import User, GuestUser, KakaoUser


class SignIn(graphene.Mutation):

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info):
        token = info.context.headers.get('authorization')
        profile_url = "https://kapi.kakao.com/v2/user/me"
        response = requests.request('get', profile_url, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        info = json.loads(response.content)
        if info['id'] is not None:
            user = KakaoUser.objects.signIn(kakao_id=info['id'], token=token)
            return SignIn(
                id=user.id,
                name=user.name
            )
        else:
            raise Exception('Invalid Access Token')


class SignInGuest(graphene.Mutation):

    id = graphene.ID()
    name = graphene.String()
    sid = graphene.String()

    def mutate(self, info):
        token = info.context.headers.get('authorization')
        user = GuestUser.objects.signIn(token=token)
        return SignInGuest(id=user.id, name=user.name, sid=user.token)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info, id, name):
        user = User.objects.fromToken(info, id)
        if user is not None:
            user.name = name
            user.save()
            return UpdateUser(id=id, name=name)
        else:
            raise Exception('Unauthenticated Access')


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        user = User.objects.fromToken(info, id)
        if user is not None:
            user.delete()
            return DeleteUser(id=id)
        else:
            raise Exception('Unauthenticated Access')
