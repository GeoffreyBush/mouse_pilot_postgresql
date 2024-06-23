# Generated by Django 5.0.6 on 2024-06-23 20:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(db_column='Name', default='My Project', max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('research_area', models.CharField(blank=True, db_column='Research Area', max_length=50, null=True)),
            ],
            options={
                'db_table': 'project',
                'managed': True,
            },
        ),
    ]
