from dal import autocomplete
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobSeekerForm, RecruiterForm
from .models import JobSeeker, Profile, Recruiter, Skill, Match, UserStatusEnum


@login_required
def user_mode_selection(request):
    if request.method == "POST":
        try:

            selected_mode = request.POST.get("user_mode")
            # print(selected_mode)

            # Change profile's field
            profile = Profile.objects.get(user=request.user)

            profile.user_status = UserStatusEnum.from_human_readable(selected_mode)
            profile.save()
            messages.info(request, f"You have selected {profile.get_user_status()}!")
            messages.info(
                request,
                f"You have selected {UserStatusEnum.from_human_readable(selected_mode)}!",
            )
        except User.DoesNotExist:
            raise Http404

        # request.session["user_mode"] = selected_mode  # Store the selection in session
        return redirect("home")  # Redirect to home view after selection

    return render(request, "base/user_mode_selection.html")


def home(request):
    # User is not authenticated. Prompt to login and choose profile
    job_seekers = JobSeeker.objects.prefetch_related("skills")[:5]
    recruiters = Recruiter.objects.all()[:5]
    context = {"job_seekers": job_seekers, "recruiters": recruiters}
    if request.user.is_authenticated:
        # Authorised
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            raise Http404
        except Profile.MultipleObjectsReturned:
            pass
        user_status = profile.get_user_status()
        context = {
            "user_status": user_status,
            "job_seekers": job_seekers,
            "recruiters": recruiters,
        }

        return render(request, "base/home.html", context)
    else:
        # Not logged in
        return redirect("login")

    # messages.info(request, 'You have selected recruiter!')


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
        except User.DoesNotExist:
            # User doesnt exist
            messages.error(request, "User does not exist")
            # NOTE: idk might lead to an error

            return render(request, "base/login_register.html", context)
        # User exists
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("user_mode_selection")
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
            all_skill_permissions = Permission.objects.filter(
                content_type=skill_content_type
            )
            # Add all permissions to the user
            user.user_permissions.add(*all_skill_permissions)
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error occured during registration process")
    return render(request, "base/login_register.html", context)


def jobseeker(request, slug=None):
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
            # Or we can do http404
        except:
            raise Http404
    # user = profile.user
    context = {"profile": profile}
    return render(request, "base/jobseeker.html", context)


def recruiter(request, slug=None):
    if slug is not None:
        try:
            profile = get_object_or_404(Recruiter, slug=slug)
        except Recruiter.DoesNotExist:
            raise Http404
        except Recruiter.MultipleObjectsReturned:
            profile = Recruiter.objects.filter(slug=slug).first()
            # Or we can do http404
        except:
            raise Http404
    context = {"profile": profile}
    return render(request, "base/recruiter.html", context)


@login_required
def select_profile_type(request):
    if request.method == "POST":
        # Register or Create a profile
        profile_type = request.POST.get("profile_type")
        if profile_type == "jobseeker":
            return redirect("create_jobseeker")
        elif profile_type == "recruiter":
            return redirect("create_recruiter")
    return render(request, "base/select_profile_type.html")


@login_required(login_url="/login")
def create_jobseeker(request):
    # NOTE f
    # common_skills = JobSeeker.skills.most_common()[:4]

    if request.method == "POST":
        form = JobSeekerForm(request.POST, user=request.user)

        if form.is_valid():
            job_seeker = form.save(commit=False)
            job_seeker.user = request.user
            job_seeker.save()
            # save skills
            form.save_m2m()

            messages.success(request, "Job Seeker profile created successfully!")
            return redirect("home")
        else:
            messages.error(
                request, "Error occured during creating a Job Seeker profile"
            )
            context = {"form": form}
            return render(request, f"base/create_jobseeker.html", context)
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
def create_recruiter(request):
    # NOTE f
    # common_skills = JobSeeker.skills.most_common()[:4]

    if request.method == "POST":
        form = RecruiterForm(request.POST, user=request.user)

        if form.is_valid():
            job_seeker = form.save(commit=False)
            job_seeker.user = request.user
            job_seeker.save()
            # save skills
            form.save_m2m()

            messages.success(request, "Recruiter profile created successfully!")
            return redirect("home")
        else:
            messages.error(request, "Error occured during creating a Recruiter profile")
            context = {"form": form}
            return render(request, f"base/create_recruiter.html", context)

    else:
        form = RecruiterForm()
        return render(
            request,
            "base/create_recruiter.html",
            {
                "form": form,
            },
        )


@login_required(login_url="/login")
def matched_profile(request, slug=None):

    user_mode = request.session.get("user_mode", False)
    print("####################################")
    print(user_mode)
    user_mode_data = {"job_seeker": JobSeeker, "recruiter": Recruiter}
    if user_mode is False or user_mode not in user_mode_data:
        messages.error(request, "Error occured while accesesing Match page")

    if user_mode == "job_seeker":
        target = user_mode_data["recruiter"]
    elif user_mode == "recruiter":
        target = user_mode_data["job_seeker"]

    user_subclass = user_mode_data[user_mode]
    if slug is not None:
        try:
            profile = get_object_or_404(user_subclass, slug=slug)
        except user_subclass.DoesNotExist:
            raise Http404
        except user_subclass.MultipleObjectsReturned:
            profile = user_subclass.objects.filter(slug=slug).first()
        except:
            raise Http404

    # Query
    # NOTE: This will go wrong lol
    matches = Match.objects.filter(user_mode=request.user)


