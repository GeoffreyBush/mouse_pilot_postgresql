from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from simple_history.models import HistoricalRecords


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "user"


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
        "Strain", on_delete=models.PROTECT, blank=False, null=False
    )
    _tube = models.CharField(db_column="Tube", primary_key=True, max_length=20)

    sex = models.CharField(
        db_column="Sex",
        max_length=1,
        default="M",
        choices=[("M", "Male"), ("F", "Female")],
        null=False,
    )
    dob = models.DateField(db_column="Date of Birth", null=False)

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

    # location = models.ForeignKey(
    #   "Cage", models.SET_NULL, db_column="Cage ID", null=True, blank=True
    # )

    project = models.ForeignKey(
        "Project", on_delete=models.PROTECT, null=True, blank=True
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
        "CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )

    history = HistoricalRecords()

    @property
    def tube(self):
        return self._tube

    def save(self, *args, **kwargs):
        if not self._tube:
            self.strain.increment_mice_count()
            self._tube = f"{self.strain.strain_name}-{self.strain.mice_count}"
        super().save(*args, **kwargs)
        self.refresh_from_db()

    def is_genotyped(self):
        return True if self.earmark != "" else False

    def __str__(self):
        return f"{self.tube}"

    class Meta:
        managed = True
        db_table = "mice"


class Request(models.Model):

    TASK_CHOICES = [
        ("Cl", "Clip"),
        ("Cu", "Cull"),
        ("Mo", "Move"),
        ("We", "Wean"),
    ]

    request_id = models.AutoField(db_column="ID", primary_key=True)
    researcher = models.ForeignKey(
        "CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )
    task_type = models.CharField(max_length=2, choices=TASK_CHOICES, default="Cl")

    # Should set constraints to have at least one mouse and delete if there are none
    mice = models.ManyToManyField("Mouse", db_column="Mouse")
    
    confirmed = models.BooleanField(
        default=False
    )  # confirmed attribute could be switched to flag with choices?
    new_message = models.CharField(max_length=1000, null=True, blank=True)
    message_history = models.CharField(max_length=10000, null=True, blank=True)

    def confirm(self):
        if not self.confirmed:
            self.confirmed = True
            self.save()

            if self.task_type == "Cl":
                for mouse in self.mice.all():
                    ###################################
                    """Need to update earmark here"""
                    ###################################
                    mouse.save()

            # Add other task types here

    def __str__(self):
        return f"{self.request_id}"

    class Meta:
        managed = True
        db_table = "request"


class Comment(models.Model):

    # Comment ID primary key is derived from Mouse ID primary key
    comment = models.OneToOneField("Mouse", on_delete=models.CASCADE, primary_key=True)

    # Django forces you to set a max_length property. Not sure if 500 characters is too much/enough.
    comment_text = models.CharField(
        db_column="Text", max_length=500, null=True, blank=True
    )

    def __str__(self):
        return f"{self.comment_id}"

    class Meta:
        managed = True
        db_table = "comment"


#################################################
# Models needed as foreign keys for Mouse model #
#################################################


class Strain(models.Model):
    strain_name = models.CharField(db_column="Strain", primary_key=True, max_length=20)
    mice_count = models.IntegerField(
        db_column="Mice Count", default=0, null=False, blank=False
    )

    def increment_mice_count(self):
        self.mice_count = F("mice_count") + 1
        self.save(update_fields=["mice_count"])
        self.refresh_from_db()

    def __str__(self):
        return f"{self.strain_name}"

    class Meta:
        managed = True
        db_table = "strain"


class Project(models.Model):
    project_name = models.CharField(db_column="Name", primary_key=True, max_length=30)
    research_area = models.CharField(
        db_column="Research Area", max_length=50, null=True, blank=True
    )
    strains = models.ManyToManyField("Strain", db_column="Strain")
    researchers = models.ManyToManyField(CustomUser)

    # Rework how mice_count is calculated. Currently done in views.py.
    # Should be whenever a mouse is added to a project.
    mice_count = 0

    def __str__(self):
        return f"{self.project_name}"

    class Meta:
        managed = True
        db_table = "project"


class BreedingCage(models.Model):
    """Could benefit from tracking when the breeding pair was put in the cage"""

    box_no = models.CharField(db_column="Box Number", max_length=10, primary_key=True)
    mother = models.ForeignKey(
        "Mouse",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="mother_breedingcage",
    )
    father = models.ForeignKey(
        "Mouse",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="father_breedingcage",
    )
    date_born = models.DateField(db_column="DBorn", null=True, blank=True, default=None)
    number_born = models.CharField(
        db_column="NBorn", max_length=5, null=True, blank=True, default=None
    )
    cull_to = models.CharField(
        db_column="C/To", max_length=20, null=True, blank=True, default=None
    )
    date_wean = models.DateField(db_column="Dwean", null=True, blank=True, default=None)
    number_wean = models.CharField(
        db_column="Nwean", max_length=5, null=True, blank=True, default=None
    )
    pwl = models.CharField(
        db_column="PWL", max_length=5, null=True, blank=True, default=None
    )

    def move_to_stock(self):
        pass

    def __str__(self):
        return f"{self.box_no}"

    class Meta:
        managed = True
        db_table = "breedingcage"
