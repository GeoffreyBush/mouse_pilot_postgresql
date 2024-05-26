import random
from datetime import date

import factory
from django.contrib.auth import get_user_model
from faker import Faker

from website.constants import RESEARCH_AREAS

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"testuser{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    email = factory.Sequence(lambda n: f"testuser{n}")
    is_superuser = False
    first_name = fake.first_name()
    last_name = fake.last_name()


class StrainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "website.Strain"

    strain_name = factory.Sequence(lambda n: f"strain{n}")


class MouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "website.Mouse"

    strain = factory.SubFactory(StrainFactory)
    sex = random.choice(["M", "F"])
    dob = date.today()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "website.Project"

    project_name = factory.Sequence(lambda n: f"project{n}")
    research_area = random.choice(RESEARCH_AREAS)

# This factory is not accurate - need more inforation from breeding wing
class BreedingCageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "website.BreedingCage"
    
    box_no = factory.Sequence(lambda n: f"box{n}")
    mother = factory.SubFactory(MouseFactory)
    father = factory.SubFactory(MouseFactory)
    date_born = date.today()
    number_born = random.randint(1, 10)
    cull_to = random.randint(1, 10)
    date_wean = date.today()
    number_wean = random.randint(1, 10)
    pwl = random.randint(1, 10)
