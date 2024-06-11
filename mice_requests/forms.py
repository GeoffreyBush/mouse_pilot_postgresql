from django import forms

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

    def clean(self):
        cleaned_data = super().clean()
        task_type = cleaned_data.get("task_type")
        mice = cleaned_data.get("mice")

        if not mice or len(mice) == 0:
            raise forms.ValidationError("You must select at least one mouse.")

        if task_type == "Cull":
            for mouse in mice:
                if mouse.culled:
                    raise forms.ValidationError(
                        f"Mouse {mouse} has already been culled."
                    )

        elif task_type == "Clip":
            for mouse in mice:
                if mouse.is_genotyped():
                    raise forms.ValidationError(
                        f"Mouse {mouse} has already been clipped."
                    )

        return cleaned_data

    class Meta:
        model = Request
        fields = ["mice", "task_type", "new_message"]
