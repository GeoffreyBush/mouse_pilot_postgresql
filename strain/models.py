from django.db import models


class Strain(models.Model):
    strain_name = models.CharField(db_column="Strain", primary_key=True, max_length=20)

    def __str__(self):
        return f"{self.strain_name}"

    class Meta:
        managed = True
        db_table = "strain"
