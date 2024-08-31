# Generated by Django 5.0.6 on 2024-08-31 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CageModel",
            fields=[
                (
                    "cage_id",
                    models.AutoField(
                        db_column="Cage ID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "box_no",
                    models.CharField(
                        db_column="Box Number",
                        default="Unnamed",
                        max_length=10,
                        unique=True,
                    ),
                ),
            ],
            options={
                "db_table": "basecage",
                "managed": True,
            },
        ),
    ]
