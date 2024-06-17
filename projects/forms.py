from django import forms

from projects.models import Project
from strain.models import Strain
from system_users.models import CustomUser


class NewProjectForm(forms.ModelForm):

    project_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30,
        required=True,
    )
    research_area = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=50,
        required=False,
    )
    strains = forms.ModelMultipleChoiceField(
        queryset=Strain.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )
    researchers = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )

    class Meta:
        model = Project
        fields = "__all__"
