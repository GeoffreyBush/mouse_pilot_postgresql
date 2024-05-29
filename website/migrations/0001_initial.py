# Generated by Django 5.0.6 on 2024-05-29 11:33

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
            name='StockCage',
            fields=[
                ('cage_id', models.AutoField(db_column='Cage ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'stockcage',
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
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
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
