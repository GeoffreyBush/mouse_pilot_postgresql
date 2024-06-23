# Generated by Django 5.0.6 on 2024-06-23 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mice_repository', '0001_initial'),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mouse',
            name='cage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mice', to='website.cagemodel'),
        ),
        migrations.AddField(
            model_name='mouse',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='father_mouse', to='mice_repository.mouse'),
        ),
    ]
