from django import forms
from .models import JobSeeker, Recruiter

from taggit.forms import TagWidget


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = [
            "profile_title",
            "academics",
            "skills",
        ]
        widgets = {
            "skills": TagWidget(attrs={"placeholder": "Add skills here"}),
        }


class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ["company"]


# class SkillForm(forms.ModelForm):
#     class Meta:
#         model = Skill
#         fields = ["name"]
