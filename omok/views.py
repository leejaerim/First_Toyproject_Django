from omok.models import User,Room
from django.shortcuts import render
from rest_framework import serializers ,status
from .serializers import RoomSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        request.session['user']=serializer.data['id']
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def login(self, request, *args, **kwargs):
        if request.session.has_key(uesr) :
            user_id = request.session.get('user')
            if user_id :
                user = User.objects.get(pk=user_id)
                return HttpResponse(user)
        else:
            return render(request,'login.html')


