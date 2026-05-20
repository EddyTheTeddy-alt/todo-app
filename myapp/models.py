from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    due_date = models.DateField()
    description = models.CharField(max_length=200)