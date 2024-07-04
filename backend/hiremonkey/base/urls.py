from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("zoo/", views.zoo, name="zoo"),
    # path("ape/<str:pk>/", views.ape, name="ape"),
    # path("user/<int:user_id>/", views.user_detail, name="user_detail"),
    path(
        "user/<int:user_id>/profile/<int:profile_id>/",
        views.profile,
        name="profile",
    ),
]
