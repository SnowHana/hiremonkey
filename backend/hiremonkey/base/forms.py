from django import forms
from .models import JobSeeker, Recruiter


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = [
            "profile_title",
            "academics",
            "skills",
        ]


class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ["company"]


# class SkillForm(forms.ModelForm):
#     class Meta:
#         model = Skill
#         fields = ["name"]
