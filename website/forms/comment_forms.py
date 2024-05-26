from django import forms

from website.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["comment_text"]
        labels = {"comment_text": ""}
        widgets = {
            "comment_text": forms.Textarea(attrs={"rows": 12, "cols": 20}),
        }