from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path(
        "profile/<int:pk>/",
        views.profile,
        name="profile",
    ),
]
