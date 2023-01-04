from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from helper import get_project_choices
from manager.models import Project, ProjectUserConnection, User, Year, ROLE_CHOICES
from .forms import LoginForm, ProjectSelectionForm, ProjectCreationForm


# Create your views here.
class Index(View):
    template = 'index.html'

    def get(self, request):
        if not isinstance(request.user, AnonymousUser):
            projects = ProjectUserConnection.objects.filter(user=request.user)
            title = ""
            description = ""
            dazs = 1
            attendance = 0
            price = 0
            other = ""
            partner = None
            permitted = True
            year = 0
            teachers = [(teacher.pk, teacher.username) for teacher in User.objects.filter(role=User.TEACHER)]
            teachers.sort(key=lambda a: a[1])
            if len(projects) > 0:
                project = projects.first().project
                if projects.first().is_partner:
                    permitted = False
                for project_connection in ProjectUserConnection.objects.filter(~Q(project=project), user__role=User.TEACHER):
                    try:
                        teachers.remove((project_connection.user.pk, project_connection.user.username))
                    except ValueError:
                        pass

                title = project.title
                description = project.description
                dazs = project.dazs
                attendance = project.attendance
                price = int(project.price)
                other = project.other
                year = project.year.year
                try:
                    partner = ProjectUserConnection.objects.filter(~Q(user=request.user), project=project).first().user.pk
                except AttributeError:
                    pass

            return render(request, self.template, context={
                "success": True,
                "teacher": request.user.role == request.user.TEACHER,
                "projects": get_project_choices(),
                "saving_succeed": request.GET.get("success") is not None and request.GET.get("success") == "1",
                "saving_failed": request.GET.get("success") is not None and request.GET.get("success") == "0",
                "error_message": "Unbekannter Fehler" if request.GET.get("error_message") is None else request.GET.get("error_message"),
                "dazs_list": Project.DAZS,
                "teachers": teachers,
                "title": title,
                "description": description,
                "dazs": dazs,
                "attendance": attendance,
                "price": price,
                "year": year,
                "years": [(year.year, year.get_year_display()) for year in Year.objects.all()],
                "other": other,
                "partner": partner,
                "permitted": permitted,
                "left_success": request.GET.get("left_success") is not None and request.GET.get("left_success") == "1",
                "left_error": request.GET.get("left_error") is not None and request.GET.get("left_error") == "1",
            })
        if request.GET.get("success") is not None:
            if request.GET.get("success") == "1":
                return render(request, self.template, context={"logged_out": True})
            elif request.GET.get("success") == "0":
                return render(request, self.template, context={"failed": True})

        return render(request, self.template)


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request=request, user=form.get_user())
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/?success=0')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/?success=1')


class ProjectSelectionView(View):
    def post(self, request):
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            ProjectUserConnection.objects.filter(user=request.user).delete()
            ProjectUserConnection.objects.create(
                user=request.user,
                priority=1,
                project=Project.objects.filter(title=form.data["first_project"]).first()
            )
            ProjectUserConnection.objects.create(
                user=request.user,
                priority=2,
                project=Project.objects.filter(title=form.data["second_project"]).first()
            )
            ProjectUserConnection.objects.create(
                user=request.user,
                priority=3,
                project=Project.objects.filter(title=form.data["third_project"]).first()
            )
            return HttpResponseRedirect("/?success=1")
        return HttpResponseRedirect("/?success=0&error_message=" + form.error_message)


class ProjectCreationView(View):
    def post(self, request):
        form = ProjectCreationForm(request.POST)
        projects = ProjectUserConnection.objects.filter(user=request.user)

        if len(projects) > 0:
            form.project = projects.first().project
            teachers = [(teacher.pk, teacher.username) for teacher in User.objects.filter(role=User.TEACHER)]
            for project_connection in ProjectUserConnection.objects.filter(~Q(project=projects.first().project), user__role=User.TEACHER):
                try:
                    teachers.remove((project_connection.user.pk, project_connection.user.username))
                except ValueError:
                    pass
            form.partner.choices = teachers
            form.year.choices = [(year.year, year.get_year_display()) for year in Year.objects.all()]
            if not projects.first().is_partner:
                form.permitted = True
        else:
            form.permitted = True
        if form.is_valid():
            if len(projects) == 0:
                ProjectUserConnection.objects.create(project=form.project, user=request.user)

            project = Project.objects.filter(pk=form.project.pk)
            if request.user.students + User.objects.get(pk=int(form.data["partner"])).students > project.first().attendance:
                project.update(
                    attendance=request.user.students + User.objects.get(pk=int(form.data["partner"])).students
                )
                return HttpResponseRedirect(
                    "/?success=0&error_message=" +
                    "Sie müssen zusammen mindestens " + str(request.user.students + User.objects.get(pk=int(form.data["partner"])).students) +
                    " Schüler betreuen, haben aber zu wenig für das Projekt ausgewählt. Die Anzahl der teilzunehmenden Schüler wurde automatisch aktualisiert."
                )
            return HttpResponseRedirect("/?success=1")
        return HttpResponseRedirect("/?success=0&error_message=" + form.error_message)


class ProjectLeaveView(View):
    def get(self, request):
        projects = ProjectUserConnection.objects.filter(user=request.user, is_partner=True)
        if len(projects) == 0:
            return HttpResponseRedirect("/?left_error=1")
        projects.delete()
        return HttpResponseRedirect("/?left_success=1")
