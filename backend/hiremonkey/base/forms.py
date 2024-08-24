from django import forms
from .models import JobSeeker, Recruiter, ProfileReference
from dal import autocomplete
from taggit.models import Tag
from taggit.forms import TagWidget


class JobSeekerForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="skill-autocomplete"),
    )

    # skills = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple
    # )

    class Meta:
        model = JobSeeker
        fields = [
            "profile_title",
            "academics",
            "skills",
        ]
        # ]
        # widgets = {
        #     "skills": TagWidget(attrs={"placeholder": "Add skills here"}),
        # }


class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ["profile_title", "company"]


PROFILE_FORM_MAPPING = {JobSeeker: JobSeekerForm, Recruiter: RecruiterForm}


def get_form_class_from_profile_reference(profile_reference: ProfileReference):
    profile_model = profile_reference.content_type.model_class()

    return PROFILE_FORM_MAPPING.get(profile_model)


# class SkillForm(forms.ModelForm):
#     class Meta:
#         model = Skill
#         fields = ["name"]
