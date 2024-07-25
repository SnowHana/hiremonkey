from django.contrib import admin

# Register your models here.
from .models import JobSeeker, Recruiter, Skill

admin.site.register(Skill)


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    # list_display = ("user", "bio", "academics", "skills")
    list_display = ("user", "bio", "academics")


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ("user", "bio", "company")


# admin.site.register(Profile)
# admin.site.register(User)
