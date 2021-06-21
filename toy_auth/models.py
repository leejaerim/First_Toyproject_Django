from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30, null=False)
    kakao_id = models.CharField(
        max_length=30, blank=True, null=True, unique=True)
    session_id = models.CharField(
        max_length=30, blank=True, null=True, unique=True)
    
    class Meta:
        db_table = 'user'
