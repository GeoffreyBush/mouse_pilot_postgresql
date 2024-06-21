import django_filters
from django import forms

from mice_repository.models import Mouse
from mouse_pilot_postgresql.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES


class ProjectFilter(django_filters.FilterSet):

    earmarks = EARMARK_CHOICES_PAIRED[1:]

    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-5"}),
        label="Sex:",
        initial="",
    )
    earmark = django_filters.ChoiceFilter(
        choices=earmarks,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-3"}),
        label="Earmark:",
        initial="",
    )

    class Meta:
        model = Mouse
        fields = ["sex", "earmark"]
