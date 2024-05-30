from django.db import models


# Create your models here.
class StockCage(models.Model):

    cage_id = models.AutoField(db_column="Cage ID", primary_key=True)

    def __str__(self):
        return f"{self.cage_id}"

    class Meta:
        managed = True
        db_table = "stockcage"
