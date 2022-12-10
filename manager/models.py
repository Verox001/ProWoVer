from django.contrib.auth.models import Group, AbstractUser
from django.db import models

# Create your models here.


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

    def __str__(self):
        return self.username


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


class ProjectUserConnection(models.Model):
    project_user_connection_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    partner = models.ForeignKey(User, related_name="partner", on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
