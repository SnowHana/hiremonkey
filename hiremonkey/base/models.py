from django.utils import timezone
from enum import Enum
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import slugify_instance_title


class UserStatusEnum(Enum):
    """User Status Enum class

    Args:
        Enum (_type_): _description_
    """

    JOBSEEKER = "J", "JobSeeker"
    RECRUITER = "R", "Recruiter"

    @classmethod
    def from_human_readable(cls, readable_name):
        """
        Convert human-readable name to enum value.
        e.g. 'JobSeeker' -> 'J' / 'Recruiter' -> 'R'/ 'Job-seeker' -> 'J'
        """
        name = (
            readable_name.strip()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
            .lower()
        )

        for tag in cls:
            if tag.value[1].lower() == name:
                return tag.value[0]
        raise ValueError(f"Invalid user status: {readable_name}")

    @classmethod
    def to_human_readable(cls, enum_value):
        """
        Convert enum value to human-readable name.
        ie. 'R' -> 'Recruiter' , 'J' -> 'JobSeeker'
        """
        for tag in cls:
            if tag.value[0] == enum_value:
                return tag.value[1]
        raise ValueError(f"Invalid enum value: {enum_value}")


class Profile(models.Model):
    # Keep track of which user_status and actiavted profile user is viewing
    # user_status = models.CharField(
    #     max_length=1,
    #     choices=[(tag.value[0], tag.value[1]) for tag in UserStatusEnum],
    #     default=UserStatusEnum.JOBSEEKER.value[0],
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    # profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    title = models.CharField(max_length=200, default="default profile")
    bio = models.TextField(blank=True, null=True)

    skills = models.ManyToManyField(
        "Skill", related_name="%(class)s_profiles", blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # Salary Range Fields
    min_salary = models.FloatField(blank=True, null=True, default=0)
    max_salary = models.FloatField(blank=True, null=True, default=0)

    def clean(self):
        # Ensure min_salary is less than or equal to max_salary
        if self.min_salary and self.max_salary and self.min_salary > self.max_salary:
            raise ValidationError(
                "Minimum salary cannot be greater than maximum salary."
            )

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        abstract = False
        ordering = ["-updated", "-created"]


class Skill(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-title"]


class JobProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_profiles"
    )
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    title = models.CharField(max_length=200, default="default profile")
    bio = models.TextField(blank=True, null=True)

    skills = models.ManyToManyField(
        "Skill", related_name="%(class)s_profiles", blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # Salary Range Fields
    min_salary = models.FloatField(blank=True, null=True, default=0)
    max_salary = models.FloatField(blank=True, null=True, default=0)

    def clean(self):
        # Ensure min_salary is less than or equal to max_salary
        if self.min_salary and self.max_salary and self.min_salary > self.max_salary:
            raise ValidationError(
                "Minimum salary cannot be greater than maximum salary."
            )

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        # NOTE: Might change this to False if error.
        abstract = True
        ordering = ["-updated", "-created"]


class JobSeeker(JobProfile):
    academics = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True, default=0)
    matches = models.ManyToManyField(
        "Recruiter", through="Match", related_name="job_seekers"
    )

    def save(self, *args, **kwargs):
        # self.user_mode = JobProfile.JOB_SEEKER_MODE
        super().save(*args, **kwargs)


class Recruiter(JobProfile):
    company = models.CharField(max_length=255)
    matches = models.ManyToManyField(
        JobSeeker, through="Match", related_name="recruiters"
    )

    def save(self, *args, **kwargs):
        # self.user_mode = Profile.RECRUITER_MODE
        super().save(*args, **kwargs)


class MatchStatusEnum(Enum):
    """Match Status Enum class

    Args:
        Enum (_type_): _description_
    """

    PENDING = "P", "Pending"
    ACCEPTED = "A", "Accepted"
    DECLINED = "D", "Declined"
    FAILED = "F", "Failed"


class Match(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    match_date = models.DateTimeField(auto_now_add=True)
    # match_status = models.CharField(max_length=50, default="pending")
    match_status = models.CharField(
        max_length=1,
        choices=[(tag.value[0], tag.value[1]) for tag in MatchStatusEnum],
        default=MatchStatusEnum.PENDING.value[0],
    )
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.match_status} : {self.job_seeker.user.username} matched with {self.recruiter.user.username} on {self.match_date}"


def profile_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        slugify_instance_title(instance)


def profile_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


class UserSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_session"
    )

    user_status = models.CharField(
        max_length=1,
        choices=[(tag.value[0], tag.value[1]) for tag in UserStatusEnum],
        default=UserStatusEnum.JOBSEEKER.value[0],
    )

    activated_profile_id = models.PositiveIntegerField(null=True, blank=True)

    def is_jobseeker(self):
        return self.user_status == UserStatusEnum.JOBSEEKER.value[0]

    def is_recruiter(self):
        return self.user_status == UserStatusEnum.RECRUITER.value[0]

    def get_user_status(self):
        if self.is_jobseeker():
            return UserStatusEnum.JOBSEEKER.value[1]
        else:
            return UserStatusEnum.RECRUITER.value[1]

    def get_activated_profile(self):
        """
        Fetch the currently activated profile (JobSeeker or Recruiter).
        """
        if self.is_jobseeker():
            return JobSeeker.objects.filter(id=self.activated_profile_id).first()
        elif self.is_recruiter():
            return Recruiter.objects.filter(id=self.activated_profile_id).first()
        else:
            raise ValueError(f"Error: Neither a recruiter or a jobseeker type.")


# Signals
pre_save.connect(profile_pre_save, sender=Recruiter)
pre_save.connect(profile_pre_save, sender=JobSeeker)

post_save.connect(profile_post_save, sender=JobSeeker)
post_save.connect(profile_post_save, sender=Recruiter)


# # Simple Profile fn
# def get_user_status(user):
#     try:
#         profile = Profile.objects.get(user=user)
#         return profile.user_status
#     except User.DoesNotExist:
#         raise ObjectDoesNotExist(f"User {user} does not exist.")
#     except Profile.DoesNotExist:
#         raise ObjectDoesNotExist(f"Profile does not exist for user {user}.")


# User.add_to_class("get_user_status", get_user_status)
