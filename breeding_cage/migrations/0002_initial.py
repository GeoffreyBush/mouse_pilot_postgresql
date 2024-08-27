# Generated by Django 5.0.6 on 2024-08-27 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("breeding_cage", "0001_initial"),
        ("mice_repository", "0001_initial"),
        ("strain", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="breedingcage",
            name="father",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cage_father",
                to="mice_repository.mouse",
            ),
        ),
        migrations.AddField(
            model_name="breedingcage",
            name="mother",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cage_mother",
                to="mice_repository.mouse",
            ),
        ),
        migrations.AddField(
            model_name="breedingcage",
            name="strain",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.PROTECT,
                to="strain.strain",
            ),
        ),
    ]
