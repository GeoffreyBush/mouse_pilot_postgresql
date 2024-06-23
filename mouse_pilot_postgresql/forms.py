from django import forms
from mice_repository.models import Mouse

class MouseSelectionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if self.project:
            self.fields["mice"].queryset = Mouse.objects.filter(project=self.project)
        else:
            self.fields["mice"].queryset = Mouse.objects.all()

    mice = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        error_messages={
            "required": "At least one mouse must be selected for a request"
        },
    )

    class Meta:
        fields = ["mice"]
        order_by = ["_global_id"]

    def clean(self):
        cleaned_data = super().clean()
        mice = cleaned_data.get("mice")

        if not mice or len(mice) == 0:
            raise forms.ValidationError(
                "At least one mouse must be selected for a request"
            )
        return cleaned_data

    def save(self, commit=True):
        pass