from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import JobSeeker, Profile, ProfileReference, Recruiter


def home(request):
    # Query concrete subclasses
    job_seekers = JobSeeker.objects.prefetch_related("skills")[:5]
    recruiters = Recruiter.objects.all()[:5]
    context = {"job_seekers": job_seekers, "recruiters": recruiters}

    return render(request, "base/home.html", context)


def loginPage(request):
    page = "login"
    context = {"page": page}
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

            return render(request, "base/login_register.html", context)
        # User exists
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exit")

    return render(request, "base/login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    page = "register"
    form = UserCreationForm()
    context = {"page": page, "form": form}

    if request.method == "POST":
        # Register user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error occured during registration process")
    return render(request, "base/login_register.html", context)


def job_seeker(request, pk):
    # profile = get_object_or_404(Profile, id=profile_id)
    # context = {"profile": profile}
    # try:
    #     profile_reference = ProfileReference.objects.get(object_id=pk)
    #     profile = profile_reference.get_profile()
    # except ProfileReference.DoesNotExist:
    #     # TODO: Later create a 404.html to handle 404 errors
    #     raise Http404("Profile does not exist")
    profile = get_object_or_404(JobSeeker, id=pk)
    # user = profile.user
    context = {"profile": profile}
    return render(request, "base/job_seeker.html", context)


def recruiter(request, pk):

    profile = get_object_or_404(Recruiter, id=pk)
    # user = profile.user
    context = {"profile": profile}
    return render(request, "base/recruiter.html", context)
