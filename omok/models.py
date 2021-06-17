from django.db import models


class User(models.Model):
    name = models.CharField(max_length=16, default="Guest")
    #reg_date = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        db_table = 'user'


class Room(models.Model):
    title = models.CharField(max_length=30)
    password = models.CharField(null=True, max_length=12)
    isAvailable = models.SmallIntegerField(default=1)
    hasPassword = models.SmallIntegerField(default=0, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'room'
