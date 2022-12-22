from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from helper import get_project_choices
from manager.models import User, Project, ProjectUserConnection


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    _user: User = None

    def is_valid(self):
        self._user = authenticate(username=self.data["username"], password=self.data["password"])
        return self._user is not None

    def get_user(self):
        if self._user is None:
            raise ObjectDoesNotExist("Use is_valid before, trying getting the user.")
        return self._user


class ProjectSelectionForm(forms.Form):
    first_project = forms.Select(choices=get_project_choices())
    second_project = forms.Select(choices=get_project_choices())
    third_project = forms.Select(choices=get_project_choices())
    error_message = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_project = forms.Select(choices=get_project_choices())
        self.second_project = forms.Select(choices=get_project_choices())
        self.third_project = forms.Select(choices=get_project_choices())

    def is_valid(self):
        if "first_project" not in self.data or "second_project" not in self.data or "third_project" not in self.data:
            self.error_message = "Du musst alle Projektwünsche angeben."
            return False

        wishes = [
            self.data["first_project"],
            self.data["second_project"],
            self.data["third_project"],
        ]
        if len(wishes) != len(set(wishes)):
            self.error_message = "Du darfst keine doppelten Projektwünsche angeben."
            return False

        return True


class ProjectCreationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}))
    dazs = forms.Select(choices=Project.DAZS)
    attendance = forms.NumberInput()
    price = forms.FloatField()
    other = forms.CharField(widget=forms.Textarea(attrs={"rows": "2"}))
    partner = forms.Select()
    error_message = ""
    permitted = False
    project = None

    def is_valid(self):
        try:
            old_partner = None
            if self.project is None:
                self.project = Project.objects.create(
                    title=self.data["title"],
                    description=self.data["description"],
                    dazs=int(self.data["dazs"]),
                    attendance=int(self.data["attendance"]),
                    price=float(self.data["price"]),
                    other=self.data["other"]
                )
            else:
                old_partners = ProjectUserConnection.objects.filter(project=self.project, is_partner=True)
                if len(old_partners) > 0:
                    old_partner = old_partners.first().user
                self.project = Project.objects.update_or_create(
                    pk=self.project.pk,
                    title=self.data["title"],
                    description=self.data["description"],
                    dazs=int(self.data["dazs"]),
                    attendance=int(self.data["attendance"]),
                    price=float(self.data["price"]),
                    other=self.data["other"]
                )[0]
            if self.permitted:
                if "partner" in self.data:
                    partner = User.objects.get(pk=int(self.data["partner"]))
                    if old_partner is not None and partner.pk != old_partner.pk:
                        ProjectUserConnection.objects.filter(project=self.project, user=old_partner).delete()
                    ProjectUserConnection.objects.create(project=self.project, user=partner, is_partner=True)
                else:
                    if old_partner is not None:
                        ProjectUserConnection.objects.filter(project=self.project, user=old_partner).delete()
            return True
        except KeyError:
            self.error_message = "Eines der Felder wurde nicht korrekt angegeben."
            return False
        except ObjectDoesNotExist:
            self.error_message = "Dieser Lehrer konnte nicht gefunden werden."
            return False
