# Generated by Django 5.0.6 on 2024-08-02 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mouse",
            fields=[
                ("tube", models.IntegerField(blank=True, db_column="Tube", null=True)),
                (
                    "_global_id",
                    models.CharField(
                        db_column="Global ID",
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        db_column="Sex",
                        default="M",
                        max_length=1,
                    ),
                ),
                ("dob", models.DateField(db_column="Date of Birth")),
                (
                    "clipped_date",
                    models.DateField(blank=True, db_column="Clipped Date", null=True),
                ),
                (
                    "earmark",
                    models.CharField(
                        choices=[
                            ("", "Not Clipped"),
                            ("TR", "TR"),
                            ("TL", "TL"),
                            ("BR", "BR"),
                            ("BL", "BL"),
                            ("TRTL", "TRTL"),
                            ("TRBR", "TRBR"),
                            ("TRTL", "TRTL"),
                            ("TLBR", "TLBR"),
                            ("TLBL", "TLBL"),
                            ("BRBL", "BRBL"),
                        ],
                        db_column="Earmark",
                        default="",
                        max_length=4,
                    ),
                ),
                (
                    "culled_date",
                    models.DateField(blank=True, db_column="Culled Date", null=True),
                ),
                (
                    "coat",
                    models.CharField(
                        blank=True,
                        db_column="Coat",
                        default="",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "result",
                    models.CharField(
                        blank=True,
                        db_column="Result",
                        default="",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "fate",
                    models.CharField(
                        blank=True,
                        db_column="Fate",
                        default="",
                        max_length=40,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "mice",
                "managed": True,
            },
        ),
    ]
