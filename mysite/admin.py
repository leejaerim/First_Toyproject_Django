from django.contrib import admin
from omok.models import Room, User
from todolist.models import Todo

admin.site.register(Room)
admin.site.register(User)
admin.site.register(Todo)