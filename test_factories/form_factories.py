from datetime import date

from breeding_cage.forms import BreedingCageForm
from system_users.forms import CustomUserCreationForm, CustomUserChangeForm
from test_factories.model_factories import (
    MouseFactory,
    ProjectFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)
from website.forms import RequestForm

# Can rewrite these factories to make better use of kwargs, requiring less repeating code
# The rewrite can remove the need to return data, can return the form object instead
# Less factory methods, more flexibility

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
        data = CustomUserCreationFormFactory.valid_data(**kwargs)
        return CustomUserCreationForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "username": kwargs.get("username", "testuser"),
            "email": kwargs.get("email", "test@example.com"),
            "password1": kwargs.get("password1", "testpassword"),
            "password2": kwargs.get("password2", "testpassword")
        }
    
class CustomUserChangeFormFactory:
    @staticmethod
    def create(**kwargs):
        data = CustomUserChangeFormFactory.valid_data(**kwargs)
        return CustomUserChangeForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "instance": kwargs.get("old_user", "olduser"),
            "new_user": kwargs.get("new_user", "newuser"),
            "email": kwargs.get("newuser@example.com")
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
        strain = kwargs.get("strain", StrainFactory())
        if strain is not None and kwargs.get("_tube") is None:
            _tube = strain.mice_count
        else:
            _tube = kwargs.get("_tube", 1)
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


class BatchFromBreedingCageFormFactory:
    @staticmethod
    def create(**kwargs):
        pass

    @staticmethod
    def valid_data(**kwargs):
        strain = kwargs.get("strain", StrainFactory())
        return {
            "tube": 123,
            "sex": "M",
            "coat": "Black",
            "strain": strain,
            "mother": MouseFactory(sex="F", strain=strain),
            "father": MouseFactory(sex="M", strain=strain),
            "dob": date.today(),
            "stock_cage": StockCageFactory(),
        }
