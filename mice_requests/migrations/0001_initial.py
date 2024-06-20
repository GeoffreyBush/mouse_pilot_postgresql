# Generated by Django 5.0.6 on 2024-06-20 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mice_repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('task_type', models.CharField(choices=[('Clip', 'Clip'), ('Cull', 'Cull')], default='Clip', max_length=10)),
                ('confirmed', models.BooleanField(default=False)),
                ('mice', models.ManyToManyField(db_column='Mouse', to='mice_repository.mouse')),
            ],
            options={
                'db_table': 'request',
                'managed': True,
            },
        ),
    ]
