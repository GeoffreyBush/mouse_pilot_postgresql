from django.db import models

from system_users.models import CustomUser


class Project(models.Model):
    project_name = models.CharField(db_column="Name", primary_key=True, max_length=30)
    research_area = models.CharField(
        db_column="Research Area", max_length=50, null=True, blank=True
    )
    strains = models.ManyToManyField("website.Strain", db_column="Strain")
    researchers = models.ManyToManyField(CustomUser)

    def __str__(self):
        return f"{self.project_name}"

    class Meta:
        managed = True
        db_table = "project"
