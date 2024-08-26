from datetime import date, timedelta

import django_filters
from django import forms

from main.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES
from mice_repository.models import Mouse
from strain.models import Strain


class MouseFilter(django_filters.FilterSet):

    earmarks = EARMARK_CHOICES_PAIRED[1:]

    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-select col-12 mb-1"}),
        label="Sex:",
        initial="",
    )

    strain = django_filters.ModelChoiceFilter(
        queryset=Strain.objects.all(),
        widget=forms.Select(attrs={"class": "form-select col-12 mb-1"}),
        label="Strain:",
    )

    earmark = django_filters.ChoiceFilter(
        choices=earmarks,
        widget=forms.Select(attrs={"class": "form-select col-12 mb-1"}),
        label="Earmark:",
        initial="",
    )

    min_age = django_filters.NumberFilter(
        method="filter_min_age",
        widget=forms.NumberInput(attrs={"class": "form-control col-12 mb-1"}),
        label="Min Age:",
    )

    max_age = django_filters.NumberFilter(
        method="filter_max_age",
        widget=forms.NumberInput(attrs={"class": "form-control col-12 mb-1"}),
        label="Max Age:",
    )

    def filter_min_age(self, queryset, name, value):
        return queryset.filter(dob__lte=date.today() - timedelta(days=int(value)))

    def filter_max_age(self, queryset, name, value):
        return queryset.filter(dob__gte=date.today() - timedelta(days=int(value)))

    # Override __init__() so that it accepts a project parameter
    # Used for showing only strains associated with that project on the filter form
    def __init__(
        self, data=None, queryset=None, *, request=None, prefix=None, project=None
    ):
        super().__init__(data, queryset, request=request, prefix=prefix)
        if project:
            self.filters["strain"].queryset = project.strains.all()

    @classmethod
    def get_filtered_mice(cls, mice_qs, http_request):
        if "search" in http_request.GET:
            filter_form = cls(http_request.GET, queryset=mice_qs)
            return filter_form.qs
        return mice_qs

    @classmethod
    def get_filter_form(cls, mice_qs, http_request, project=None):
        if "search" in http_request.GET:
            return cls(http_request.GET, queryset=mice_qs, project=project)
        return cls(queryset=mice_qs, project=project)

    class Meta:
        model = Mouse
        fields = ["sex", "strain", "earmark", "min_age", "max_age"]
