from django.db import models

# Create your models here.
class Todo(models.Model):
    text = models.CharField(max_length=200)#Not Null
    isCompleted = models.SmallIntegerField(null=True)
    def __str__(self):
        return f'id: {self.id}, text: {self.text}, isCompleted : {self.isCompleted}'
    class Meta:
        db_table='todo'