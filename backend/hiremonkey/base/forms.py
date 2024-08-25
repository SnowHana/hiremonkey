from django import forms
from .models import JobSeeker, Recruiter, ProfileReference
from dal import autocomplete
from dal_select2.widgets import TagSelect2
from django import forms
from taggit.forms import TagField


class JobSeekerForm(forms.ModelForm):
    # skills = forms.ModelChoiceField(
    #     label = 'Skills',
    #     required=False,
    #     queryset=Skills.ob
    # )
    #     obra_social = forms.ModelChoiceField(
    #     label='Obra Social',
    #     required=False,
    #     queryset=ObraSocial.objects.all(),
    #     widget=autocomplete.ModelSelect2(
    #         url="obra-social-all-autocomplete",
    #         attrs={"data-placeholder": "Seleccione una Obra social"}
    #     ),
    # )
    # paciente = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Paciente.objects.all(),)
    skills = TagField(widget=TagSelect2(url="skill-autocomplete"))

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
        fields = ["profile_title", "company"]


PROFILE_FORM_MAPPING = {JobSeeker: JobSeekerForm, Recruiter: RecruiterForm}


def get_form_class_from_profile_reference(profile_reference: ProfileReference):
    profile_model = profile_reference.content_type.model_class()

    return PROFILE_FORM_MAPPING.get(profile_model)


# class SkillForm(forms.ModelForm):
#     class Meta:
#         model = Skill
#         fields = ["name"]
