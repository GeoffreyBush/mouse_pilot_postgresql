import datetime

import django_filters
from django import forms

from mouse_pilot_postgresql.constants import EARMARK_CHOICES_PAIRED


# This filter doesn't meet requirements - will only filter mice born on a specific date, not a range
class CustomDateTimeWidget(forms.widgets.SelectDateWidget):
    def __init__(self, years=None, months=None, empty_label="---", attrs=None):
        if attrs is None:
            attrs = {}
        attrs.setdefault("class", "mr-2")
        if years is None:
            years = range(
                datetime.date.today().year - 100, datetime.date.today().year + 100
            )
        super().__init__(
            years=years, months=months, empty_label=empty_label, attrs=attrs
        )


class BWFilter(django_filters.FilterSet):
    SEX_CHOICES = (
        ("F", "F"),
        ("M", "M"),
    )

    id = django_filters.CharFilter(
        widget=forms.TextInput(attrs={"class": "form-control w-25"}), label="Mouse ID: "
    )
    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        empty_label="---",
        widget=forms.Select(attrs={"class": "form-control w-25"}),
        label="Sex: ",
    )
    earmark = django_filters.ChoiceFilter(
        choices=EARMARK_CHOICES_PAIRED,
        empty_label="---",
        widget=forms.Select(attrs={"class": "form-control w-25"}),
        label="Earmark: ",
    )
