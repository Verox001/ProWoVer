from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

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
