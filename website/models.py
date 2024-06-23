from django.db import models


class CageModel(models.Model):

    cage_id = models.AutoField(db_column="Cage ID", primary_key=True)
    box_no = models.CharField(
        db_column="Box Number",
        max_length=10,
        null=False,
        blank=False,
        default="Unnamed",
        unique=True,
    )

    def __str__(self):
        return f"{self.box_no}"
    
    class Meta:
        managed = True
        db_table = "basecage"

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
