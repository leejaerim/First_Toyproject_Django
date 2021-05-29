from django.db import models

# Create your models here.
#django automatically gives each model the id field with primary key
class Todo(models.Model):
    text = models.CharField(max_length=200)#Not Null
    isCompleted = models.SmallIntegerField(null=True)
    def __str__(self):
        return self.text
    class Meta:
        db_table='todo'

class User(models.Model):
    user_name = models.CharField(max_length=16,default="Guest")
    #api_key = models.CharField(max_length=40, null=True)
    #reg_date = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.user_name+str(self.id)
    class Meta:
        db_table='user'
class Room(models.Model):
    title = models.CharField(max_length=30)
    password = models.CharField(null=True,max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isAvailable = models.SmallIntegerField(default=1)
    hasPassword = models.SmallIntegerField(default=0,null=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table='room'

from django.contrib import admin

admin.site.register(Room) 