from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path(
        "job-seeker/<int:pk>/",
        views.job_seeker,
        name="job-seeker",
    ),
    path(
        "recruiter/<int:pk>/",
        views.recruiter,
        name="recruiter",
    ),
]
