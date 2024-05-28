from website.forms import BreedingCageForm, CustomUserCreationForm
from website.tests.model_factories import MouseFactory


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
