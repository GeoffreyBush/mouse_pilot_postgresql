from django.db import models

from website.models import CageModel

# Need to track whether female is pregnant


class BreedingCage(CageModel):
    """Could benefit from tracking when the breeding pair was put in the cage"""

    strain = models.ForeignKey(
        "strain.Strain",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        default="",
    )
    mother = models.ForeignKey(
        "mice_repository.Mouse",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="cage_mother",
    )
    father = models.ForeignKey(
        "mice_repository.Mouse",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="cage_father",
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

    # Used to define immutable values for PupsToStockCageFormSet in wean_pups app
    def get_initial_data_for_pups(self):
        initial_data = []
        for sex, count in [("M", self.male_pups), ("F", self.female_pups)]:
            initial_data += [
                {
                    "sex": sex,
                    "strain": self.strain,
                    "mother": self.mother,
                    "father": self.father,
                    "dob": self.date_born,
                }
                for _ in range(count)
            ]
        return initial_data

    class Meta:
        managed = True
        db_table = "breedingcage"
