import datetime

import django_filters
from django import forms

from test_factories.constants import EARMARK_CHOICES_PAIRED


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


class ProjectFilter(django_filters.FilterSet):
    SEX_CHOICES = (
        ("F", "F"),
        ("M", "M"),
    )
    EARMARK_CHOICES_PAIRED = (
        ("TR", "TR"),
        ("TL", "TL"),
        ("BR", "BR"),
        ("BL", "BL"),
        ("TRTL", "TRTL"),
        ("TRBR", "TRBR"),
        ("TRTL", "TRTL"),
        ("TLBR", "TLBR"),
        ("TLBL", "TLBL"),
        ("BRBL", "BRBL"),
    )
    id = django_filters.CharFilter(
        widget=forms.TextInput(attrs={"class": "form-control w-25"}), label="Mouse ID: "
    )
    # Review how to use this filter with mouse.is_genotyped()
    """
    genotyped = django_filters.ChoiceFilter(
        choices=[(True, "True"), (False, "False")],
        empty_label="---",
        widget=forms.Select(attrs={"class": "form-control w-25"}),
        label="Genotyped: ",
    )
    """
    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        empty_label="---",
        widget=forms.Select(attrs={"class": "form-control w-25 ml-5"}),
        label="Sex:",
    )
    box_no = django_filters.CharFilter(
        widget=forms.TextInput(attrs={"class": "form-control w-25 ml-5"}),
        label="Cage: ",
        field_name="cage__box_no",
    )
    earmark = django_filters.ChoiceFilter(
        choices=EARMARK_CHOICES_PAIRED,
        empty_label="---",
        widget=forms.Select(attrs={"class": "form-control w-25 ml-3"}),
        label="Earmark: ",
    )
