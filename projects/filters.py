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

    @classmethod
    def get_filtered_project_mice(cls, project, http_request):
        project_mice = Mouse.objects.filter(project=project.pk).order_by("_global_id")
        if "search" in http_request.GET:
            filter_form = cls(http_request.GET, queryset=project_mice)
            return filter_form.qs
        return project_mice

    @classmethod
    def get_filter_form(cls, project, http_request):
        project_mice = Mouse.objects.filter(project=project.pk).order_by("_global_id")
        if "search" in http_request.GET:
            return cls(http_request.GET, queryset=project_mice)
        return cls(queryset=project_mice)

    class Meta:
        model = Mouse
        fields = ["sex", "earmark"]
