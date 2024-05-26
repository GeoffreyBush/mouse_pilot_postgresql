import factory
import random
from datetime import date
from django.contrib.auth import get_user_model
from faker import Faker

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

    strain = factory.SubFactory(StrainFactory, strain_name="teststrain")
    sex = random.choice(["M", "F"])
    dob = date.today()



