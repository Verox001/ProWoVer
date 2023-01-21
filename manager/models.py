from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, AbstractUser
from django.db import models, IntegrityError
import csv


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


class Year(models.Model):
    year = models.PositiveBigIntegerField(choices=ROLE_CHOICES, primary_key=True)
    students = models.IntegerField()
    projects = models.IntegerField()


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


'''with open("KuK_SuS_Einsatz.csv", "r") as f:
    reader = csv.reader(f)
    for line in reader:
        try:
            User.objects.get_or_create(username=line[0], students=int(line[1]), password=make_password(line[2]), role=2)
        except IntegrityError: pass'''


class Project(models.Model):
    DAZS = (
        (1, "Für Sprachlerner geeignet"),
        (2, "Nur für fortgeschrittene Sprachlerner geeignet"),
        (3, "Nicht für Sprachlerner geeignet")
    )

    project_id = models.BigAutoField(primary_key=True)
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=8000)
    attendance = models.IntegerField()
    price = models.FloatField(default=0.0)
    dazs = models.PositiveSmallIntegerField(choices=DAZS, default=1)
    other = models.TextField(max_length=255, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=Year.objects.values().first())

    def __str__(self):
        return self.year.get_year_display() + ": " + ProjectUserConnection.objects.filter(project=self).first().user.username + ", " + ProjectUserConnection.objects.filter(project=self)[1].user.username


class ProjectUserConnection(models.Model):
    first = 1
    second = 2
    third = 3

    PRIORITY = (
        (first, 'Erstwunsch'),
        (second, 'Zweitwunsch'),
        (third, 'Drittwunsch'),
    )
    project_user_connection_id = models.BigAutoField(primary_key=True)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_partner = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
