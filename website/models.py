from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "user"


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
    mice = models.ManyToManyField("mice_repository.Mouse", db_column="Mouse")

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
    comment = models.OneToOneField(
        "mice_repository.Mouse", on_delete=models.CASCADE, primary_key=True
    )

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

    # Could use F() expressions for incremenet and decrement for better DB concurrency 
    def increment_mice_count(self):
        self.mice_count = self.mice_count + 1
        self.save(update_fields=["mice_count"])
        self.refresh_from_db()

    def decrement_mice_count(self):
        if self.mice_count > 0:
            self.mice_count = self.mice_count - 1
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
