from omok.models import User,Room
<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
=======
from django.shortcuts import render
>>>>>>> cc895bd558e676669571e53c105dc646158ddc83
from rest_framework import serializers ,status
from .serializers import RoomSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
<<<<<<< HEAD
from omok.permissions import IsOwnerOrReadOnly
=======
>>>>>>> cc895bd558e676669571e53c105dc646158ddc83

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
<<<<<<< HEAD
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
=======
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
>>>>>>> cc895bd558e676669571e53c105dc646158ddc83
    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
<<<<<<< HEAD
    
        
=======
>>>>>>> cc895bd558e676669571e53c105dc646158ddc83

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
<<<<<<< HEAD
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
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

=======
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
>>>>>>> cc895bd558e676669571e53c105dc646158ddc83
    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
<<<<<<< HEAD
    def login(self, request, *args, **kwargs):
        user_id = request.session.get('user')
        if user_id :
            user = User.objects.get(pk=user_id)
            return HttpResponse(user)
        else:
            return render(request,'login.html')
    
=======
>>>>>>> cc895bd558e676669571e53c105dc646158ddc83



# def room_list(request):

#     if request.method == 'GET':
#         query_set = Room.objects.all()
#         serializer = RoomSerializer(query_set,many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = RoomSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data , status=201)
#         return JsonResponse(serializer.errors , status=400)

# def room(request, pk):
#     obj = Room.objects.get(pk=pk)

#     if request.method =='GET':
#         serializer = RoomSerializer(obj)
#         return JsonResponse(serializer.data,safe=False)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = RoomSerializer(obj,data =data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.errors,status=400)
#     elif request.method == 'DELETE':
#         obj.delelte()
#         return HttpResponse(status=204)

