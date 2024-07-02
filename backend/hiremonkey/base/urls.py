from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("zoo/", views.zoo, name="zoo"),
    path("ape/<str:pk>/", views.ape, name="ape"),
]
