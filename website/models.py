from django.db import models


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
