from django.shortcuts import get_object_or_404, render
from .models import Profile, User

# For testing. changer it alter
apes = [{"id": 1, "name": "azir"}, {"id": 2, "name": "jax"}, {"id": 3, "name": "kaisa"}]


def home(request):
    context = {"apes": apes}
    return render(request, "base/home.html", context)


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profiles = user.profiles.all()
    return render(request, "user_detail.html", {"user": user, "profiles": profiles})


def profile_detail(request, user_id, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user_id=user_id)
    context = {"profile": profile}
    return render(request, "profile_detail.html", context)


# def zoo(request):
#     return render(request, "base/zoo.html")


# def ape(request, pk):
#     ape = None
#     for i in apes:
#         if i["id"] == int(pk):
#             ape = i
#     context = {"ape": ape}
#     return render(request, "base/ape.html", context)
