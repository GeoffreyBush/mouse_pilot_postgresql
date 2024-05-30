from django import forms
from django.contrib.auth import get_user_model

from mice_repository.models import Mouse
from website.models import Request


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
