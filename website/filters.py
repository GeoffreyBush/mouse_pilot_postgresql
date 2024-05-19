import datetime

import django_filters
from django import forms

from website.constants import EARMARK_CHOICES


# filters for BW cage view
# variable name have to follow the model otherwise won't display properly
class CustomDateTimeWidget(forms.widgets.SelectDateWidget):
    def __init__(self, years=None, months=None, empty_label="---", attrs=None):
        if attrs is None:
            attrs = {}
        attrs.setdefault("style", "")
        attrs["style"] += "margin-right: 2px;"
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
        widget=forms.TextInput(attrs={"style": "width: 60px;"}), label="Mouse ID: "
    )
    dob = django_filters.DateTimeFilter(
        widget=CustomDateTimeWidget(attrs={}), field_name="dob", label="Date of birth: "
    )
    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        empty_label="---",
        widget=forms.Select(attrs={"style": "width: 60px;"}),
        label="Sex: ",
    )
    earmark = django_filters.ChoiceFilter(
        choices=EARMARK_CHOICES,
        empty_label="---",
        widget=forms.Select(attrs={"style": "width: 60px;"}),
        label="Earmark: ",
    )


class ProjectFilter(django_filters.FilterSet):
    SEX_CHOICES = (
        ("F", "F"),
        ("M", "M"),
    )
    EARMARK_CHOICES = (
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
        widget=forms.TextInput(attrs={"style": "width: 70px;"}), label="Mouse ID: "
    )
    genotyped = django_filters.ChoiceFilter(
        choices=[(True, "True"), (False, "False")],
        empty_label="---",
        widget=forms.Select(attrs={"style": "width: 70px;"}),
        label="Genotyped: ",
    )
    dob = django_filters.DateTimeFilter(
        widget=CustomDateTimeWidget(attrs={}), field_name="dob", label="Date of birth: "
    )
    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        empty_label="---",
        widget=forms.Select(attrs={"style": "margin-left: 45px; width: 70px;"}),
        label="Sex:",
    )
    # cage = django_filters.CharFilter(
    #     widget = forms.TextInput(attrs={'style': 'margin-left: 45px; width: 70px;'}),
    #     label = "Cage: "
    # )
    box_no = django_filters.CharFilter(
        widget=forms.TextInput(attrs={"style": "margin-left: 45px; width: 70px;"}),
        label="Cage: ",
        field_name="cage__box_no",
    )
    earmark = django_filters.ChoiceFilter(
        choices=EARMARK_CHOICES,
        empty_label="---",
        widget=forms.Select(attrs={"style": "margin-left: 32px; width: 97px;"}),
        label="Earmark: ",
    )


# class CageFilter(django_filters.FilterSet):
#     cage = django_filters.CharFilter(
#         widget = forms.TextInput(attrs={'style': 'margin-left: 45px; width: 70px;'}),
#         label = "Cage: ",
#         field_name='Cage__box_no'
#     )
#     class Meta:
#         model = Mice
#         fields = ['cage']
