from django import forms

from mice_repository.models import Mouse
from system_users.models import CustomUser
from test_factories.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from website.models import Project, Strain


from django.contrib.auth import get_user_model
from website.models import Request

class ProjectMiceForm(forms.ModelForm):

    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    clipped_date = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    mother = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    father = forms.ModelChoiceField(
        queryset=Mouse.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    earmark = forms.ChoiceField(
        choices=EARMARK_CHOICES_PAIRED,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    genotyper = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    strain = forms.ModelChoiceField(
        queryset=Strain.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Mouse
        fields = [
            "sex",
            "dob",
            "clipped_date",
            "mother",
            "father",
            "project",
            "earmark",
            "genotyper",
            "strain",
        ]

class RequestForm(forms.ModelForm):

    # Override __init__() to filter mice by project
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if self.project:
            self.fields["mice"].queryset = Mouse.objects.filter(project=self.project)
        else:
            self.fields["mice"].queryset = Mouse.objects.all()

    # Add checkbox for mice selection
    mice = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )

    researcher = forms.ModelChoiceField(queryset=get_user_model().objects.all())

    class Meta:
        model = Request
        fields = ["mice", "task_type", "researcher", "new_message"]


class MouseSelectionForm(forms.ModelForm):

    # Override __init__() to filter mice by project
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if self.project:
            self.fields["mice"].queryset = Mouse.objects.filter(project=self.project)
        else:
            self.fields["mice"].queryset = Mouse.objects.all()

    mice = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Mouse
        fields = ["mice"]