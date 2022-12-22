from django.urls import path

from manager import views

urlpatterns = [
    path("", views.Index.as_view()),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("choose-project/", views.ProjectSelectionView.as_view()),
    path("update-project/", views.ProjectCreationView.as_view()),
    path("leave-project/", views.ProjectLeaveView.as_view())
]
