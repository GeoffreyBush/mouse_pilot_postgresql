# Generated by Django 5.0.6 on 2024-06-11 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockCage',
            fields=[
                ('cage_id', models.AutoField(db_column='Cage ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'stockcage',
                'managed': True,
            },
        ),
    ]
