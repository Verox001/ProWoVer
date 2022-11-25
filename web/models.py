from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
__all__ = [
    "User",
    "Project"
]


class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.TextField(max_length=8000)
    isTeacher = models.BooleanField(default=False)


class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    year = models.IntegerField()
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=8000)
    target_group = models.TextField(max_length=255)
    attendance = models.IntegerField()
    other = models.TextField(max_length=255)
