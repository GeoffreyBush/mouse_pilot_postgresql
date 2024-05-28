import os
import glob
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Removes all migrations, deletes db.sqlite3, runs makemigrations and migrate'

    def handle(self, *args, **kwargs):
        self.stdout.write('Removing migrations and deleting db.sqlite3')
        # Remove all migration files
        migrations_dir = 'website/migrations'
        if os.path.exists(migrations_dir):
            files = glob.glob(os.path.join(migrations_dir, '*.py'))
            for file in files:
                if file != os.path.join(migrations_dir, '__init__.py'):
                    os.remove(file)
        # Delete db.sqlite3
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')

        self.stdout.write('Running makemigrations')
        call_command('makemigrations', interactive=True)

        self.stdout.write('Running migrate')
        call_command('migrate', interactive=True)
