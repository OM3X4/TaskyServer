from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="topics")

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic , null=True , blank=True , on_delete=models.SET_NULL , related_name="tasks")
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    expire = models.DateField()

    def __str__(self):
        return self.name
