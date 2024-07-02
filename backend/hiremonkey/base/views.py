from django.shortcuts import render


def home(request):
    return render(request, "base/home.html")


def zoo(request):
    return render(request, "base/zoo.html")
