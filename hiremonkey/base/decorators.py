from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def require_activated_profile(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_session = getattr(request.user, "usersession", None)
        if not user_session:
            messages.error(request, "User session not found.")
            return redirect("home")

        profile = user_session.get_activated_profile()
        if profile is None:
            messages.warning(
                request,
                "You need to create or select an active profile to access this feature.",
            )
            return redirect("active_profile_selection")

        request.activated_profile = profile
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_job_profile(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Require at least one profile created by an user
        user_session = getattr(request.user, "usersession", None)
        if not user_session:
            messages.error(request, "User session not found.")
            return redirect("home")

        if not user_session.get_all_job_profiles():
            # No profile crated
            messages.error(request, "At least one job profile should be created.")
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
