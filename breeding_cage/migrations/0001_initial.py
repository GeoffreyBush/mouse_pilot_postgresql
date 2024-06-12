# Generated by Django 5.0.6 on 2024-06-12 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BreedingCage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_no', models.CharField(db_column='Box Number', default='Unnamed', max_length=10, unique=True)),
                ('date_born', models.DateField(blank=True, db_column='DBorn', default=None, null=True)),
                ('number_born', models.IntegerField(blank=True, db_column='NBorn', default=0, null=True)),
                ('cull_to', models.CharField(blank=True, db_column='C/To', default='', max_length=20, null=True)),
                ('date_wean', models.DateField(blank=True, db_column='Dwean', default=None, null=True)),
                ('number_wean', models.CharField(blank=True, db_column='Nwean', default='', max_length=5, null=True)),
                ('pwl', models.CharField(blank=True, db_column='PWL', default='', max_length=5, null=True)),
                ('male_pups', models.IntegerField(blank=True, db_column='Male Pups', default=0, null=True)),
                ('female_pups', models.IntegerField(blank=True, db_column='Female Pups', default=0, null=True)),
                ('transferred_to_stock', models.BooleanField(db_column='Moved to Stock', default=False)),
            ],
            options={
                'db_table': 'breedingcage',
                'managed': True,
            },
        ),
    ]
