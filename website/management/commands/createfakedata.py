import random

from colorama import Fore, Style
from django.core.management.base import BaseCommand
from faker import Faker

from mice_repository.models import Mouse
from mouse_pilot_postgresql.constants import EARMARK_CHOICES
from mouse_pilot_postgresql.model_factories import (
    BreedingCageFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from projects.models import Project
from stock_cage.models import StockCage
from strain.models import Strain
from system_users.models import CustomUser
from website.models import Comment


class Command(BaseCommand):

    help = "Populates an empty database with fake data."
    fake = Faker()

    def create_strains(self, n):
        for _ in range(n):
            StrainFactory.create()

    def create_users(self, n):
        for _ in range(n):
            UserFactory.create()

    def create_super_user(self):
        UserFactory.create(
            username="SuperUser", is_superuser=True, password="samplepassword"
        )

    def create_projects(self, n):
        existing_strains = Strain.objects.all()
        existing_researchers = CustomUser.objects.all()
        for _ in range(n):
            project = ProjectFactory.create()
            project.strains.add(random.choice(existing_strains))
            project.researchers.add(random.choice(existing_researchers))
            project.save()

    def create_stock_cages(self, n):
        for _ in range(n):
            StockCage.objects.create()

    # Convert this method to use a factory instead
    def create_mice(self, n):
        existing_projects = Project.objects.all()
        existing_strains = Strain.objects.all()
        for _ in range(n):
            Mouse.objects.create(
                strain=random.choice(existing_strains),
                sex=random.choice(["M", "F"]),
                dob=self.fake.date(),
                clipped_date=self.fake.date(),
                project=random.choice(existing_projects),
                earmark=random.choice(EARMARK_CHOICES),
                mother=None,
                father=None,
            )

    def create_breeding_cages(self, n):
        female_mice = Mouse.objects.filter(sex="F")
        male_mice = Mouse.objects.filter(sex="M")
        for _ in range(n):
            BreedingCageFactory.create(
                mother=random.choice(female_mice), father=random.choice(male_mice)
            )

    # Convert this method to use a factory instead
    def create_comments(self, x):
        existing_mice = Mouse.objects.all()
        for index in range(len(existing_mice)):
            mouse = existing_mice[index]
            Comment.objects.create(
                comment=mouse,
                comment_text=self.fake.text(max_nb_chars=500),
            )

    def handle(self, *args, **kwargs):
        print("Beginning fake data creation...")

        print("  Creating strains...", end=" ")
        self.create_strains(5)
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        print("  Creating users...", end=" ")
        self.create_users(5)
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        print("  Creating 'SuperUser' account...", end=" ")
        self.create_super_user()
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        print("  Creating projects...", end=" ")
        self.create_projects(5)
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        print("  Creating stock cages...", end=" ")
        self.create_stock_cages(5)
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        print("  Creating mice...", end=" ")
        self.create_mice(100)
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        print("  Creating breeding cages...", end=" ")
        self.create_breeding_cages(5)
        print(Fore.GREEN + Style.BRIGHT + "OK" + Style.RESET_ALL)

        # print("  Creating comments...", end=" ")
        # self.create_comments(50)
        # print(Fore.GREEN + "OK" + Style.RESET_ALL)

        self.stdout.write(
            self.style.SUCCESS("Fake data successfully created in database")
        )
