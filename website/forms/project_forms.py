from django import forms

from website.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from website.models import CustomUser, Mouse, Project, Strain


class ProjectMiceForm(forms.ModelForm):

    sex = forms.ChoiceField(
        choices=SEX_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    clippedDate = forms.DateField(
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
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Mouse
        fields = "__all__"
