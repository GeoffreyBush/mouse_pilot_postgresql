from django import forms

from website.models import MouseComment


class MouseCommentForm(forms.ModelForm):

    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        max_length=400,
        required=False,
    )

    class Meta:
        model = MouseComment
        fields = ["comment_text"]
