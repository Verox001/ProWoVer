from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.Index.as_view())
]