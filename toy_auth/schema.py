import graphene
import requests
import json

from django.contrib.sessions.backends.db import SessionStore
from graphene_django import DjangoObjectType
from .session import get_name
from toy_auth.models import User




class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = ("id", "name")


class CreateUser(graphene.Mutation):
    class Arguments:
        token = graphene.String()
        sid = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info, token=None, sid=None):
        if token is not None:
            profile_url = "https://kapi.kakao.com/v2/user/me"
            response = requests.request('get', profile_url, headers={
                'Authorization': 'Bearer {}'.format(token)
            })
            info = json.loads(response.content)
            print(info)
            if info['id'] is not None:
                try:
                    user = User.objects.get(kakao_id=info['id'])
                    print('registered user')
                    return CreateUser(
                        id=user.id,
                        name=user.name
                    )
                except User.DoesNotExist:
                    user = User.objects.create(
                        name=get_name(),
                        kakao_id=info['id']
                    )
                    print('new user registered!!')
                    return CreateUser(
                        id=user.id,
                        name=user.name
                    )
        else :  # when access token is not given
            s: SessionStore = info.context.session
            if s.exists(session_key=sid):
                user = User.objects.get(session_id=sid)
                print('session exist')
                return CreateUser(id=user.id, name=user.name)
            else:
                s.create()
                s.set_expiry(0)  # expire when browser is closed
                s.save()
                user = User.objects.create(name=get_name(),
                                           session_id=s.session_key)
                print('create new guest !!')
                return CreateUser(id=user.id, name=user.name)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    id = graphene.ID()
    name = graphene.String()

    def mutate(self, info, id, name):
        s: SessionStore = info.context.session
        if s.exists(id):
            s.setdefault('name', name)
            s.save()
            return UpdateUser(id=id, name=s.get('name'))


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        if user is not None:
            user.delete()
            return DeleteUser(id=id)
