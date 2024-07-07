from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("", views.home, name="home"),
    path(
        "user/<int:user_id>/profile/<int:profile_id>/",
        views.profile,
        name="profile",
    ),
]
