from django import forms

from mice_repository.models import Mouse
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


class AddMouseToProjectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.strains = kwargs.pop("strains", None)
        super().__init__(*args, **kwargs)
        if self.strains:
            self.fields["mice"].queryset = Mouse.objects.filter(
                strain__in=self.strains
            ).filter(project=None)
        else:
            raise ValueError("Strains must be provided to initialise the form")

    mice = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "8"}),
        required=True,
    )
