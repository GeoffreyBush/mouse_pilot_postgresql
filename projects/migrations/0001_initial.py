# Generated by Django 4.2.6 on 2024-06-04 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "project_name",
                    models.CharField(
                        db_column="Name",
                        max_length=30,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "research_area",
                    models.CharField(
                        blank=True, db_column="Research Area", max_length=50, null=True
                    ),
                ),
            ],
            options={
                "db_table": "project",
                "managed": True,
            },
        ),
    ]
