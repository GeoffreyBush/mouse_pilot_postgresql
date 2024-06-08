from django import forms
from django.contrib.auth import get_user_model

from mice_repository.models import Mouse
from mice_requests.models import Request


class RequestForm(forms.ModelForm):

    mice = forms.ModelMultipleChoiceField(
        queryset=Mouse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    researcher = forms.ModelChoiceField(queryset=get_user_model().objects.all())

    class Meta:
        model = Request
        fields = ["mice", "task_type", "researcher", "new_message"]
