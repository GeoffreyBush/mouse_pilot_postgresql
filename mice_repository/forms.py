from django import forms

from mice_repository.models import Mouse
from mouse_pilot_postgresql.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from projects.models import Project
from stock_cage.models import StockCage
from system_users.models import CustomUser
from strain.models import Strain


# Add validation handling for duplicate _global_id here?
# Needed for formset validation. Could do this in the view
class RepositoryMiceForm(forms.ModelForm):

    _tube = forms.IntegerField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    sex = forms.ChoiceField(
        initial="M",
        required=True,
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    dob = forms.DateField(
        initial=None,
        required=True,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    stock_cage = forms.ModelChoiceField(
        initial=None,
        queryset=StockCage.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
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
        initial="",
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    earmark = forms.ChoiceField(
        initial="",
        required=False,
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
    coat = forms.CharField(
        initial="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    result = forms.CharField(
        initial="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    fate = forms.CharField(
        initial="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Mouse
        fields = "__all__"
        exclude = ["_global_id"]
