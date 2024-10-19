from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import slugify_instance_title


class Profile(models.Model):
    # JOB_SEEKER = "JS"
    # RECRUITER = "RE"
    #
    # PROFILE_CHOICES = [
    #     (JOB_SEEKER, "Job Seeker"),
    #     (RECRUITER, "Recruiter"),
    # ]
    #
    # JOB_SEEKER_MODE = 'job_seeker'
    # RECRUITER_MODE = 'recruiter'
    #
    # MODE_CHOICES = [
    #     (JOB_SEEKER_MODE, 'Job Seeker Mode'),
    #     (RECRUITER_MODE, 'Recruiter Mode'),
    # ]
    # user_mode = models.CharField(max_length=20, choices=MODE_CHOICES, default=JOB_SEEKER_MODE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_profiles")
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    # profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    title = models.CharField(max_length=200, default="default profile")
    bio = models.TextField(blank=True, null=True)

    skills = models.ManyToManyField('Skill', related_name="%(class)s_profiles", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # Salary Range Fields
    min_salary = models.FloatField(blank=True, null=True, default=0)
    max_salary = models.FloatField(blank=True, null=True, default=0)

    def clean(self):
        # Ensure min_salary is less than or equal to max_salary
        if self.min_salary and self.max_salary and self.min_salary > self.max_salary:
            raise ValidationError("Minimum salary cannot be greater than maximum salary.")

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        abstract = True
        ordering = ["-updated", "-created"]


class Skill(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-title"]


class JobSeeker(Profile):
    academics = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True, default=0)
    matches = models.ManyToManyField('Recruiter', through='Match', related_name="job_seekers")

    def save(self, *args, **kwargs):
        # self.user_mode = Profile.JOB_SEEKER_MODE
        super().save(*args, **kwargs)


class Recruiter(Profile):
    company = models.CharField(max_length=255)
    matches = models.ManyToManyField(JobSeeker, through="Match", related_name="recruiters")

    def save(self, *args, **kwargs):
        # self.user_mode = Profile.RECRUITER_MODE
        super().save(*args, **kwargs)


class Match(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    match_date = models.DateTimeField(auto_now_add=True)
    match_status = models.CharField(max_length=50, default="pending")

    def __str__(self):
        return f"{self.job_seeker.user.username} matched with {self.recruiter.user.username} on {self.match_date}"


def profile_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        slugify_instance_title(instance)


def profile_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


# Signals
pre_save.connect(profile_pre_save, sender=Recruiter)
pre_save.connect(profile_pre_save, sender=JobSeeker)

post_save.connect(profile_post_save, sender=JobSeeker)
post_save.connect(profile_post_save, sender=Recruiter)
