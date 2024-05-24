from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import BreedingCage, Comment, CustomUser, Mice, Project, Strain


# Changes what attributes are displayed and which attributes you can filter by in admin page
@admin.register(Mice)
class MiceAdmin(admin.ModelAdmin):
    list_display = ("clippedDate", "genotyped")


# Add custom admin class to admin page
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username"]


# Register your models here.
admin.site.register(Project)
admin.site.register(BreedingCage)
admin.site.register(Strain)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comment)
