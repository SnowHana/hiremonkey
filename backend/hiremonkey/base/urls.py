from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path(
        "job_seeker/<int:pk>/",
        views.job_seeker,
        name="job_seeker",
    ),
    path(
        "recruiter/<int:pk>/",
        views.recruiter,
        name="recruiter",
    ),
    path("select_profile_type/", views.select_profile_type, name="select_profile_type"),
    path("create_job_seeker/", views.create_job_seeker, name="create_job_seeker"),
    path("create_recruiter/", views.create_recruiter, name="create_recruiter"),
    path(
        "update_job_seeker/<str:pk>/", views.update_job_seeker, name="update_job_seeker"
    ),
    path(
        "delete_job_seeker/<str:pk>/", views.update_job_seeker, name="update_job_seeker"
    ),
]
