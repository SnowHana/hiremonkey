from django import forms
from .models import JobSeeker, Recruiter, ProfileReference, Skill
from dal import autocomplete
from taggit.forms import TagWidget
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.urls import reverse_lazy


class JobSeekerForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=AddAnotherWidgetWrapper(
            autocomplete.ModelSelect2Multiple(
                url="skill-autocomplete",
                attrs={
                    "data-placeholder": "Search or add skills",
                },
            ),
            reverse_lazy("skill_create"),
        ),
        required=False,
    )

    class Meta:
        model = JobSeeker
        fields = [
            "profile_title",
            "academics",
            "skills",
        ]


# def clean_skills(self):
#     # TODO: So issue is probs related to this function delivering raw string value instead of String object
#     skills = []
#     skill_names = self.cleaned_data.get("skills")

#     # print("YOU ARE HERE ########")
#     for item in skill_names:
#         # Check if item is alr a Skill object
#         if isinstance(item, Skill):
#             # Alr a skill object
#             skills.append(item)
#         else:
#             skill_name = item.lower().strip()
#             skill, created = Skill.objects.get_or_create(
#                 name=skill_name, defaults={"description": skill_name}
#             )
#             skills.append(skill)
#         # print(skill)
#         # if skill_name and not Skill.objects.filter(name=skill_name).exists():
#         #     new_skill = Skill.objects.create(name=skill_name)
#         #     skills = skills | Skill.objects.filter(id=new_skill.pk)

#     return skills


class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ["profile_title", "company"]


PROFILE_FORM_MAPPING = {JobSeeker: JobSeekerForm, Recruiter: RecruiterForm}


def get_form_class_from_profile_reference(profile_reference: ProfileReference):
    profile_model = profile_reference.content_type.model_class()

    return PROFILE_FORM_MAPPING.get(profile_model)
