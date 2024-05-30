from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "user"
