from django.apps import apps

from django.contrib import admin

from api.models import Project, User

admin.site.register(User)
admin.site.register(Project)

