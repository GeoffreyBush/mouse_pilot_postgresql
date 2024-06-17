from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


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
        "strain.Strain", on_delete=models.PROTECT, blank=False, null=False
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

    stock_cage = models.ForeignKey(
        "stock_cage.StockCage",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mice",
    )

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

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mice",
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
        "system_users.CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )

    """ Add history back in the future. Error across multiple areas """
    # history = HistoricalRecords()

    coat = models.CharField(
        db_column="Coat", max_length=20, null=True, blank=True, default=""
    )

    # Result could be a set of choices?
    result = models.CharField(
        db_column="Result", max_length=20, null=True, blank=True, default=""
    )

    fate = models.CharField(
        db_column="Fate", max_length=40, null=True, blank=True, default=""
    )

    culled = models.BooleanField(default=False)

    @property
    def tube(self):
        return self._tube

    @property
    def age(self):
        return (date.today() - self.dob).days

    def cull(self):
        if self.culled:
            raise ValidationError("Mouse has already been culled")
        else:
            self.culled = True
            self.save()

    # Custom tube can be set or is set automatically using strain.mice_count. Tube value then used to set _global_id
    # This logic cannot be placed in clean()
    def save(self, *args, **kwargs):
        self.strain.increment_mice_count()
        if self._tube is None:
            self._tube = self.strain.mice_count
        if not self._global_id:
            self._global_id = f"{self.strain.strain_name}-{self._tube}"

        try:
            self.validate_unique()
        except ValidationError as e:
            self.strain.decrement_mice_count()
            raise ValidationError(e)
        super().save(*args, **kwargs)

    def is_genotyped(self):
        return True if self.earmark != "" else False

    def __str__(self):
        return f"{self._global_id}"

    class Meta:
        managed = True
        db_table = "mice"
