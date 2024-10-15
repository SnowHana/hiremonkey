from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, Permission
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import JobSeeker, Profile, ProfileReference, Recruiter, Skill
from .forms import JobSeekerForm, RecruiterForm, get_form_class_from_profile_reference
from dal import autocomplete
from django.http import Http404


def home(request):
    # Get 5 latest job seeker and recruiters' profile reference objects

    # Query concrete subclasses
    job_seekers = JobSeeker.objects.prefetch_related("skills")[:5]
    # job_seekers = JobSeeker.objects.all()[:5]

    recruiters = Recruiter.objects.all()[:5]

    # Get profile references
    js_ids = [js.id for js in job_seekers]
    rc_ids = [rc.id for rc in recruiters]

    # Content type
    js_content = ContentType.objects.get_for_model(JobSeeker)
    rc_content = ContentType.objects.get_for_model(Recruiter)

    # Query
    # NOTE:Probably order got mixed here..?
    # TODO: Fix this so it finds profile ref in order.
    # for js_id in js_ids:
    #     js_ref = ProfileReference.objects.filter(
    #         content_type=js_content, object_id__in=js_ids
    #     )
    js_ref_q = ProfileReference.objects.filter(
        content_type=js_content, object_id__in=js_ids
    )
    rc_ref_q = ProfileReference.objects.filter(
        content_type=rc_content, object_id__in=rc_ids
    )

    js_ref_map = {ref.object_id: ref for ref in js_ref_q}
    rc_ref_map = {ref.object_id: ref for ref in rc_ref_q}

    js_ref = [js_ref_map[js_id] for js_id in js_ids if js_id in js_ref_map]

    rc_ref = [
        rc_ref_map[rc_id] for rc_id in rc_ids if rc_id in rc_ref_map
    ]  # Error checking

    if len(js_ref) != len(js_ids) or len(rc_ref) != len(rc_ids):
        # TODO: Flash message feature (saying sth went wrong)
        # print(len(js_ref))
        # print(js_ids)

        # print(rc_ref)
        # print(rc_ids)
        return HttpResponse("Sth went wrong!")

    js = list(zip(js_ref, job_seekers))
    rc = list(zip(rc_ref, recruiters))
    # profile_references = ProfileReference.objects.all()[:5]
    # context = {
    #     "js_ref": js_ref,
    #     "rc_ref": rc_ref,
    #     "job_seekers": job_seekers,
    #     "recruiters": recruiters,
    # }
    context = {"job_seekers": js, "recruiters": rc}
    # print(js[0])

    return render(request, "base/home.html", context)


def loginPage(request):
    # If user is alr logged in, redirect him to the home page when he tries to login - again
    if request.user.is_authenticated:
        return redirect("home")
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
            # Add skill add / edit permission to user
            # Get all permissions related to the Skill model
            skill_content_type = ContentType.objects.get_for_model(Skill)
            all_skill_permissions = Permission.objects.filter(content_type=skill_content_type)
            # Add all permissions to the user
            user.user_permissions.add(*all_skill_permissions)
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error occured during registration process")
    return render(request, "base/login_register.html", context)


def job_seeker(request, slug=None):
    # profile = get_object_or_404(Profile, id=profile_id)
    # context = {"profile": profile}
    # try:
    #     profile_reference = ProfileReference.objects.get(object_id=pk)
    #     profile = profile_reference.get_profile()
    # except ProfileReference.DoesNotExist:
    #     # TODO: Later create a 404.html to handle 404 errors
    #     raise Http404("Profile does not exist")
    if slug is not None:
        try:
            profile = get_object_or_404(JobSeeker, slug=slug)
        except JobSeeker.DoesNotExist:
            raise Http404
        except JobSeeker.MultipleObjectsReturned:
            profile = JobSeeker.objects.filter(slug=slug).first()
        except:
            raise Http404
    # user = profile.user
    context = {"profile": profile}
    return render(request, "base/jobseeker.html", context)


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


@login_required(login_url="/login")
def create_job_seeker(request):
    # NOTE
    # common_skills = JobSeeker.skills.most_common()[:4]

    if request.method == "POST":
        form = JobSeekerForm(request.POST)

        if form.is_valid():
            job_seeker = form.save(commit=False)
            job_seeker.user = request.user
            job_seeker.save()
            # save skills
            form.save_m2m()

            messages.success(request, "Job Seeker profile created successfully!")
            return redirect("home")
    else:
        form = JobSeekerForm()

    return render(
        request,
        "base/create_jobseeker.html",
        {
            "form": form,
        },
    )


@login_required(login_url="/login")
def update_profile(request, pk):
    # TODO: Allow user to only update their own profile
    # TODO: When we finsih the tag(Skill) search feature, we will probably have to fix this as well.
    profile_ref = get_object_or_404(ProfileReference, id=pk)
    form_class = get_form_class_from_profile_reference(profile_ref)

    if not form_class:
        # Sth went wrong (Invalid profile ref?)
        return redirect("home")

    # profile_instance = profile_ref.get_profile()
    profile_instance = profile_ref.content_object

    profile_model = profile_ref.content_type.model_class()
    model_name = profile_model.__name__

    if request.user != profile_instance.user:
        return HttpResponse("You are not allowed here.")
    # profile = get_object_or_404(profile_model, id=pk)
    if request.method == "POST":
        form = form_class(request.POST, instance=profile_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # save skills
            form.save_m2m()

            messages.success(
                request,
                f"{profile_model.__name__} profile updated successfully!",
            )
            return redirect("home")
        else:
            # Debuggig...sth went wrong.
            print(form.non_field_errors())
            print(form.errors)
            return HttpResponse(f"Invalid form. Something went wrong")
    else:

        form = form_class(instance=profile_instance)
        context = {"form": form}
        html_name = f"base/create_{profile_model.__name__}.html".lower()
        return render(
            request,
            html_name,
            context,
        )


@login_required(login_url="/login")
def delete_profile(request, pk):
    # Profile Reference to query
    profile_ref = get_object_or_404(ProfileReference, id=pk)
    profile_model = profile_ref.content_type.model_class()
    # We need to get pk (profileReference id) to profile id?

    profile = get_object_or_404(profile_model, id=profile_ref.object_id)
    # profile = Profile.objects.get(id=pk)

    if request.user != profile.user:
        return HttpResponse("You are not allowed here.")

    if request.method == "POST":
        profile.delete()
        return redirect("home")
    else:
        return render(request, "base/delete.html", {"obj": profile})


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


@login_required(login_url="/login")
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

#
# class JobSeekerAutoComplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Filter out result based on a visitor
#         if not self.request.user.is_authenticated:
#             return JobSeeker.objects.none()
#
#         qs = JobSeeker.objects.all()
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs


class SkillAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Skill.objects.none()

        qs = Skill.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        # print("HELLOOOoooOOOOOOOO")
        return qs
