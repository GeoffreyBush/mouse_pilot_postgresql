from datetime import date, timedelta

import django_filters
from django import forms

from strain.models import Strain
from main.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from mice_repository.models import Mouse


class MouseFilter(django_filters.FilterSet):

    earmarks = EARMARK_CHOICES_PAIRED[1:]

    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-5"}),
        label="Sex:",
        initial="",
    )

    strain = django_filters.ModelChoiceFilter(
        queryset=Strain.objects.all(),
        widget=forms.Select(attrs={"class": "form-select w-25 ml3"}),
        label="Strain:",
    )

    earmark = django_filters.ChoiceFilter(
        choices=earmarks,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-3"}),
        label="Earmark:",
        initial="",
    )

    min_age = django_filters.NumberFilter(
        method="filter_min_age",
        widget=forms.NumberInput(attrs={"class": "form-control w-25 ml-5"}),
        label="Min Age:",
    )

    max_age = django_filters.NumberFilter(
        method="filter_max_age",
        widget=forms.NumberInput(attrs={"class": "form-control w-25 ml-3"}),
        label="Max Age:",
    )

    def filter_min_age(self, queryset, name, value):
        return queryset.filter(dob__lte=date.today() - timedelta(days=int(value)))

    def filter_max_age(self, queryset, name, value):
        return queryset.filter(dob__gte=date.today() - timedelta(days=int(value)))

    @classmethod
    def get_filtered_mice(cls, mice_qs, http_request):
        if "search" in http_request.GET:
            filter_form = cls(http_request.GET, queryset=mice_qs)
            return filter_form.qs
        return mice_qs

    @classmethod
    def get_filter_form(cls, mice_qs, http_request):
        if "search" in http_request.GET:
            return cls(http_request.GET, queryset=mice_qs)
        return cls(queryset=mice_qs)

    class Meta:
        model = Mouse
        fields = ["sex", "strain", "earmark", "min_age", "max_age"]
