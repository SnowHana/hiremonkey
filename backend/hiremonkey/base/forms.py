from django import forms
from .models import JobSeeker, Recruiter, Skill
from dal import autocomplete
from taggit.forms import TagWidget


class JobSeekerForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="skill-autocomplete",
            attrs={
                "data-placeholder": "Search or add skills",
            },
        ),
        required=False,
    )

    class Meta:
        model = JobSeeker
        fields = ["title", 'bio', "academics", "skills", 'min_salary', 'max_salary', ]
class RecruiterForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="skill-autocomplete",
            attrs={
                "data-placeholder": "Search or add skills",
            },
        ),
        required=False,
    )

    class Meta:
        model = Recruiter
        fields = ["title", 'bio', "company", 'skills', 'min_salary', 'max_salary']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop the user from kwargs
        super(RecruiterForm, self).__init__(*args, **kwargs)  # Call parent __init__

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.user is None:
            raise forms.ValidationError("User information is missing.")

        # Query the database to check for existing titles for the same user
        queryset = Recruiter.objects.filter(user=self.user, title=title)
        print(queryset)
        if queryset.exists():
            raise forms.ValidationError("A recruiter profile with this title already exists.")

        return title


PROFILE_FORM_MAPPING = {JobSeeker: JobSeekerForm, Recruiter: RecruiterForm}

#
# def get_form_class_from_profile_reference(profile_reference: ProfileReference):
#     profile_model = profile_reference.content_type.model_class()
#
#     return PROFILE_FORM_MAPPING.get(profile_model)


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
#                 title=skill_name, defaults={"description": skill_name}
#             )
#             skills.append(skill)
#         # print(skill)
#         # if skill_name and not Skill.objects.filter(title=skill_name).exists():
#         #     new_skill = Skill.objects.create(title=skill_name)
#         #     skills = skills | Skill.objects.filter(id=new_skill.pk)

#     return skills

