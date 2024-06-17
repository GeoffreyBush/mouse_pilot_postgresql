from django.core.validators import MinLengthValidator
from django.db import models

from system_users.models import CustomUser


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(
        db_column="Name",
        blank=False,
        null=False,
        default="My Project",
        unique=True,
        validators=[MinLengthValidator(3)],
        max_length=30,
    )
    research_area = models.CharField(
        db_column="Research Area", max_length=50, null=True, blank=True
    )
    strains = models.ManyToManyField("strain.Strain", db_column="Strain")
    researchers = models.ManyToManyField(CustomUser)

    def __str__(self):
        return f"{self.project_name}"

    class Meta:
        managed = True
        db_table = "project"
