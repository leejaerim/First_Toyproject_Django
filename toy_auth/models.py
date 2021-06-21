from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30, null=False)
    kakao_id = models.CharField(
        max_length=30, blank=True, null=True, unique=True)
    session_id = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    
    def __str__(self):
        return f'id: {self.id} name: {self.name}'
    
    class Meta:
        db_table = 'user'
