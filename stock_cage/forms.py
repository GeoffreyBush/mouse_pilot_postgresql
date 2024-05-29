from django import forms
from django.core.exceptions import ValidationError

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
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )
    mother = forms.ModelChoiceField(
        required=True,
        queryset=Mouse.objects.filter(sex="F"),
    )
    father = forms.ModelChoiceField(
        required=True,
        queryset=Mouse.objects.filter(sex="M"),
    )

    # Override clean() to hrow ValidationError if new _global_id is already in use
    def clean(self):
        cleaned_data = super().clean()
        _tube = cleaned_data.get("_tube")
        strain = cleaned_data.get("strain")
        new_global_id = f"{strain.strain_name}-{_tube}"
        if Mouse.objects.filter(_global_id=new_global_id).exists():
            raise ValidationError("Global ID already in use")

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
