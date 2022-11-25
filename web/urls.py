from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    path("", views.Index.as_view()),
]
