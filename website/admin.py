from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mice_repository.models import Mouse
from projects.models import Project
from stock_cage.models import StockCage
from strain.models import Strain
from system_users.forms import CustomUserChangeForm, CustomUserCreationForm
from system_users.models import CustomUser
from mice_repository.models import MouseComment


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
admin.site.register(MouseComment)
admin.site.register(StockCage)
