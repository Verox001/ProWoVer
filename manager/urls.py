from django.urls import path

from manager import views

urlpatterns = [
    path("", views.Index.as_view()),
    path("login/", views.LoginView.as_view()),
]
