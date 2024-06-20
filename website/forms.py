from django import forms

from mice_repository.models import Mouse
from website.models import MouseComment


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
        error_messages={"required": "At least one mouse must be selected for a request"},
    )

    class Meta:
        fields = ["mice"]

    def clean(self):
        cleaned_data = super().clean()
        mice = cleaned_data.get("mice")

        if not mice or len(mice) == 0:
            raise forms.ValidationError("At least one mouse must be selected for a request")
        return cleaned_data

    def save(self, commit=True):
        pass

class MouseCommentForm(forms.ModelForm):
    
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        max_length=400,
        required=False,
    )

    class Meta:
        model = MouseComment
        fields = ["comment_text"]

