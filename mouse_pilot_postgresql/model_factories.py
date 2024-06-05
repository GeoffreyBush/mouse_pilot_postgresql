import random
from datetime import date

import factory
from django.contrib.auth import get_user_model
from faker import Faker

from mouse_pilot_postgresql.constants import RESEARCH_AREAS

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"testuser{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    email = factory.Sequence(lambda n: f"test{n}@example.com")
    is_superuser = False
    first_name = fake.first_name()
    last_name = fake.last_name()


class StrainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "website.Strain"

    strain_name = factory.Sequence(lambda n: f"strain{n}")


class MouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mice_repository.Mouse"

    strain = factory.SubFactory(StrainFactory)
    sex = random.choice(["M", "F"])
    dob = date.today()
    _tube = 1


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "projects.Project"

    project_name = factory.Sequence(lambda n: f"project{n}")
    research_area = random.choice(RESEARCH_AREAS)


# This factory is not accurate - need more inforation from breeding wing
class BreedingCageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "breeding_cage.BreedingCage"

    box_no = factory.Sequence(lambda n: f"box{n}")
    mother = factory.SubFactory(MouseFactory)
    father = factory.SubFactory(MouseFactory)
    date_born = date.today()
    number_born = random.randint(1, 10)
    cull_to = random.randint(1, 10)
    date_wean = date.today()
    number_wean = random.randint(1, 10)
    pwl = random.randint(1, 10)


class StockCageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = "stock_cage.StockCage"

class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mice_requests.Request"

    project = factory.SubFactory(ProjectFactory)
    task_type = random.choice(["Cl", "Cu", "Mo", "We"])
    mice = factory.SubFactory(MouseFactory)
    new_message = fake.text(200)
    date_requested = date.today()
    date_completed = date.today()
