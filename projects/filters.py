import django_filters
from django import forms

from mouse_pilot_postgresql.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES

class ProjectFilter(django_filters.FilterSet):

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