from rest_framework import serializers
from .models import User,Room

#Room serialize object to json
# serializers.HyperlinkedModelSerializer
# serializers.ModelSerializer

class UserSerializer(serializers.ModelSerializer):
          class Meta:
             model = User
             fields = ['id','user_name']

class RoomSerializer(serializers.ModelSerializer):
       class Meta:
            model = Room
            fields = ['id','title', 'user', 'isAvailable', 'hasPassword']
