# Generated by Django 5.0.6 on 2024-05-30 21:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mice_repository', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('task_type', models.CharField(choices=[('Cl', 'Clip'), ('Cu', 'Cull'), ('Mo', 'Move'), ('We', 'Wean')], default='Cl', max_length=2)),
                ('confirmed', models.BooleanField(default=False)),
                ('new_message', models.CharField(blank=True, max_length=1000, null=True)),
                ('message_history', models.CharField(blank=True, max_length=10000, null=True)),
                ('mice', models.ManyToManyField(db_column='Mouse', to='mice_repository.mouse')),
                ('researcher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'request',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_name', models.CharField(db_column='Name', max_length=30, primary_key=True, serialize=False)),
                ('research_area', models.CharField(blank=True, db_column='Research Area', max_length=50, null=True)),
                ('researchers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('strains', models.ManyToManyField(db_column='Strain', to='website.strain')),
            ],
            options={
                'db_table': 'project',
                'managed': True,
            },
        ),
    ]
