from django.contrib.auth.models import Group, AbstractUser
from django.db import models

# Create your models here.
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

class Years(models.Model):
    year = models.PositiveBigIntegerField(choices=ROLE_CHOICES, primary_key=True)
    students = models.IntegerField()

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
    students = models.IntegerField(default=12)

    def __str__(self):
        return self.username


class Project(models.Model):
    DAZS = (
        (1, "Für Sprachlerner geeignet"),
        (2, "Nur für fortgeschrittene Sprachlerner geeignet"),
        (3, "Nicht für Sprachlerner geeignet")
    )

    project_id = models.BigAutoField(primary_key=True)
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=8000)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    attendance = models.IntegerField()
    price = models.FloatField(default=0.0)
    dazs = models.PositiveSmallIntegerField(choices=DAZS, default=1)
    other = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class ProjectUserConnection(models.Model):
    project_user_connection_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_partner = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
