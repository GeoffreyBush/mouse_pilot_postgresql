from datetime import date
import factory

from breeding_cage.forms import BreedingCageForm
from mice_repository.forms import RepositoryMiceForm
from stock_cage.forms import BatchFromBreedingCageForm
from system_users.forms import CustomUserChangeForm, CustomUserCreationForm
from test_factories.model_factories import (
    MouseFactory,
    ProjectFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)
from website.forms import RequestForm


class BreedingCageFormFactory:

    @staticmethod
    def create(**kwargs):
        return BreedingCageForm(data=kwargs)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "box_no": "1",
            "mother": MouseFactory(sex="F"),
            "father": MouseFactory(sex="M"),
        }

    @staticmethod
    def invalid_mother(**kwargs):
        return {
            "box_no": "1",
            "father": MouseFactory(sex="M"),
        }

    @staticmethod
    def invalid_father(**kwargs):
        return {
            "box_no": "1",
            "mother": MouseFactory(sex="F"),
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
            "password2": kwargs.get("password2", "testpassword"),
        }


class CustomUserChangeFormFactory:
    @staticmethod
    def create(old_user, **kwargs):
        data = CustomUserChangeFormFactory.valid_data(**kwargs)
        return CustomUserChangeForm(instance=old_user, data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "username": kwargs.get("username", "new_user"),
            "email": kwargs.get("email", "newuser@example.com"),
        }


# Could refactor RequestFormFactory to use kwargs more
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
        data = RepositoryMiceFormFactory.valid_data(**kwargs)
        return RepositoryMiceForm(data=data)

    @staticmethod
    def valid_data(**kwargs):

        strain = kwargs.get("strain")
        if strain is not None and kwargs.get("_tube") is None:
            _tube = strain.mice_count
        elif strain is not None and kwargs.get("_tube") is not None:
            _tube = strain.mice_count+1 # Shouldn't strain auto increment?
        elif strain is None and kwargs.get("_tube") is not None:
            strain = StrainFactory()
            _tube = kwargs.get("_tube")
        else:
            strain = StrainFactory()
            _tube = strain.mice_count

        data = {
            "_tube": _tube,
            "sex": kwargs.get("sex", "M"),
            "dob": kwargs.get("dob", date.today()),
            "clipped_date": kwargs.get("clipped_date", date.today()),
            "project": kwargs.get("project", ProjectFactory()),
            "earmark": kwargs.get("earmark", ""),
            "genotyper": kwargs.get("genotyper", UserFactory().id),
            "strain": strain,
            "coat": kwargs.get("coat", "Black"),
            "result": kwargs.get("result", "Positive"),
            "fate": kwargs.get("fate", "Culled"),
        }
        return data


class BatchFromBreedingCageFormFactory:
    @staticmethod
    def create(**kwargs):
        data = BatchFromBreedingCageFormFactory.valid_data(**kwargs)
        return BatchFromBreedingCageForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        strain = kwargs.get("strain", StrainFactory())
        return {
            "tube": kwargs.get("_tube", 3),
            "sex": kwargs.get("sex", "M"),
            "coat": kwargs.get("coat", "Black"),
            "strain": strain,
            "mother": kwargs.get("mother", MouseFactory(sex="F", strain=strain)),
            "father": kwargs.get("father", MouseFactory(sex="M", strain=strain)),
            "dob": kwargs.get("dob", date.today()),
            "stock_cage": kwargs.get("stock_cage", StockCageFactory()),
        }
