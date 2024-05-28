from website.forms import BreedingCageForm, CustomUserCreationForm, RequestForm
from website.tests.model_factories import MouseFactory, UserFactory


class BreedingCageFormFactory:

    @staticmethod
    def create(**kwargs):
        return BreedingCageForm(data=kwargs)

    @staticmethod
    def valid_data(**kwargs):
        father, mother = MouseFactory(sex="M"), MouseFactory(sex="F")
        return {
            "box_no": "1",
            "mother": mother,
            "father": father,
        }

    @staticmethod
    def invalid_mother(**kwargs):
        father = MouseFactory(sex="M")
        return {
            "box_no": "1",
            "father": father,
        }

    @staticmethod
    def invalid_box_no(**kwargs):
        father, mother = MouseFactory(sex="M"), MouseFactory(sex="F")
        return {
            "box_no": "",
            "mother": mother,
            "father": father,
        }


class CustomUserCreationFormFactory:
    @staticmethod
    def create(**kwargs):
        return CustomUserCreationForm(data=kwargs)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

    @staticmethod
    def mismatched_passwords(**kwargs):
        return {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "wrongpass",
        }


class RequestFormFactory:

    @staticmethod
    def create(**kwargs):
        return RequestForm(data=kwargs)

    @staticmethod
    def valid_data(mouse1, mouse2, **kwargs):
        user = UserFactory()
        return {
            "mice": [mouse1.pk, mouse2.pk],
            "task_type": "Cl",
            "researcher": user.id,
            "new_message": "Test message",
        }

    @staticmethod
    def missing_mice(**kwargs):
        user = UserFactory()
        return {
            "mice": [],
            "task_type": "Cl",
            "researcher": user.id,
            "new_message": "Test message",
        }
