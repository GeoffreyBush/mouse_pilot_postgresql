from django.db import models

from mice_repository.models import Mouse
from website.models import StockCage


# Create your models here.
class BreedingCage(models.Model):
    """Could benefit from tracking when the breeding pair was put in the cage"""

    box_no = models.CharField(
        db_column="Box Number",
        max_length=10,
        null=False,
        blank=False,
        default="Unnamed",
        unique=True,
    )
    mother = models.ForeignKey(
        "mice_repository.Mouse",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="mother_breeding_cage",
    )
    father = models.ForeignKey(
        "mice_repository.Mouse",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="father_breeding_cage",
    )
    date_born = models.DateField(db_column="DBorn", null=True, blank=True, default=None)
    number_born = models.IntegerField(
        db_column="NBorn", null=True, blank=True, default=0
    )
    cull_to = models.CharField(
        db_column="C/To", max_length=20, null=True, blank=True, default=""
    )
    date_wean = models.DateField(db_column="Dwean", null=True, blank=True, default=None)
    number_wean = models.CharField(
        db_column="Nwean", max_length=5, null=True, blank=True, default=""
    )
    pwl = models.CharField(
        db_column="PWL", max_length=5, null=True, blank=True, default=""
    )
    male_pups = models.IntegerField(
        db_column="Male Pups", null=True, blank=True, default=0
    )
    female_pups = models.IntegerField(
        db_column="Female Pups", null=True, blank=True, default=0
    )
    transferred_to_stock = models.BooleanField(
        db_column="Moved to Stock", default=False
    )

    def convert_pup_to_mouse(self, sex, stock_cage):
        mouse = Mouse.objects.create(
            strain=self.mother.strain,
            sex=sex,
            stock_cage=stock_cage,
            dob=self.date_born,
            mother=self.mother,
            father=self.father,
            # Add project?
        )
        mouse.save()
        mouse.refresh_from_db()

    # Need to be able to set a custom tube number to start from for transfer to stock
    # Default is to start from the next available tube number
    # Need a form to set individual tube numbers for each pup
    def transfer_to_stock(self):
        if not self.transferred_to_stock:
            stock_cage = StockCage.objects.create()

            for _ in range(self.male_pups):
                self.convert_pup_to_mouse("M", stock_cage)

            for _ in range(self.female_pups):
                self.convert_pup_to_mouse("F", stock_cage)

        self.transferred_to_stock = True
        self.save()
        self.refresh_from_db()
        return stock_cage

    def __str__(self):
        return f"{self.box_no}"

    class Meta:
        managed = True
        db_table = "breedingcage"
