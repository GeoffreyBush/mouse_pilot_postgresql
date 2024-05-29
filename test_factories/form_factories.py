from datetime import date

from breeding_cage.forms import BreedingCageForm
from test_factories.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.forms import CustomUserCreationForm, RequestForm
from stock_cage.forms import CreateMouseFromBreedingCageForm

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
    def invalid_father(**kwargs):
        mother = MouseFactory(sex="F")
        return {
            "box_no": "1",
            "mother": mother,
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
        return {
            "mice": [mouse1.pk, mouse2.pk],
            "task_type": "Cl",
            "researcher": UserFactory().id,
            "new_message": "Test message",
        }

    @staticmethod
    def missing_mice(**kwargs):
        return {
            "mice": [],
            "task_type": "Cl",
            "researcher": UserFactory().id,
            "new_message": "Test message",
        }


class RepositoryMiceFormFactory:
    @staticmethod
    def create(**kwargs):
        # return RepositoryMiceForm(data=kwargs)
        pass

    @staticmethod
    def valid_data(**kwargs):
        _tube = kwargs.get("_tube", 1)
        strain = kwargs.get("strain", StrainFactory())
        return {
            "_tube": _tube,
            "sex": "M",
            "dob": date.today(),
            "clipped_date": date.today(),
            "project": ProjectFactory(),
            "earmark": "TR",
            "genotyper": UserFactory().id,
            "strain": strain,
            "coat": "Black",
            "result": "Positive",
            "fate": "Culled",
        }

    @staticmethod
    def invalid_dob(**kwargs):
        return {
            "sex": "M",
            "dob": None,
            "clipped_date": date.today(),
            "mother": None,
            "father": None,
            "project": ProjectFactory(),
            "earmark": "TR",
            "genotyper": UserFactory().id,
            "strain": StrainFactory(),
            "coat": "Black",
            "result": "Positive",
            "fate": "Culled",
        }

    @staticmethod
    def duplicate_mice(**kwargs):
        return {
            "sex": "M",
            "dob": date.today(),
            "clipped_date": date.today(),
            "mother": None,
            "father": None,
            "project": ProjectFactory(),
            "earmark": "TR",
            "genotyper": None,
            "strain": StrainFactory(),
            "coat": "Black",
            "result": "Positive",
            "fate": "Culled",
        }
    
