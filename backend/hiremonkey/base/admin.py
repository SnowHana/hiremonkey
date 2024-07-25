from django.contrib import admin

# Register your models here.
from .models import JobSeeker, Recruiter, Skill


class SkillInline(admin.TabularInline):
    model = JobSeeker.skills.through
    extra = 1


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ("user", "academics", "profile_type", "created", "updated")
    search_fields = ("user__username", "academics")
    inlines = [SkillInline]
    exclude = ["profile_type"]
    # For debugging
    readonly_fields = ("id",)


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "profile_type", "created", "updated")
    search_fields = ("user__username", "company")
    exclude = ["profile_type"]
    # For debugging
    readonly_fields = ("id",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
