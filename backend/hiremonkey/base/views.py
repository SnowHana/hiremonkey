from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobSeeker, Profile, ProfileReference, Recruiter, Skill
from .forms import JobSeekerForm, RecruiterForm, SkillForm


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


@login_required
def select_profile_type(request):
    if request.method == "POST":
        # Register or Create a profile
        profile_type = request.POST.get("profile_type")
        if profile_type == "job_seeker":
            return redirect("create_job_seeker")
        elif profile_type == "recruiter":
            return redirect("create_recruiter")
    return render(request, "base/select_profile_type.html")


@login_required
def create_job_seeker(request):
    SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=1, can_delete=True)
    if request.method == "POST":
        job_seeker_form = JobSeekerForm(request.POST)
        skill_formset = SkillFormSet(request.POST, queryset=Skill.objects.none())

        if job_seeker_form.is_valid() and skill_formset.is_valid():
            job_seeker = job_seeker_form.save(commit=False)
            job_seeker.user = request.user
            job_seeker.save()
            job_seeker_form.save_m2m()  # Save the many-to-many relationships

            # Save new skills
            for form in skill_formset:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    skill = form.save()
                    job_seeker.skills.add(skill)

            messages.success(request, "Job Seeker profile created successfully!")
            return redirect("home")
    else:
        job_seeker_form = JobSeekerForm()
        skill_formset = SkillFormSet(queryset=Skill.objects.none())

    return render(
        request,
        "base/create_job_seeker.html",
        {"job_seeker_form": job_seeker_form, "skill_formset": skill_formset},
    )


# def create_job_seeker(request):
#     if request.method == "POST":
#         # Ceate a job seeker
#         form = JobSeekerForm(request.POST)
#         if form.is_valid():
#             job_seeker = form.save(commit=False)
#             job_seeker.user = request.user
#             job_seeker.save()
#             messages.success(request, "Successfully created a job seeker profile!")
#             return redirect("home")
#         else:
#             messages.error(
#                 request, "Error occured during creating a job seeker profile"
#             )
#     else:
#         form = JobSeekerForm()
#         return render(request, "base/create_job_seeker.html", {"form": form})


@login_required
def create_recruiter(request):
    if request.method == "POST":
        # Ceate a job seeker
        form = RecruiterForm(request.POST)
        if form.is_valid():
            recruiter = form.save(commit=False)
            recruiter.user = request.user
            recruiter.save()
            messages.success(request, "Successfully created a recruiter profile!")
            return redirect("home")
        else:
            messages.error(request, "Error occured during creating a recruiter profile")
    else:
        form = RecruiterForm()
        return render(request, "base/create_recruiter.html", {"form": form})
