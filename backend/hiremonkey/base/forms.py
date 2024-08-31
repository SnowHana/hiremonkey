from django import forms
from .models import JobSeeker, Recruiter, ProfileReference, Skill
from dal import autocomplete
from taggit.forms import TagWidget


# class JobSeekerForm(forms.ModelForm):

#     # skills = forms.ModelMultipleChoiceField(
#     #     queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple
#     # )
#     skills = forms.ModelMultipleChoiceField(
#         queryset=Skill.objects.all(),
#         widget=autocomplete.ModelSelect2Multiple(
#             url="skill-autocomplete",
#             attrs={
#                 "data-tags": "true",
#                 "data-token-separators": '[",", " "]',  # Allow comma and space as separators
#                 "data-allow-clear": "true",  # Optional: Allow clearing the selection
#                 "placeholder": "Search or add for skills",
#             },
#         ),
#         required=False,
#         # widget=autocomplete.ModelSelect2Multiple(url="skill-autocomplete"),
#     )

#     class Meta:
#         model = JobSeeker
#         fields = ["profile_title", "academics", "skills"]

# # NOTE: This might break it?
# def clean_skills(self):
#     skills = self.cleaned_data.get("skills")
#     skill_names = self.data.getlist("skills")  # Get raw data input

#     for skill_name in skill_names:
#         # Create a new Skill if it does not already exist
#         if skill_name and not Skill.objects.filter(name=skill_name).exists():
#             new_skill = Skill.objects.create(name=skill_name)
#             skills = skills | Skill.objects.filter(pk=new_skill.pk)

#     return skills

# def clean_skills(self):
#     skills = self.cleaned_data.get("skills")
#     skill_names = self.data.getlist("skills")

#     for skill_name in skill_names:
#         if skill_name and not Skill.objects.filter(name=skill_name).exists():
#             new_skill = Skill.objects.create(name=skill_name)
#             skills = skills | Skill.objects.filter(pk=new_skill.pk)

#     return skills


class JobSeekerForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="skill-autocomplete",
            # attrs={
            #     "data-tags": "true",
            #     "data-token-separators": '[",", " "]',  # Allow comma and space as separators
            #     "data-allow-clear": "true",  # Optional: Allow clearing the selection
            #     "placeholder": "Search or add for skills",
            # },
        ),
        required=False,
    )

    class Meta:
        model = JobSeeker
        fields = ["profile_title", "academics", "skills"]

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


# widgets = {
#     "skills": autocomplete.ModelSelect2Multiple(
#         url="skill-autocomplete",
#         attrs={
#             "data-placeholder": "Autocomplete...",
#             # Trigger after 3 characters are entered
#             "data-minimum-input-length": 3,
#         },
#     )
# }

# skills = forms.(
#     queryset=Skill.objects.all(),
# )
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
