# Generated by Django 5.0.6 on 2024-06-23 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mice_repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CageModel',
            fields=[
                ('cage_id', models.AutoField(db_column='Cage ID', primary_key=True, serialize=False)),
                ('box_no', models.CharField(db_column='Box Number', default='Unnamed', max_length=10, unique=True)),
            ],
            options={
                'db_table': 'basecage',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MouseComment',
            fields=[
                ('comment_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mice_repository.mouse')),
                ('comment_text', models.CharField(blank=True, db_column='Text', default='', max_length=400, null=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': True,
            },
        ),
    ]
