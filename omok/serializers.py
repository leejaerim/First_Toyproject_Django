from rest_framework import serializers
from .models import User,Room
from django.contrib.sessions.models import Session

class UserSerializer(serializers.ModelSerializer):
          class Meta:
            model = User
            fields = ['id','name']
            

class RoomSerializer(serializers.ModelSerializer):
       class Meta:
            model = Room
            fields = ['id','title','password', 'user', 'isAvailable', 'hasPassword']
            extra_kwargs = {'password': {'write_only': True, 'max_length': 4}}

