# Generated by Django 5.0.6 on 2024-08-26 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('strain_name', models.CharField(db_column='Strain', max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'strain',
                'managed': True,
            },
        ),
    ]
