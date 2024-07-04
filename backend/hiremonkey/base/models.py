from django.db import models

# Create your models here.


# class Ape(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    JOB_SEEKER = "JS"
    RECRUITER = "RE"
    BOTH = "BO"

    PROFILE_CHOICES = [
        (JOB_SEEKER, "Job Seeker"),
        (RECRUITER, "Recruiter"),
        (BOTH, "Both"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.profile_type}"
