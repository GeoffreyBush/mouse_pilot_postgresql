from django import forms
from datetime import date
from website.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from website.models import CustomUser, Mouse, Project, Strain


class RepositoryMiceForm(forms.ModelForm):

    sex = forms.ChoiceField(
        initial="M",
        required=True,
        choices=SEX_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    dob = forms.DateField(  
        initial=None,
        required=True,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    clipped_date = forms.DateField(
        initial=None,
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    mother = forms.ModelChoiceField(
        initial=None,
        queryset=Mouse.objects.filter(sex="F"),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    father = forms.ModelChoiceField(
        initial=None,
        queryset=Mouse.objects.filter(sex="M"),
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
        fields = "__all__"  # or list the fields you want to include
