from django.core.exceptions import ValidationError
from django.db import models

from mice_repository.models import Mouse
from system_users.models import CustomUser


class Request(models.Model):

    TASK_CHOICES = [
        ("Clip", "Clip"),
        ("Cull", "Cull"),
    ]

    request_id = models.AutoField(db_column="ID", primary_key=True)
    requested_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, null=False, blank=False
    )
    task_type = models.CharField(max_length=10, choices=TASK_CHOICES, default="Clip")
    mice = models.ManyToManyField("mice_repository.Mouse", db_column="Mouse")

    confirmed = models.BooleanField(
        default=False,
    )  # confirmed attribute could be switched to flag with choices?

    # Need confirmed_by attribute. Could replace confirmed attribute with is_confirmed method

    # Break this ValidationErrors into validate_clip() and validate_cull() methods
    def confirm(self, earmark=None, date=None):
        if self.confirmed:
            raise ValidationError("Request is already confirmed")
        # This clip logic can be moved to a mouse method. Or a request method?
        if self.task_type == "Clip":
            if earmark is None:
                raise ValidationError("Earmark is required to confirm request")
            elif earmark not in [choice[0] for choice in Mouse.EARMARK_CHOICES_PAIRED]:
                raise ValidationError("Earmark is not valid")
            elif any([mouse.is_genotyped() for mouse in self.mice.all()]):
                raise ValidationError("A mouse in this clip request has already been clipped")
            else:
                for mouse in self.mice.all():
                    # Add clipped_date
                    # Add genotyper
                    mouse.earmark = earmark
                    mouse.save()

        elif self.task_type == "Cull":
            if any([mouse.is_culled() for mouse in self.mice.all()]):
                raise ValidationError("A mouse in this cull request has already been culled")
            else:
                for mouse in self.mice.all():
                    mouse.cull(date)

        else:
            raise ValidationError("Request type is not valid")
        
        self.confirmed = True
        self.save()

    def __str__(self):
        return f"{self.request_id}"

    class Meta:
        managed = True
        db_table = "request"
