from django import forms

from stock_cage.models import StockCage


class StockCageForm(forms.ModelForm):

    box_no = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = StockCage
        fields = "__all__"
        exclude = ["cage_id"]
