from django import forms
from django.core.exceptions import ValidationError

from mice_repository.models import Mouse
from stock_cage.models import StockCage
from website.models import Strain


# Need to create validation handling for readonly attributes here, add handling to view
class BatchFromBreedingCageForm(forms.ModelForm):

    tube = forms.IntegerField(
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

    stock_cage = forms.ModelChoiceField(
        required=True,
        queryset=StockCage.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    strain = forms.ModelChoiceField(
        required=True,
        queryset=Strain.objects.all(),
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )
    mother = forms.ModelChoiceField(
        required=True,
        queryset=Mouse.objects.filter(sex="F"),
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )
    father = forms.ModelChoiceField(
        required=True,
        queryset=Mouse.objects.filter(sex="M"),
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )
    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"class": "form-control", "readonly": "readonly", "type": "date"}
        ),
    )

    # Override clean() to throw ValidationError if new _global_id is already in use
    def clean(self):
        cleaned_data = super().clean()
        tube = cleaned_data.get("tube")
        strain = cleaned_data.get("strain")
        new_global_id = f"{strain.strain_name}-{tube}"
        if Mouse.objects.filter(_global_id=new_global_id).exists():
            raise ValidationError("Global ID already in use")

    # Override save() method to convert tube field in form to _tube instance for Mouse model
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance._tube = self.cleaned_data["tube"]
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Mouse
        include = ["strain", "stock_cage", "_tube"]
        exclude = [
            "project",
            "earmark",
            "result",
            "_global_id",
            "fate",
            "genotyper",
            "clipped_date",
        ]
