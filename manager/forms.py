from django import forms

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def is_valid(self):
        print(self)
        users = User.objects.filter(username=self.username)
        user: User = users.first()
