from django.db import models


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

    def decrement_mice_count(self):
        if self.mice_count > 0:
            self.mice_count = self.mice_count - 1
            self.save(update_fields=["mice_count"])

    def __str__(self):
        return f"{self.strain_name}"

    class Meta:
        managed = True
        db_table = "strain"
