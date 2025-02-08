from django.utils import timezone
from enum import Enum
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from .utils import slugify_instance_title


class UserStatusEnum(models.TextChoices):
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
        e.g. 'R' -> 'Recruiter', 'J' -> 'JobSeeker'
        """
        return dict(cls.choices).get(enum_value, f"Invalid enum value: {enum_value}")


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    user_status = models.CharField(
        max_length=1,
        choices=UserStatusEnum.choices,
        default=UserStatusEnum.JOBSEEKER,
    )

    activated_profile_id = models.PositiveIntegerField(null=True, blank=True)

    def is_jobseeker(self):
        return self.user_status == UserStatusEnum.JOBSEEKER

    def is_recruiter(self):
        return self.user_status == UserStatusEnum.RECRUITER

    def get_user_status(self):
        # if self.is_jobseeker():
        #     return UserStatusEnum.JOBSEEKER.value[1]
        # else:
        #     return UserStatusEnum.RECRUITER.value[1]
        return UserStatusEnum.to_human_readable(self.user_status)

    def get_activated_profile(self):
        """Get currently activated profile of User

        Raises:
            ValueError: If user is neither a job seeker, nor a recruiter

        Returns:
            _type_: JobProfile Object (JobSeeker, Recruiter)
            None : If Not exists..
        """
        # Handle when there is no activated profile
        if not self.activated_profile_id:
            # raise AttributeError("No active profile is set for this user")
            return None
        # Activated profile exists
        try:
            if self.is_jobseeker():
                return JobSeeker.objects.get(id=self.activated_profile_id)
            elif self.is_recruiter():
                return Recruiter.objects.get(id=self.activated_profile_id)
            else:
                raise ValueError("Error: Neither a recruiter nor a jobseeker type.")
        except (
            JobSeeker.DoesNotExist,
            Recruiter.DoesNotExist,
            JobSeeker.MultipleObjectsReturned,
            Recruiter.MultipleObjectsReturned,
        ):
            return None

    def set_activated_profile(self, profile_id):
        self.activated_profile_id = profile_id
        self.save()

    def get_all_job_profiles(self):
        try:
            if self.is_jobseeker():
                return JobSeeker.objects.filter(user=self.user)
            elif self.is_recruiter():
                return Recruiter.objects.filter(user=self.user)
            else:
                raise ValueError("Error: Neither a recruiter nor a jobseeker type.")
        except (
            JobSeeker.DoesNotExist,
            Recruiter.DoesNotExist,
        ):
            return None

    def __str__(self):
        return f"{self.user} - {self.get_user_status()} : Actiaved {self.get_activated_profile()}"


class Profile(models.Model):
    # Keep track of which user_status and actiavted profile user is viewing

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # def clean(self):
    #     # Ensure min_salary is less than or equal to max_salary
    #     pass

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            self.slug = f"{base_slug}-{self.pk}" if self.pk else base_slug

        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - Profile"

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

    def pending_matches(self):
        """Get pending matches of JobSeeker

        Returns:
            _type_: _description_
        """
        return self.matches.filter(match__match_status=MatchStatusEnum.PENDING)

    def send_like(self, recruiter):
        match, created = Match.get_or_create_match(self, recruiter)
        # Now update Match object
        # We sent like, for a alr existing pending match => Match!
        if not created and match.is_pending():
            # ACCEPTED
            match.match_status = MatchStatusEnum.ACCEPTED
            match.save()


class Recruiter(JobProfile):
    company = models.CharField(max_length=255)
    matches = models.ManyToManyField(
        JobSeeker, through="Match", related_name="recruiters"
    )

    def save(self, *args, **kwargs):
        # self.user_mode = Profile.RECRUITER_MODE
        super().save(*args, **kwargs)

    def accepted_matches(self):
        return self.matches.filter(match__match_status=MatchStatusEnum.ACCEPTED)

    def send_like(self, job_seeker):
        match, created = Match.get_or_create_match(job_seeker, self)

        if not created and match.is_pending():
            # ACCEPTED
            match.match_status = MatchStatusEnum.ACCEPTED
            match.save()


class MatchStatusEnum(models.TextChoices):
    """Match Status Enum class

    Args:
        Enum (_type_): _description_
    """

    PENDING = "P", "Pending"
    ACCEPTED = "A", "Accepted"
    DECLINED = "D", "Declined"
    FAILED = "F", "Failed"


class Match(models.Model):
    """Represent Match established
    between a Job Seeker and a Recruiter


    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    match_date = models.DateTimeField(auto_now_add=True)
    match_status = models.CharField(
        max_length=1,
        choices=MatchStatusEnum.choices,
        default=MatchStatusEnum.FAILED,
    )
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.match_status} : {self.job_seeker.user.username} matched with {self.recruiter.user.username} on {self.match_date}"

    def is_accepted(self):
        return self.match_status == MatchStatusEnum.ACCEPTED

    def is_pending(self):
        return self.match_status == MatchStatusEnum.PENDING

    def is_declined(self):
        return self.match_status == MatchStatusEnum.DECLINED

    def is_failed(self):
        return self.match_status == MatchStatusEnum.FAILED

    @classmethod
    def get_or_create_match(cls, job_seeker: JobSeeker, recruiter: Recruiter):
        """Get or create a Match object between JS and RC

        Args:
            job_seeker (JobSeeker):
            recruiter (Recruiter):
        """

        match, created = cls.objects.get_or_create(
            job_seeker=job_seeker,
            recruiter=recruiter,
            defaults={"match_status": MatchStatusEnum.PENDING},
        )

        return match, created

    # def get_match_status(self):
    #     return MatchStatusEnum.t


def profile_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        slugify_instance_title(instance)


def profile_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


# Signals
pre_save.connect(profile_pre_save, sender=Recruiter)
pre_save.connect(profile_pre_save, sender=JobSeeker)
# pre_save.connect(profile_pre_save, sender=Profile)

post_save.connect(profile_post_save, sender=JobSeeker)
post_save.connect(profile_post_save, sender=Recruiter)
# post_save.connect(profile_post_save, sender=Profile)


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
