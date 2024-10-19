from django.contrib import admin

from .forms import JobSeekerForm

# Register your models here.
from .models import JobSeeker, Recruiter, Skill


# class SkillInline(admin.TabularInline):
#     model = JobSeeker.skills.through
#     extra = 1


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("title",)


#
# @admin.register(ProfileReference)
# class ProfileReferenceAdmin(admin.ModelAdmin):
#     # Optionally, customize the list display
#     list_display = ("id", "content_type", "object_id", "content_object")
#     search_fields = ("object_id",)
#
#     def content_object_display(self, obj):
#         return str(obj.content_object)
#
#     content_object_display.short_description = "Profile"
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.select_related("content_type")
#         return queryset
#

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "academics",
        'min_salary',
        "created",
        "updated",
        'slug',
    )
    # list_display = [field.name for field in JobSeeker._meta.get_fields()]
    search_fields = ("user__username", "academics")
    # inlines = [SkillInline]
    exclude = ["profile_type"]
    # For debugging
    readonly_fields = ("id",)

    # Make it use our form
    form = JobSeekerForm

    def get_skills(self, obj):
        return "\n".join([j.skill for j in obj.skills.all()])


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "created", "updated", 'slug', 'min_salary')
    search_fields = ("user__username", "company")
    exclude = ["profile_type"]
    # For debugging
    readonly_fields = ("id",)

# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ("title",)
