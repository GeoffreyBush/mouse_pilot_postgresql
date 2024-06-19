import random
from datetime import date

import factory
from faker import Faker

from mouse_pilot_postgresql.constants import RESEARCH_AREAS

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "system_users.CustomUser"

    username = factory.Sequence(lambda n: f"testuser{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    email = factory.Sequence(lambda n: f"test{n}@example.com")
    is_superuser = False


class StrainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "strain.Strain"

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


# This factory is not accurate - need more inforation from breeding wing
class BreedingCageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "breeding_cage.BreedingCage"

    box_no = factory.Sequence(lambda n: f"box{n}")
    mother = factory.SubFactory(MouseFactory)
    father = factory.SubFactory(MouseFactory)
    date_born = date.today()


class StockCageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = "stock_cage.StockCage"


class MiceRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mice_requests.Request"

    requested_by = factory.SubFactory(UserFactory)
    task_type = random.choice(["Clip", "Cull"])
    confirmed = False

    @factory.post_generation
    def mice(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for mouse in extracted:
                self.mice.add(mouse)
        else:
            self.mice.add(MouseFactory())
