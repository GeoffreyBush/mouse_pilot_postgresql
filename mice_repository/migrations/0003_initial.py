# Generated by Django 5.0.6 on 2024-06-23 22:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mice_repository", "0002_initial"),
        ("projects", "0001_initial"),
        ("strain", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="mouse",
            name="genotyper",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="mouse",
            name="mother",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mother_mouse",
                to="mice_repository.mouse",
            ),
        ),
        migrations.AddField(
            model_name="mouse",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mice",
                to="projects.project",
            ),
        ),
        migrations.AddField(
            model_name="mouse",
            name="strain",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mice",
                to="strain.strain",
            ),
        ),
    ]
