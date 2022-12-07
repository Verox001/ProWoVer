from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
__all__ = [
    "User",
    "Project"
]

# Create years as groups
group = Group.objects.get_or_create(name="5/6")
for year in range(7, 13):
    group = Group.objects.get_or_create(name=str(year))


class Project(models.Model):
    YEAR56 = 1
    YEAR7 = 2
    YEAR8 = 3
    YEAR9 = 4
    YEAR10 = 5
    YEAR11 = 6
    YEAR12 = 7

    ROLE_CHOICES = (
        (YEAR56, '5./6. Jahrgang'),
        (YEAR7, '7. Jahrgang'),
        (YEAR8, '8. Jahrgang'),
        (YEAR9, '9. Jahrgang'),
        (YEAR10, '10. Jahrgang'),
        (YEAR11, '11. Jahrgang'),
        (YEAR12, '12. Jahrgang'),
    )

    project_id = models.BigAutoField(primary_key=True)
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=8000)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    attendance = models.IntegerField()
    price = models.FloatField(default=0.0)
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
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    password = models.TextField(max_length=8000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
