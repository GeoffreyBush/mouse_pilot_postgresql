from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Mouse(models.Model):

    EARMARK_CHOICES_PAIRED = [
        ("", ""),
        ("TR", "TR"),
        ("TL", "TL"),
        ("BR", "BR"),
        ("BL", "BL"),
        ("TRTL", "TRTL"),
        ("TRBR", "TRBR"),
        ("TRTL", "TRTL"),
        ("TLBR", "TLBR"),
        ("TLBL", "TLBL"),
        ("BRBL", "BRBL"),
    ]
    strain = models.ForeignKey(
        "website.Strain", on_delete=models.PROTECT, blank=False, null=False
    )
    _tube = models.IntegerField(db_column="Tube", blank=True, null=True)
    _global_id = models.CharField(
        db_column="Global ID", max_length=20, primary_key=True
    )
    sex = models.CharField(
        db_column="Sex",
        max_length=1,
        default="M",
        choices=[("M", "Male"), ("F", "Female")],
        null=False,
    )
    dob = models.DateField(db_column="Date of Birth", null=False, blank=False)

    # Culled boolean attribute will be useful

    mother = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mother_mouse",
    )
    father = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="father_mouse",
    )

    stock_cage = models.ForeignKey(
        "website.StockCage",
        on_delete=models.SET_NULL,
        db_column="Stock Cage ID",
        null=True,
        blank=True,
        default=None,
        related_name="mice",
    )

    project = models.ForeignKey(
        "website.Project", on_delete=models.PROTECT, null=True, blank=True
    )

    clipped_date = models.DateField(db_column="Clipped Date", null=True, blank=True)
    earmark = models.CharField(
        db_column="Earmark",
        max_length=4,
        default="",
        choices=EARMARK_CHOICES_PAIRED,
        null=False,
    )
    genotyper = models.ForeignKey(
        "website.CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )

    """ Add history back in the future. Error across multiple areas """
    # history = HistoricalRecords()

    coat = models.CharField(
        db_column="Coat", max_length=20, null=True, blank=True, default=""
    )

    # Think result should be a set of choices
    result = models.CharField(
        db_column="Result", max_length=20, null=True, blank=True, default=""
    )

    fate = models.CharField(
        db_column="Fate", max_length=40, null=True, blank=True, default=""
    )

    @property
    def tube(self):
        return self._tube

    @tube.setter
    def tube(self, value):
        self._tube = value

    # Custom tube can be set or is set automatically. Tube value then used to set _global_id
    def save(self, *args, **kwargs):
        self.strain.increment_mice_count()
        if self._tube is None:
            self._tube = self.strain.mice_count
        if not self._global_id:
            self._global_id = f"{self.strain.strain_name}-{self._tube}"

        # If the new _global_id is not unique, revert the strain mice count and raise ValidationError    
        try: 
            self.validate_unique()
        except ValidationError as e:
            self.strain.decrement_mice_count()
            raise ValidationError(e)
        
        super().save(*args, **kwargs)
        self.refresh_from_db()

    def is_genotyped(self):
        return True if self.earmark != "" else False

    def __str__(self):
        return f"{self._global_id}"

    class Meta:
        managed = True
        db_table = "mice"
