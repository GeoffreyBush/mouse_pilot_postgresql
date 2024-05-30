from django import forms

from mice_repository.models import Mouse
from website.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from website.models import Project, Strain
from system_users.models import CustomUser


class ProjectMiceForm(forms.ModelForm):

    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    clipped_date = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    mother = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    father = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    earmark = forms.ChoiceField(
        choices=EARMARK_CHOICES_PAIRED,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    genotyper = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    strain = forms.ModelChoiceField(
        queryset=Strain.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Mouse
        fields = [
            "sex",
            "dob",
            "clipped_date",
            "mother",
            "father",
            "project",
            "earmark",
            "genotyper",
            "strain",
        ]
