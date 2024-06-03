import django_filters
from django import forms

from mouse_pilot_postgresql.constants import SEX_CHOICES, EARMARK_CHOICES_PAIRED

class ProjectFilter(django_filters.FilterSet):

    earmarks = EARMARK_CHOICES_PAIRED[1:],

    sex = django_filters.ChoiceFilter(
        choices=SEX_CHOICES,
        #empty_label="---------",
        widget=forms.Select(attrs={"class": "form-select w-25 ml-5"}),
        label="Sex:",
    )
    earmark = django_filters.ChoiceFilter(
        
        choices = EARMARK_CHOICES_PAIRED,
        widget=forms.Select(attrs={"class": "form-select w-25 ml-3"}),
        label="Earmark: ",
    )
