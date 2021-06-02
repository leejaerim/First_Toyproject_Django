from .models import Todo
from .serializers import TodoSerializer
from rest_framework import viewsets
from rest_framework import permissions

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
