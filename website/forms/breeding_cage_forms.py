from django import forms
from website.models import BreedingCage, Mouse

class BreedingCageForm(forms.ModelForm):

    STATUS_CHOICE = [
        ("Empty", "Empty"),
        ("ParentsInside", "ParentsInside"),
        ("ParentsRemoved", "ParentsRemoved"),
    ]

    box_no = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "---"}), label="Box Number"
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICE, widget=forms.Select(), label="Status"
    )
    mother = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Mother ID"}),
    )
    father = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Father ID"}),
    )
    date_born = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        label="DBorn",
    )
    number_born = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "NBorn"}), label="NBorn"
    )
    cull_to = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "C/To"}), label="C/To"
    )
    date_wean = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        label="DWean",
    )
    number_wean = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "NWean"}), label="NWean"
    )
    pwl = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "NBorn - NWean"}), label="PWL"
    )

    class Meta:
        model = BreedingCage
        fields = "__all__"


class BreedingPairForm(forms.ModelForm):
    box_no = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Cage ID"}
        ),
        label="Box Number",
    )
    mother = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Mother ID"}),
    )
    father = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Father ID"}),
    )

    class Meta:
        model = BreedingCage
        fields = ["box_no", "mother", "father"]