from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user_type', 'kakao_id', 'first_created', 'last_modified']

admin.site.register(User, UserAdmin)
