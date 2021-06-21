from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'password', 'isAvailable', 'user')


admin.site.register(Room, RoomAdmin)
