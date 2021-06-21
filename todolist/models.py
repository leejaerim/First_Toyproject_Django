from django.db import models
from django.db.models import deletion
from toy_auth.models import User

class Todo(models.Model):
    text = models.CharField(max_length=200)  # Not Null
    isCompleted = models.SmallIntegerField(null=True)
    user = models.ForeignKey(User, on_delete=deletion.CASCADE)

    def __str__(self):
        return f'id: {self.id}, text: {self.text}, isCompleted : {self.isCompleted}'

    class Meta:
        db_table = 'todo'
