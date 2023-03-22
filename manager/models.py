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

YEARS = (
    (YEAR56, '5./6. Jahrgang'),
    (YEAR7, '7. Jahrgang'),
    (YEAR8, '8. Jahrgang'),
    (YEAR9, '9. Jahrgang'),
    (YEAR10, '10. Jahrgang'),
    (YEAR11, '11. Jahrgang'),
    (YEAR12, '12. Jahrgang'),
)


class Year(models.Model):
    year = models.PositiveBigIntegerField(choices=YEARS, primary_key=True)
    students = models.IntegerField()
    projects = models.IntegerField()


class User(AbstractUser):
    TEACHER = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (TEACHER, 'Lehrer'),
        (STUDENT, 'Schüler'),
    )

    DAZS = (
        (1, "Sprachlerner"),
        (2, "Fortgeschrittener Sprachlerner"),
        (3, "Kein Sprachlerner")
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=STUDENT)
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    password = models.TextField(max_length=8000)
    students = models.IntegerField(default=12)
    year = models.PositiveBigIntegerField(choices=YEARS, blank=True, null=True)
    dazs = models.PositiveSmallIntegerField(choices=DAZS, default=3)

    def __str__(self):
        return self.username


'''with open("SuS.csv", "r", encoding="unicode_escape") as f:
    reader = csv.reader(f)
    for line in reader:
        dazs = 3
        if line[4].startswith("DaZ"):
            if line[4].split("DaZ")[0] == "1":
                dazs = 1
            else:
                dazs = 2
        try:
            User.objects.get_or_create(
                first_name=line[1],
                last_name=line[0],
                username=line[2],
                password=make_password(line[3]),
                dazs=dazs,
                role=2,
                year=(dazs == 3) if Year.objects.get(year=int(line[4])) else Year.objects.get(year=2)
            )
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
        return self.year.get_year_display() + ": " + ProjectUserConnection.objects.filter(project=self).first().user.username + ", " + ProjectUserConnection.objects.filter(project=self)[1].user.username + "; " + str(self.attendance) + " Schüler"


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
