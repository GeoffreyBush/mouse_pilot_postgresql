import factory
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
