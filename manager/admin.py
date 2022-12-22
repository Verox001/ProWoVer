from django.contrib import admin
from .models import User, Project, ProjectUserConnection, Year

# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectUserConnection)
admin.site.register(Year)
