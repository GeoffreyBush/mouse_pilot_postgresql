from django import forms
from django.forms import formset_factory

from mice_repository.models import Mouse
from stock_cage.models import StockCage


class MouseForm(forms.ModelForm):
    class Meta:
        model = Mouse
        fields = "__all__"  # replace with your actual fields


MouseFormSet = formset_factory(MouseForm, extra=0)


class TransferToStockCageForm(forms.ModelForm):
    class Meta:
        model = StockCage
        fields = "__all__"  # replace with your actual fields
