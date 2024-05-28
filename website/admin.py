from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import  Comment, CustomUser, Mouse, Project, Strain


# Changes what attributes are displayed and which attributes you can filter by in admin page
@admin.register(Mouse)
class MiceAdmin(admin.ModelAdmin):
    list_display = ("clipped_date", "strain")


# Add custom admin class to admin page
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username"]


# Register your models here.
admin.site.register(Project)
admin.site.register(Strain)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comment)
