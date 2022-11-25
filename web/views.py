from django.shortcuts import render
from django.views import View


# Create your views here.
class Index(View):
    template = 'index.html'

    def get(self, request):
        return render(request, self.template)
