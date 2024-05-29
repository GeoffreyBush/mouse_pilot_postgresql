from django import forms

from mice_repository.models import Mouse

# Need to create validation handling for readonly attributes here
# Add them to view
class CreateMouseFromBreedingCageForm(forms.ModelForm):
    #strain = forms.CharField(max_length=20, required=True,
     #                       widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}) )

    sex = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )



    class Meta:
        model = Mouse
        fields = "__all__"
        include = []
        exclude = ["project", "earmark", "result", "_global_id", "mother", "father", "dob", "strain", "fate", "genotyper", "clipped_date"]
