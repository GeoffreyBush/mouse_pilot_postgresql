from django import forms

from mice_repository.models import Mouse
from website.models import Strain


# Need to create validation handling for readonly attributes here, add handling to view
class BatchMiceFromBreedingCageForm(forms.ModelForm):

    _tube = forms.IntegerField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    sex = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )

    coat = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # Hidden fields ????
    strain = forms.ModelChoiceField(
        required=True,
        queryset=Strain.objects.all(),
    )
    mother = forms.ModelChoiceField(
        required=True,
        queryset=Mouse.objects.filter(sex="F"),
    )
    father = forms.ModelChoiceField(
        required=True,
        queryset=Mouse.objects.filter(sex="M"),
    )

    class Meta:
        model = Mouse
        fields = "__all__"
        include = []
        exclude = [
            "project",
            "earmark",
            "result",
            "_global_id",
            "fate",
            "genotyper",
            "clipped_date",
        ]
