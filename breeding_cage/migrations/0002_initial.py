# Generated by Django 5.0.6 on 2024-05-30 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('breeding_cage', '0001_initial'),
        ('mice_repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breedingcage',
            name='father',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='father_breeding_cage', to='mice_repository.mouse'),
        ),
        migrations.AddField(
            model_name='breedingcage',
            name='mother',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mother_breeding_cage', to='mice_repository.mouse'),
        ),
    ]
