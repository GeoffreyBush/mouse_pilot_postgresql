from django import forms
from strain.models import Strain

class StrainForm(forms.ModelForm):

    strain_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Strain
        fields = ["strain_name"]
        labels = {"strain_name": "Strain Name"}
        help_texts = {"strain_name": "Enter the name of the strain."}
        error_messages = {
            "strain_name": {
                "unique": "This strain already exists. Please enter a different strain."
            }
        }