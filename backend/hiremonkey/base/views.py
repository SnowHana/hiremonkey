from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile


def loginPage(request):
    if request.method == "POST":
        # POST method : User trying to log-in
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Check if user exists
        try:
            # NOTE: Later change it with email
            user = User.objects.get(username=username)
        except:
            # User doesnt exist
            messages.error(request, "User does not exist")
            # NOTE: idk might lead to an error
            page = "login"
            context = {"page": page}
            return render(request, "base/login_register.html", context)
        # User exists
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exit")

    page = "login"
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def home(request):
    profiles = Profile.objects.all()[0:5]
    context = {"profiles": profiles}

    return render(request, "base/home.html", context)


# def user_detail(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     profiles = user.profiles.all()
#     return render(request, "user_detail.html", {"user": user, "profiles": profiles})


def profile(request, user_id, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user_id=user_id)
    context = {"profile": profile}
    return render(request, "base/profile.html", context)


# def zoo(request):
#     return render(request, "base/zoo.html")


# def ape(request, pk):
#     ape = None
#     for i in apes:
#         if i["id"] == int(pk):
#             ape = i
#     context = {"ape": ape}
#     return render(request, "base/ape.html", context)
