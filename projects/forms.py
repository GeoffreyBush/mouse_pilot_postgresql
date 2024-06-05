from django import forms

from projects.models import Project
from system_users.models import CustomUser
from website.models import Strain

class NewProjectForm(forms.ModelForm):
    
    project_name = forms.CharField(max_length=30)
    research_area = forms.CharField(max_length=50, required=False)
    strains = forms.ModelMultipleChoiceField(queryset=Strain.objects.all(), widget=forms.CheckboxSelectMultiple)
    researchers = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Project
        fields = "__all__"