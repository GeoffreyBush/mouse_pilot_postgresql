import glob
import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Removes all migrations, deletes db.sqlite3, runs makemigrations and migrate"

    def handle(self, *args, **kwargs):
        self.stdout.write("Removing migrations and deleting db.sqlite3")

        for migrations_dir in glob.glob("*/migrations", recursive=True):
            files = glob.glob(os.path.join(migrations_dir, "*.py"))
            for file in files:
                if file != os.path.join(migrations_dir, "__init__.py"):
                    os.remove(file)

        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")

        self.stdout.write("Running makemigrations")
        call_command("makemigrations", interactive=True)

        self.stdout.write("Running migrate")
        call_command("migrate", interactive=True)
