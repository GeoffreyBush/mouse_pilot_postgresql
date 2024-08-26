# Generated by Django 5.0.6 on 2024-08-26 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mouse',
            fields=[
                ('tube', models.IntegerField(blank=True, db_column='Tube', null=True)),
                ('_global_id', models.CharField(db_column='Global ID', max_length=20, primary_key=True, serialize=False)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], db_column='Sex', default='M', max_length=1)),
                ('dob', models.DateField(db_column='Date of Birth')),
                ('clipped_date', models.DateField(blank=True, db_column='Clipped Date', null=True)),
                ('earmark', models.CharField(choices=[('', 'Not Clipped'), ('TR', 'TR'), ('TL', 'TL'), ('BR', 'BR'), ('BL', 'BL'), ('TRTL', 'TRTL'), ('TRBR', 'TRBR'), ('TRTL', 'TRTL'), ('TLBR', 'TLBR'), ('TLBL', 'TLBL'), ('BRBL', 'BRBL')], db_column='Earmark', default='', max_length=4)),
                ('culled_date', models.DateField(blank=True, db_column='Culled Date', null=True)),
                ('coat', models.CharField(blank=True, db_column='Coat', default='', max_length=20, null=True)),
                ('result', models.CharField(blank=True, db_column='Result', default='', max_length=20, null=True)),
                ('fate', models.CharField(blank=True, db_column='Fate', default='', max_length=40, null=True)),
                ('cage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mice', to='website.cagemodel')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='father_mouse', to='mice_repository.mouse')),
            ],
            options={
                'db_table': 'mice',
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
