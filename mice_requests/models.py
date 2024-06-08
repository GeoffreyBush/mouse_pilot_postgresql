from django.core.exceptions import ValidationError
from django.db import models

from system_users.models import CustomUser


class Request(models.Model):

    TASK_CHOICES = [
        ("Clip", "Clip"),
        ("Cull", "Cull"),
        ("Move", "Move"),
        ("Wean", "Wean"),
    ]

    request_id = models.AutoField(db_column="ID", primary_key=True)
    requested_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, null=False, blank=False
    )
    task_type = models.CharField(max_length=10, choices=TASK_CHOICES, default="Clip")
    mice = models.ManyToManyField("mice_repository.Mouse", db_column="Mouse")

    confirmed = models.BooleanField(
        default=False
    )  # confirmed attribute could be switched to flag with choices?

    # Message system is not robust enough
    new_message = models.CharField(max_length=1000, null=True, blank=True)
    message_history = models.CharField(max_length=10000, null=True, blank=True)

    def confirm_clip(self, earmark):
        if earmark is None:
            raise ValidationError("Earmark is required to confirm request")
        elif self.confirmed:
            raise ValidationError("Request is already confirmed")
        else:
            self.confirmed = True
            self.save()
            for mouse in self.mice.all():
                mouse.earmark = earmark
                mouse.save()

    def __str__(self):
        return f"{self.request_id}"

    class Meta:
        managed = True
        db_table = "request"
