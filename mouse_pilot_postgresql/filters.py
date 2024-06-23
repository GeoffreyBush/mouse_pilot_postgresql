import django_filters
from django import forms

from mice_repository.models import Mouse
from mouse_pilot_postgresql.constants import EARMARK_CHOICES_PAIRED, SEX_CHOICES


class MouseFilter(django_filters.FilterSet):

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
        fields = ["sex", "earmark"]
