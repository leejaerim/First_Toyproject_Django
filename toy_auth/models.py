from django.contrib.sessions.backends.db import SessionStore
from django.db import models
from django.db.models import QuerySet
from django.db.models.query import EmptyQuerySet

import json
import random


class User(models.Model):
    USER_CHOICES = [
        (0, 'Guest'),
        (1, 'Kakao')
    ]

    user_type = models.IntegerField(choices=USER_CHOICES, default=0)
    name = models.CharField(max_length=30, null=False)
    kakao_id = models.CharField(
        max_length=30, blank=True, null=True, unique=True)
    token = models.CharField(max_length=100, null=False)
    first_created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        ordering = ['user_type']
        db_table = 'toy_auth_user'


class KakaoUserManager(models.Manager):
    def get_queryset(self) -> QuerySet[User]:
        return super(KakaoUserManager, self).get_queryset().filter(user_type=1)

    def signIn(self, **kwargs) -> User:
        kakao_id = kwargs.get('kakao_id')
        token = kwargs.get('token')
        try:
            user = KakaoUser.objects.get(kakao_id=kakao_id)
            user.token = token
            user.save()
            print('user sign in!!')
            return user
        except User.DoesNotExist:
            user = KakaoUser.objects.create(
                name= get_name(),
                kakao_id=kakao_id,
                token = token
            )
            print('new user registered!!')
            return user
        

class GuestUserManager(models.Manager):
    def get_queryset(self) -> QuerySet[User]:
        return super(GuestUserManager, self).get_queryset().filter(user_type=0)

    def signIn(self, **kwargs) -> User:
        token = kwargs.get('token')
        s = SessionStore()
        if s.exists(session_key=token) :
            user = GuestUser.objects.get(token = token)
            print('guest exists!!')
            return user
        else :
            s.create()
            s.set_expiry(0)
            s.save()
            user = GuestUser.objects.create(
                name= get_name(),
                token = s.session_key,
            )
            print('new guest created!!')
            return user


class KakaoUser(User):
    class Meta:
        proxy = True

    objects = KakaoUserManager()


class GuestUser(User):
    class Meta:
        proxy = True

    objects = GuestUserManager()



def get_name():
    # get user input
    # read word lists
    with open('nouns.txt', 'r') as infile:
        nouns = infile.read().strip(' \n').split('\n')
    with open('adjectives.txt', 'r') as infile:
        adjectives = infile.read().strip(' \n').split('\n')
    # generate usernames
    # construct username
    word1 = random.choice(adjectives)
    word2 = random.choice(nouns)
    #else make and print the username
    #captilaize first letter
    word1 =word1.title()
    word2 =word2.title()
    username = '{}{}'.format(word1, word2)
    return username


def isAuthenticated(headers, uid) -> bool:
    token = headers.get('authorization')
    if token is None:
        return False
    else:
        return User.objects.filter(pk=uid, token=token) is not EmptyQuerySet