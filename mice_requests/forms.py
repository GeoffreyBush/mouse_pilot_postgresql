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
        widget=forms.MultipleHiddenInput(),
    )

    # Should be able to initialise a form when no mice are selected from MouseSelectionForm

    def clean(self):
        cleaned_data = super().clean()
        task_type = cleaned_data.get("task_type")
        mice = cleaned_data.get("mice")

        errors = {}
        if not mice or len(mice) == 0:
            raise forms.ValidationError("You must select at least one mouse.")
        else:
            mice_errors = []
            if task_type == "Cull":
                for mouse in mice:
                    if mouse.culled:
                        mice_errors.append(f"Mouse {mouse} has already been culled.")
                    elif Request.objects.filter(task_type="Cull", mice=mouse).exists():
                        mice_errors.append(f"Mouse {mouse} already has a cull request.")

            elif task_type == "Clip":
                for mouse in mice:
                    if mouse.is_genotyped():
                        mice_errors.append(f"Mouse {mouse} has already been clipped.")
                    elif Request.objects.filter(task_type="Clip", mice=mouse).exists():
                        mice_errors.append(f"Mouse {mouse} already has a clip request.")

            if mice_errors:
                errors["mice"] = mice_errors

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = Request
        fields = ["mice", "task_type"]
