import random

import faker.providers
from colorama import Fore, Style
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from website.constants import (
    EARMARK_CHOICES,
    PROJECT_NAMES,
    RESEARCH_AREAS,
    STRAINS,
)
from website.models import Cage, Comment, CustomUser, Mice, Project, Strain

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

    help = "Command information"

    ###############################################
    ### Add all strains from STRAINS list to DB ###
    ###############################################
    def create_strains(self):
        print("Creating strains...", end=" ")
        for i in range(len(STRAINS)):
            Strain.objects.get_or_create(strain_name=STRAINS[i])
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ######################################
    ### Create x number of cages in DB ###
    ######################################
    def create_cages(self, x):

        fake = Faker()
        fake.add_provider(Provider)
        Mice.objects.all()

        print("Creating cages...", end=" ")
        for _ in range(x):
            variable_number_born = random.randint(1, 21)
            variable_number_wean = random.randint(1, variable_number_born)
            Cage.objects.create(
                box_no=fake.unique.website_box_no(),
                status=random.choice(["Empty", "ParentsInside", "ParentsRemoved"]),
                mother="Female ID",
                father="Male ID",
                date_born=fake.date(),
                number_born=variable_number_born,
                cull_to="placeholder",
                date_wean=fake.date(),
                number_wean=variable_number_wean,
                pwl=variable_number_born - variable_number_wean,
            )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ######################################
    ### Create x number of users in DB ###
    ######################################
    def create_users(self, x):

        fake = Faker()

        print("Creating users...", end=" ")
        for _ in range(x):
            CustomUser.objects.create(
                password=make_password(fake.password()),
                is_superuser=False,
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.ascii_email(),
                is_staff=True,
                is_active=True,
            )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #########################################
    ### Create x number of projects in DB ###
    #########################################
    def create_projects(self, x):

        fake = Faker()
        fake.add_provider(Provider)

        print("Creating projects...", end=" ")
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
                projectname=fake.unique.website_project_name(),
                researcharea=fake.unique.website_research_area(),
            )

            # Add strains and researchers from random indexes
            for i in random_index_strains:
                project.strains.add(existing_strains[i])
            for j in random_index_researchers:
                project.researchers.add(existing_researchers[j])
            project.save()

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #####################################
    ### Create x number of mice in DB ###
    #####################################

    def create_mice(self, x):
        fake = Faker()

        # Collect foreign keys
        existing_cages = Cage.objects.all()
        existing_projects = Project.objects.all()
        existing_researchers = CustomUser.objects.all()
        existing_strains = Strain.objects.all()

        print("Creating mice...", end=" ")

        # Create all the mice first
        for _ in range(x):
            Mice.objects.create(
                sex=random.choice(["M", "F"]),
                dob=fake.date(),
                clippedDate=fake.date(),
                genotyped=fake.boolean(chance_of_getting_true=60),
                cage=random.choice(existing_cages),
                project=random.choice(existing_projects),
                genotyper=random.choice(existing_researchers),
                strain=random.choice(existing_strains),
                earmark=random.choice(EARMARK_CHOICES),
                mother=None,
                father=None,
            )

        """
        # This doesn't create mothers and fathers as intended, review Autumn 2024
        # Assign mothers and fathers for the mice
        all_mice = Mice.objects.all()
        for mouse in all_mice:
            project_mice = Mice.objects.filter(project=mouse.project)

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

    #########################################
    ### Create x number of comments in DB ###
    #########################################
    def create_comments(self, x):

        fake = Faker()

        print("Creating comments...", end=" ")
        existing_mice = Mice.objects.all()

        for index in range(len(existing_mice)):
            mouse = existing_mice[index]
            Comment.objects.create(
                comment=mouse,
                comment_text=fake.text(max_nb_chars=500),
            )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ######################################
    ### Create x number of users in DB ###
    ######################################
    def create_requests(self):
        print("Creating requests", end=" ")
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    #######################################################################
    ### Create "SuperUser" account with password "samplepassword" in DB ###
    #######################################################################
    def create_super_user(self):

        fake = Faker()

        print("Creating 'SuperUser' account...", end=" ")
        CustomUser.objects.create(
            password=make_password("samplepassword"),
            is_superuser=True,
            username="SuperUser",
            email=fake.ascii_email(),
            is_staff=True,
            is_active=True,
        )
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    ###################
    ### Main method ###
    ###################
    def handle(self, *args, **kwargs):

        fake = Faker()
        fake.add_provider(Provider)

        print("Beginning fake data creation...")

        # Add fake data to database
        self.create_strains()
        self.create_cages(30)
        self.create_users(20)
        self.create_super_user()
        self.create_projects(10)
        self.create_mice(500)
        self.create_comments(50)

        self.stdout.write(
            self.style.SUCCESS("Fake data successfully created in database")
        )
