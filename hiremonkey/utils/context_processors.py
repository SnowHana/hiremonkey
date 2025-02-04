from base.models import UserSession, UserStatusEnum


def user_session_context(request):
    user_session = UserSession.objects.get(user=request.user)

    return {"user_session": user_session}


def user_status_enum_context(request):
    return {
        "JOBSEEKER": UserStatusEnum.JOBSEEKER,
        "RECRUITER": UserStatusEnum.RECRUITER,
    }
