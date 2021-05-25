from rest_framework import serializers
from .models import Room, User

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
            fields = ['id','room_title','room_password', 'user_one', 'isAvailable']
