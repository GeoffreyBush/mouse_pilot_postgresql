from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from main.constants import EARMARK_CHOICES_PAIRED


class CustomManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def alive(self):
        return self.filter(culled_date__isnull=True)

    def culled(self):
        return self.filter(culled_date__isnull=False)

    def weaned_lt_2_months_old(self):
        return self.filter()

    def between_2_6_months_old(self):
        pass

    def between_6_12_months_old(self):
        pass

    def between_12_24_months_old(self):
        pass


class Mouse(models.Model):

    # When you call Mouse.objects, it will redirect to MortalityManager instead of default Manager
    objects = CustomManager()

    strain = models.ForeignKey(
        "strain.Strain",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="mice",
    )
    tube = models.IntegerField(db_column="Tube", blank=True, null=True)
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

    cage = models.ForeignKey(
        "common.CageModel",
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

    culled_date = models.DateField(db_column="Culled Date", null=True, blank=True)

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

    @property
    def age_days(self):
        return (date.today() - self.dob).days

    @property
    def age_months(self):
        return (date.today() - self.dob).days / 30

    def cull(self, culled_date):
        if self.is_culled():
            raise ValidationError("Mouse has already been culled")
        else:
            self.culled_date = culled_date
            self.save()

    # tube can be set manually or is set automatically using strain.mice.count(). tube value then used to set _global_id
    def clean(self):
        super().clean()
        new_tube = self.strain.mice.count()
        if self.tube is None:
            self.tube = new_tube + 1
        if not self._global_id:
            self._global_id = f"{self.strain.strain_name}-{self.tube}"
        try:
            self.validate_unique()
        except ValidationError as e:
            raise ValidationError(e)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def is_genotyped(self):
        return self.earmark != ""

    def is_culled(self):
        return self.culled_date is not None

    def __str__(self):
        return f"{self._global_id}"

    class Meta:
        managed = True
        base_manager_name = "objects"
        db_table = "mice"


class MouseComment(models.Model):

    comment_id = models.OneToOneField(
        "mice_repository.Mouse", on_delete=models.CASCADE, primary_key=True
    )

    comment_text = models.CharField(
        db_column="Text", max_length=400, null=True, blank=True, default=""
    )

    def __str__(self):
        return f"{self.comment_id}"

    class Meta:
        managed = True
        db_table = "comment"
