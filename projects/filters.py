import django_filters
from django import forms

from mouse_pilot_postgresql.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from mice_repository.models import Mouse


class ProjectFilter(django_filters.FilterSet):

    earmarks = (EARMARK_CHOICES_PAIRED[1:])

    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-5"}),
        label="Sex:",
    )
    earmark = django_filters.ChoiceFilter(
        choices=earmarks,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-3"}),
        label="Earmark: ",
    )

    class Meta:
        model = Mouse
        fields = ["sex", "earmark"]
