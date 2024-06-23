from django import forms
from django.core.exceptions import ValidationError

from mice_repository.models import Mouse
from stock_cage.models import StockCage
from strain.models import Strain


class PupsToStockCageFormSet(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        self.breeding_cage = kwargs.pop("breeding_cage", None)
        super().__init__(*args, **kwargs)

    # Override clean method to enforce that:
    # 1. Breeding cage cannot have already been transferred to stock
    # 2. No tube can be null
    # 3. All tubes must be convertible to integers
    # 4. No duplicate tube numbers are allowed
    def clean(self):
        super().clean()
        if self.breeding_cage and self.breeding_cage.transferred_to_stock:
            raise ValidationError(
                "Pups have already been transferred out of this breeding cage"
            )
        tube_numbers = []
        for i, form in enumerate(self.forms):
            tube = self.data.get(f"mouse-{i}-tube")
            if tube is None:
                raise ValidationError("Tube number is required")
            try:
                int(tube)
            except ValueError:
                raise ValidationError("Tube must be convertible to an integer")
            if tube in tube_numbers:
                raise ValidationError("Duplicate tube number")

            tube_numbers.append(tube)

    # Override save method to save all forms in formset with custom data from cage
    def save(self, breeding_cage):
        if not self.is_valid():
            raise ValueError("Formset must be valid before saving")

        for form in self:
            mouse_instance = form.save(commit=False)
            mouse_instance.strain = breeding_cage.strain
            mouse_instance.mother = breeding_cage.mother
            mouse_instance.father = breeding_cage.father
            mouse_instance.dob = breeding_cage.date_born
            mouse_instance.save()

        breeding_cage.transferred_to_stock = True
        breeding_cage.save()


# Need to create validation handling for readonly attributes here, add handling to view
class PupsToStockCageForm(forms.ModelForm):

    _global_id = forms.CharField(required=False, widget=forms.HiddenInput())

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

    cage = forms.ModelChoiceField(
        required=True,
        queryset=StockCage.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        error_messages={"required": "Stock cage is required"},
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

    # Override clean() to throw ValidationError if proposed _global_id for new mouse is already in use by another mouse
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
        instance.tube = self.cleaned_data["tube"]
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Mouse
        include = ["strain", "cage", "tube"]
        exclude = [
            "project",
            "earmark",
            "result",
            # "_global_id",
            "fate",
            "genotyper",
            "clipped_date",
        ]
