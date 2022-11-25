from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
__all__ = [
    "User",
    "Project"
]

# Create years as groups
for year in range(7, 11):
    group = Group.objects.get_or_create(name=str(year))


class Project(models.Model):
    YEAR7 = 1
    YEAR8 = 2
    YEAR9 = 3
    YEAR10 = 4

    ROLE_CHOICES = (
        (YEAR7, '7. Jahrgang'),
        (YEAR8, '8. Jahrgang'),
        (YEAR9, '9. Jahrgang'),
        (YEAR10, '10. Jahrgang'),
    )

    project_id = models.BigAutoField(primary_key=True)
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=8000)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    attendance = models.IntegerField()
    other = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    TEACHER = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (TEACHER, 'Lehrer'),
        (STUDENT, 'Schüler'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=STUDENT)
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.TextField(max_length=8000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
