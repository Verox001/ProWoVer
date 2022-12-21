from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from helper import get_project_choices
from .models import User


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

class ProjectForm(forms.Form):
    first_project = forms.Select(choices=get_project_choices())
    second_project = forms.Select(choices=get_project_choices())
    third_project = forms.Select(choices=get_project_choices())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_project = forms.Select(choices=get_project_choices())
        self.second_project = forms.Select(choices=get_project_choices())
        self.third_project = forms.Select(choices=get_project_choices())
