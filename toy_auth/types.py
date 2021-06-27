import graphene
from graphene_django import DjangoObjectType
from toy_auth.models import User
from django.core.cache import cache

import os
import binascii

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("kakao_id",)

    token = graphene.String()

    def resolve_token(self, info):
        ttl = os.environ['TOKEN_EXPIRE_TIMEOUT']
        uid = self.pk
        def make_token():
            token = binascii.hexlify(os.urandom(20)).decode()
            if cache.add(token, uid, timeout=int(ttl)) :
                return token
            else :
                return make_token()
        return make_token() 
        
