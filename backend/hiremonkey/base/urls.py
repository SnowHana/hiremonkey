from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path('user-mode-selection/', views.user_mode_selection, name='user_mode_selection'),
    path(
        "jobseeker/<slug:slug>/",
        views.jobseeker,
        name="jobseeker",
    ),
    path(
        "recruiter/<slug:slug>/",
        views.recruiter,
        name="recruiter",
    ),
    path("select_profile_type/", views.select_profile_type, name="select_profile_type"),
    path("create_jobseeker/", views.create_jobseeker, name="create_jobseeker"),
    path("create_recruiter/", views.create_recruiter, name="create_recruiter"),
    path('update/<str:profile_type>/<slug:slug>/', views.update_profile, name='update_profile'),
    path("delete/<str:profile_type>/<slug:slug>/", views.delete_profile, name="delete_profile"),
    path(
        "skill-autocomplete/",
        views.SkillAutoComplete.as_view(create_field="title", validate_create=True),
        name="skill-autocomplete",
    ),
]
