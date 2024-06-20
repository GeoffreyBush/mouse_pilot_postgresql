# Generated by Django 5.0.6 on 2024-06-20 09:23

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
                ('mice_count', models.IntegerField(db_column='Mice Count', default=0)),
            ],
            options={
                'db_table': 'strain',
                'managed': True,
            },
        ),
    ]
