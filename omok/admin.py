from django.contrib import admin
from .models import User, Room


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'password', 'isAvailable', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Room, RoomAdmin)
