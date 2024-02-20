from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    isDone = models.BooleanField(default=False)
    date = models.DateTimeField('date publised')

    def __str__(self):
        return self.title
