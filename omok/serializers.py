from rest_framework import serializers
from .models import User,Room

#Room serialize object to json
# serializers.HyperlinkedModelSerializer
# serializers.ModelSerializer

class UserSerializer(serializers.ModelSerializer):
          class Meta:
             model = User
             fields = ['id','name']

class RoomSerializer(serializers.ModelSerializer):
       class Meta:
            model = Room
            fields = ['id','title','password', 'user', 'isAvailable', 'hasPassword']
            extra_kwargs = {'password': {'write_only': True, 'max_length': 4}}
