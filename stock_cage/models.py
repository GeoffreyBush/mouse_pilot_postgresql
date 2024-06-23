from website.models import CageModel

class StockCage(CageModel):

    class Meta:
        managed = True
        db_table = "stockcage"
