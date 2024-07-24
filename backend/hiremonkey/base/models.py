from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Ape(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    JOB_SEEKER = "JS"
    RECRUITER = "RE"
    # BOTH = "BO"

    PROFILE_CHOICES = [
        (JOB_SEEKER, "Job Seeker"),
        (RECRUITER, "Recruiter"),
        # (BOTH, "Both"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    
    # Highest level of education
    edu_level = models.CharField(max_length=2, choices=)
    academics = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name="profiles")

    def __str__(self):
        return f"{self.user.username} - {self.profile_type}"
