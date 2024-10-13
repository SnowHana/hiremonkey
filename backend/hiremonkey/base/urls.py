from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path(
        "jobseeker/<int:pk>/",
        views.job_seeker,
        name="job_seeker",
    ),
    path(
        "recruiter/<int:pk>/",
        views.recruiter,
        name="recruiter",
    ),
    path("select_profile_type/", views.select_profile_type, name="select_profile_type"),
    path("create_jobseeker/", views.create_job_seeker, name="create_jobseeker"),
    path("create_recruiter/", views.create_recruiter, name="create_recruiter"),
    path("update_profile/<str:pk>/", views.update_profile, name="update_profile"),
    path("delete/<str:pk>/", views.delete_profile, name="delete_profile"),
    path(
        "jobseeker-autocomplete/",
        views.JobSeekerAutoComplete.as_view(),
        name="jobseeker-autocomplete",
    ),
    path(
        "skill-autocomplete/",
        views.SkillAutoComplete.as_view(create_field="name", validate_create=True),
        name="skill-autocomplete",
    ),
]
