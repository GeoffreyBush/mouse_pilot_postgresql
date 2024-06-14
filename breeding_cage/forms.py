from django import forms

from breeding_cage.models import BreedingCage
from mice_repository.models import Mouse


class BreedingCageForm(forms.ModelForm):

    box_no = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "---"}),
        required=True,
        label="Box Number",
    )
    mother = forms.ModelChoiceField(
        queryset=Mouse.objects.filter(sex="F"),
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Mother ID"}),
    )
    father = forms.ModelChoiceField(
        queryset=Mouse.objects.filter(sex="M"),
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Father ID"}),
    )
    date_born = forms.DateField(
        initial=None,
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
        ),
        label="DBorn",
    )
    number_born = forms.CharField(
        initial="0",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="NBorn",
    )
    cull_to = forms.CharField(
        initial="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "C/To"}),
        label="C/To",
    )
    date_wean = forms.DateField(
        initial=None,
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
        ),
        label="DWean",
    )
    number_wean = forms.CharField(
        initial="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "NWean"}),
        label="NWean",
    )
    pwl = forms.CharField(
        initial="",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "NBorn - NWean"}
        ),
        label="PWL",
    )
    male_pups = forms.IntegerField(
        initial="0",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Current Male Pups",
    )
    female_pups = forms.CharField(
        initial="0",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Current Female Pups",
    )

    class Meta:
        model = BreedingCage
        fields = "__all__"
        exclude = ["transferred_to_stock", "id"]


class PupsToStockCageForm(forms.ModelForm):
    transferred_to_stock = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Mouse
        fields = "__all__"
        exclude = []
