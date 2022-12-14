from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from .forms import LoginForm


# Create your views here.
class Index(View):
    template = 'auth/login.html'

    def get(self, request):
        if request.GET.get("success") is not None:
            if request.GET.get("success") == "1":
                return render(request, self.template, context={"success": True})
            elif request.GET.get("success") == "0":
                return render(request, self.template, context={"failed": True})
            return render(request, self.template, context={"success": False})
        return render(request, self.template, context={"success": False})



class LoginView(View):
    template_name = 'auth/login.html'

    def post(self, request):
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            return HttpResponseRedirect('/?success=1')
        else:
            return HttpResponseRedirect('/?success=0')