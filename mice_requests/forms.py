from django import forms
from django.contrib.auth import get_user_model

from mice_repository.models import Mouse
from mice_requests.models import Request


class RequestForm(forms.ModelForm):

    task_type = forms.ChoiceField(
        choices=Request.TASK_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    mice = forms.ModelMultipleChoiceField(
        queryset=Mouse.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    new_message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )

    class Meta:
        model = Request
        fields = ["mice", "task_type", "new_message"]
