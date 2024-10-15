from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# class Skill(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


class ProfileReference(models.Model):
    # NOTE: We dont really utilise this model, we can delete this later
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        if not self.content_object:
            raise ValueError(
                "ProfileReference cannot be created without a valid content_object."
            )
        super().save(*args, **kwargs)

    def get_profile(self):
        return self.content_object

    def __str__(self):
        return f"{self.id}/ object_id: {self.object_id} / {self.content_type}"

    class Meta:
        ordering = []


class Profile(models.Model):
    JOB_SEEKER = "JS"
    RECRUITER = "RE"

    PROFILE_CHOICES = [
        (JOB_SEEKER, "Job Seeker"),
        (RECRUITER, "Recruiter"),
    ]

    profile_title = models.TextField(max_length=200, default="default profile")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.profile_type} - {self.profile_title} - {self.id}"

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(f"{self.user}-{self.profile_title}")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True  # Mark this model as abstract
        ordering = ["-updated", "-created"]


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    # Later on add sth like description, skill level, years of experience etc
    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        ordering = ["-name"]

        # def save(self, *args, **kwargs):
        #     super().save(*args, **kwargs)


class JobSeeker(Profile):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_seeker_profiles"
    )
    academics = models.TextField(blank=True, null=True)

    skills = models.ManyToManyField("Skill", related_name="job_seekers")

    # skills = TaggableManager()

    def save(self, *args, **kwargs):
        self.profile_type = Profile.JOB_SEEKER
        super().save(*args, **kwargs)
        # Create ProfileReference model
        ProfileReference.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            defaults={"content_object": self},
        )


class Recruiter(Profile):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recruiter_profiles"
    )
    company = models.TextField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.profile_type = Profile.RECRUITER
        super().save(*args, **kwargs)
        # Create ProfileReference model
        ProfileReference.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            defaults={"content_object": self},
        )
