import random

import faker.providers
from colorama import Fore, Style
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from breeding_cage.models import BreedingCage
from mice_repository.models import Mouse
from projects.models import Project
from stock_cage.models import StockCage
from system_users.models import CustomUser
from mouse_pilot_postgresql.constants import (
    EARMARK_CHOICES,
    PROJECT_NAMES,
    RESEARCH_AREAS,
    STRAINS,
)
from website.models import Comment, Strain

# Adapted from https://www.youtube.com/watch?v=8LHdbaV7Dvo


class Provider(faker.providers.BaseProvider):

    def website_project_name(self):
        return self.random_element(PROJECT_NAMES)

    def website_research_area(self):
        return self.random_element(RESEARCH_AREAS)

    def website_box_no(self):
        return self.random_element(
            [f"{i}-{random.randint(1, 4)}" for i in range(1, 20)]
        )


class Command(BaseCommand):

    help = "Populates an empty database with fake data."
    fake = Faker()
    fake.add_provider(Provider)

    ###############################################
    ### Add all strains from STRAINS list to DB ###
    ###############################################
    def create_strains(self):
        print("  Creating strains...", end=" ")
        for i in range(len(STRAINS)):
            Strain.objects.get_or_create(strain_name=STRAINS[i])
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ######################################
    ### Create x number of users in DB ###
    ######################################
    def create_users(self, x):

        print("  Creating users...", end=" ")
        for _ in range(x):
            CustomUser.objects.create(
                password=make_password(self.fake.password()),
                is_superuser=False,
                username=self.fake.unique.user_name(),
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                email=self.fake.ascii_email(),
                is_staff=True,
                is_active=True,
            )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #########################################
    ### Create x number of projects in DB ###
    #########################################
    def create_projects(self, x):

        print("  Creating projects...", end=" ")
        existing_strains = Strain.objects.all()
        # CustomUser should differentiate between researchers and breeding wing staff, but doesn't currently.
        existing_researchers = CustomUser.objects.all()

        for _ in range(x):

            # Get random indexes of researchers and strains
            random_index_strains = random.sample(
                range(len(existing_strains)), random.randint(1, 5)
            )
            random_index_researchers = random.sample(
                range(len(existing_researchers)), random.randint(1, 5)
            )

            # Make a project
            project = Project.objects.create(
                project_name=self.fake.unique.website_project_name(),
                research_area=self.fake.unique.website_research_area(),
            )

            # Add strains and researchers from random indexes
            for i in random_index_strains:
                project.strains.add(existing_strains[i])
            for j in random_index_researchers:
                project.researchers.add(existing_researchers[j])
            project.save()

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ############################################
    ### Create x number of stock cages in DB ###
    ############################################
    def create_stock_cages(self, x):
        print("  Creating stock cages...", end=" ")
        for _ in range(x):
            StockCage.objects.create()

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #####################################
    ### Create x number of mice in DB ###
    #####################################

    def create_mice(self, x):

        # Collect foreign keys
        existing_projects = Project.objects.all()
        existing_researchers = CustomUser.objects.all()
        existing_strains = Strain.objects.all()

        print("  Creating mice...", end=" ")

        # Create all the mice first
        for _ in range(x):
            Mouse.objects.create(
                strain=random.choice(existing_strains),
                sex=random.choice(["M", "F"]),
                dob=self.fake.date(),
                clipped_date=self.fake.date(),
                project=random.choice(existing_projects),
                genotyper=random.choice(existing_researchers),
                earmark=random.choice(EARMARK_CHOICES),
                mother=None,
                father=None,
            )

        """
        # This doesn't create mothers and fathers as intended, review Autumn 2024
        # Assign mothers and fathers for the mice
        all_mice = Mouse.objects.all()
        for mouse in all_mice:
            project_mice = Mouse.objects.filter(project=mouse.project)

            # Filter the project mice to get the eligible mothers and fathers
            eligible_mothers = project_mice.filter(sex='F').exclude(id=mouse.id)
            eligible_fathers = project_mice.filter(sex='M').exclude(id=mouse.id)

            # Assign a random eligible mother and father, if available
            if eligible_mothers.exists() and eligible_fathers.exists():
                mouse.mother = random.choice(eligible_mothers)
                mouse.father = random.choice(eligible_fathers)
                mouse.save()
        """

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ######################################
    ### Create x number of cages in DB ###
    ######################################
    def create_breeding_cages(self, x):

        existing_mice = Mouse.objects.all()
        female_mice = existing_mice.filter(sex="F")
        male_mice = existing_mice.filter(sex="M")

        print("  Creating breeding cages...", end=" ")
        for _ in range(x):
            variable_number_born = random.randint(1, 21)
            variable_number_wean = random.randint(1, variable_number_born)
            mother = random.choice(female_mice)
            father = male_mice.filter(strain=mother.strain).order_by("?").first()
            BreedingCage.objects.create(
                box_no=self.fake.unique.website_box_no(),
                mother=mother,
                father=father,
                date_born=self.fake.date(),
                number_born=variable_number_born,
                cull_to="placeholder",
                date_wean=self.fake.date(),
                number_wean=variable_number_wean,
                pwl=variable_number_born - variable_number_wean,
                male_pups=random.randint(1, 6),
                female_pups=random.randint(1, 6),
            )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #########################################
    ### Create x number of comments in DB ###
    #########################################
    def create_comments(self, x):

        print("  Creating comments...", end=" ")
        existing_mice = Mouse.objects.all()

        for index in range(len(existing_mice)):
            mouse = existing_mice[index]
            Comment.objects.create(
                comment=mouse,
                comment_text=self.fake.text(max_nb_chars=500),
            )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #########################################
    ### Create x number of requests in DB ###
    #########################################
    def create_requests(self):
        print("  Creating requests", end=" ")
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #######################################################################
    ### Create "SuperUser" account with password "samplepassword" in DB ###
    #######################################################################
    def create_super_user(self):

        print("  Creating 'SuperUser' account...", end=" ")
        CustomUser.objects.create(
            password=make_password("samplepassword"),
            is_superuser=True,
            username="SuperUser",
            email=self.fake.ascii_email(),
            is_staff=True,
            is_active=True,
        )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ###################
    ### Main method ###
    ###################
    def handle(self, *args, **kwargs):

        print("Beginning fake data creation...")

        # Add fake data to database
        self.create_strains()
        self.create_users(20)
        self.create_super_user()
        self.create_projects(10)
        self.create_stock_cages(20)
        self.create_mice(500)
        self.create_breeding_cages(30)
        self.create_comments(50)

        self.stdout.write(
            self.style.SUCCESS("Fake data successfully created in database")
        )
