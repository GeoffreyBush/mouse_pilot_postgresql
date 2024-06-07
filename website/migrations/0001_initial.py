# Generated by Django 5.0.6 on 2024-06-07 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mice_repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mice_repository.mouse')),
                ('comment_text', models.CharField(blank=True, db_column='Text', max_length=500, null=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('strain_name', models.CharField(db_column='Strain', max_length=20, primary_key=True, serialize=False)),
                ('mice_count', models.IntegerField(db_column='Mice Count', default=0)),
            ],
            options={
                'db_table': 'strain',
                'managed': True,
            },
        ),
    ]
