from dal import autocomplete
from django import forms

from .models import JobSeeker, Recruiter, Skill, Match


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
        fields = [
            "title",
            "bio",
            "academics",
            "skills",
            "min_salary",
            "max_salary",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Pop the user from kwargs
        super(JobSeekerForm, self).__init__(*args, **kwargs)  # Call parent __init__

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if self.user is None:
            raise forms.ValidationError("User information is missing.")

        # Query the database to check for existing titles for the same user
        queryset = JobSeeker.objects.filter(user=self.user, title=title)
        # TODO: Now queryset always exists, cuz profile exist.'\\\
        if self.instance.pk is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(
                "A recruiter profile with this title already exists."
            )

        return title


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
        fields = ["title", "bio", "company", "skills", "min_salary", "max_salary"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Pop the user from kwargs
        super(RecruiterForm, self).__init__(*args, **kwargs)  # Call parent __init__

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if self.user is None:
            raise forms.ValidationError("User information is missing.")

        # Query the database to check for existing titles for the same user
        queryset = Recruiter.objects.filter(user=self.user, title=title)

        if queryset.exists():
            raise forms.ValidationError(
                "A recruiter profile with this title already exists."
            )

        return title


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["job_seeker", "recruiter", "memo"]


PROFILE_FORM_MAPPING = {JobSeeker: JobSeekerForm, Recruiter: RecruiterForm}