# if request.method == "POST":
#     print(f"Request user in POST: {request.user}")
#     form = RecruiterForm(request.POST, user=request.user)
#     if form.is_valid():
#         recruiter = form.save(commit=False)
#         print(f"Recruiter user: {recruiter.user}")
#         recruiter.user = request.user
#         recruiter.save()
#         form._save_m2m()
#         messages.success(request, "Successfully created a recruiter profile!")
#         return redirect("home")
#     # else:
#     #     messages.error(request, "Error occurred during creating a recruiter profile")
# else:
#     print(f"Request user in GET: {request.user}")
#     form = RecruiterForm(user=request.user)
#
# return render(request, "base/create_recruiter.html", {"form": form})


@login_required(login_url="/login")
def update_profile(request, profile_type=None, slug=None):
    if profile_type == "jobseeker":
        profile_model = JobSeeker
        form_class = JobSeekerForm
    elif profile_type == "recruiter":
        profile_model = Recruiter
        form_class = RecruiterForm
    else:
        raise Http404("Profile type is not valid.")

    # Retrieve the profile using slug
    profile = None
    if slug is not None:
        try:
            profile = get_object_or_404(profile_model, slug=slug)
        except profile_model.DoesNotExist:
            raise Http404
        except profile_model.MultipleObjectsReturned:
            profile = profile_model.objects.filter(slug=slug).first()
            # Or we can do http404
        except:
            raise Http404

    if request.user != profile.user:
        # TODO: Later do some elegant way..maybe pop up message or sth
        return HttpResponse("You are not allowed here.")

    # form_class = get_form_class_from_profile_reference(profile_type)

    if request.method == "POST":
        # Pass user info as well
        form = form_class(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"{profile_model.__name__} profile updated successfully!"
            )
            return redirect("home")
        else:
            messages.error(
                request, f"Error occurred during updating a {profile_model.__name__}."
            )
            # TODO: Display messages more elegantly
            context = {"form": form}
            return render(request, f"base/create_{profile_type}.html", context)
            # return render(request, f"base/create_{profile_type}.html", context)
    else:
        form = form_class(instance=profile, user=request.user)
        context = {"form": form}
        return render(request, f"base/create_{profile_type}.html", context)


# def update_profile(request, slug=None):
#     # TODO: Allow user to only update their own profile
#     # TODO: When we finsih the tag(Skill) search feature, we will probably have to fix this as well.
#     profile_ref = get_object_or_404(ProfileReference, id=pk)
#     form_class = get_form_class_from_profile_reference(profile_ref)
#     if not form_class:
#         # Sth went wrong (Invalid profile ref?)
#         return redirect("home")
#
#     # profile_instance = profile_ref.get_profile()
#     profile_instance = profile_ref.content_object
#
#     profile_model = profile_ref.content_type.model_class()
#     model_name = profile_model.__name__
#
#     if request.user != profile_instance.user:
#         return HttpResponse("You are not allowed here.")
#     # profile = get_object_or_404(profile_model, id=pk)
#     if request.method == "POST":
#         form = form_class(request.POST, instance=profile_instance)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             # save skills
#             form.save_m2m()
#
#             messages.success(
#                 request,
#                 f"{profile_model.__name__} profile updated successfully!",
#             )
#             return redirect("home")
#         else:
#             # Debuggig...sth went wrong.
#             print(form.non_field_errors())
#             print(form.errors)
#             return HttpResponse(f"Invalid form. Something went wrong")
#     else:
#
#         form = form_class(instance=profile_instance)
#         context = {"form": form}
#         html_name = f"base/create_{profile_model.__name__}.html".lower()
#         return render(
#             request,
#             html_name,
#             context,
#         )


@login_required(login_url="/login")
def delete_profile(request, profile_type=None, slug=None):
    # Profile Reference to query
    if profile_type == "jobseeker":
        profile_model = JobSeeker
        form_class = JobSeekerForm
    elif profile_type == "recruiter":
        profile_model = Recruiter
        form_class = RecruiterForm
    else:
        raise Http404("Profile type is not valid.")

    # Retrieve the profile using slug
    profile = None
    if slug is not None:
        try:
            profile = get_object_or_404(profile_model, slug=slug)
        except profile_model.DoesNotExist:
            raise Http404
        except profile_model.MultipleObjectsReturned:
            profile = profile_model.objects.filter(slug=slug).first()
            # Or we can do http404
        except:
            raise Http404
    # profile_ref = get_object_or_404(ProfileReference, id=pk)
    # profile_model = profile_ref.content_type.model_class()
    # We need to get pk (profileReference id) to profile id?

    # profile = get_object_or_404(profile_model, id=profile_ref.object_id)
    # profile = Profile.objects.get(id=pk)

    if request.user != profile.user:
        return HttpResponse("You are not allowed here.")

    if request.method == "POST":
        profile.delete()
        return redirect("home")
    else:
        return render(request, "base/delete.html", {"obj": profile})


class SkillAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Skill.objects.none()

        qs = Skill.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)
        # print("HELLOOOoooOOOOOOOO")
        return qs
