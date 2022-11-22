# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.auth.models import AbstractUser
from django.db import models

__all__ = ["User", "Project"]


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
