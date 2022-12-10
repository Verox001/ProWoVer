from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from .forms import LoginForm


# Create your views here.
class Index(View):
    template = 'auth/login.html'

    def get(self, request):
        return render(request, self.template)


class LoginView(View):
    template_name = 'auth/login.html'

    def post(self, request):
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')