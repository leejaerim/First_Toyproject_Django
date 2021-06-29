from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet
import random


#reference : https://github.com/purry03/Username-Generator
#generate random username
def generate_name()->str:
    with open('nouns.txt', 'r') as infile:
        nouns = infile.read().strip(' \n').split('\n')
    with open('adjectives.txt', 'r') as infile:
        adjectives = infile.read().strip(' \n').split('\n')

    word1 = random.choice(adjectives)
    word2 = random.choice(nouns)
    word1 =word1.title()
    word2 =word2.title()
    
    username = '{}{}'.format(word1, word2)
    return username


class User(models.Model):
    GUEST = 0
    KAKAO = 1
    USER_CHOICES = [
        (GUEST, 'Guest'),
        (KAKAO, 'Kakao')
    ]

    user_type = models.IntegerField(choices=USER_CHOICES, default = GUEST)
    name = models.CharField(max_length=30, null=False)
    kakao_id = models.CharField(
        max_length=30, blank=True, null=True, unique=True)
    first_created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        ordering = ['user_type']
        db_table = 'toy_user'


class KakaoUserManager(models.Manager):
    def get_queryset(self) -> QuerySet[User]:
        return super(KakaoUserManager, self).get_queryset().filter(user_type=User.KAKAO)

    def create(self, *args, **kwargs) -> User:
        kwargs.update({
            'user_type': User.KAKAO,
            'name' : generate_name()
        })
        return super(KakaoUserManager, self).create(*args, **kwargs)

    def get(self, *args, **kwargs) -> User:
        kwargs.update({'user_type': User.KAKAO})
        return super(KakaoUserManager, self).get(*args, **kwargs)

    def signIn(self, **kwargs) -> User:
        kakao_id = kwargs.get('kakao_id')
        try:
            user = self.get(kakao_id=kakao_id)
            print('user sign in!!')
            return user
        except User.DoesNotExist:
            user = self.create(
                name= User.objects.get_name(),
                kakao_id=kakao_id,
            )
            print('new user registered through kakao!!')
            return user
        

class GuestUserManager(models.Manager):
    def get_queryset(self) -> QuerySet[User]:
        return super(GuestUserManager, self).get_queryset().filter(user_type=User.GUEST)

    def create(self, *args, **kwargs) -> User:
        kwargs.update({
            'user_type': User.GUEST,
            'name' : generate_name()
        })
        return super(GuestUserManager, self).create(*args, **kwargs)

    def get(self, *args, **kwargs) -> User:
        kwargs.update({'user_type': User.GUEST})
        return super(GuestUserManager, self).get(*args, **kwargs)

    def signIn(self, **kwargs) -> User:
        token = kwargs.get('token')
        uid = cache.get(token, default=None) 
        if uid is not None :
            user = self.get(pk = uid)
            print('guest sign in!!')
            return user
        else :
            user = self.create()
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






