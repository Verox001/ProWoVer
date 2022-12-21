from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from .forms import LoginForm


# Create your views here.
class Index(View):
    template = 'auth/login.html'

    def get(self, request):
        print(request.user)
        if request.user != AnonymousUser:
            return render(request, self.template, context={"success": True, "teacher": request.user.role == request.user.TEACHER})
        if request.GET.get("success") is not None:
            if request.GET.get("success") == "1":
                return render(request, self.template, context={"success": True, "teacher": request.user.role == request.user.TEACHER})
            elif request.GET.get("success") == "0":
                return render(request, self.template, context={"failed": True})



class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request=request, user=form.get_user())
            return HttpResponseRedirect('/?success=1')
        else:
            return HttpResponseRedirect('/?success=0')