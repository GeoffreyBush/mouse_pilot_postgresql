import random
from datetime import date

from breeding_cage.forms import BreedingCageForm
from mice_repository.forms import RepositoryMiceForm
from mice_requests.forms import RequestForm
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)
from projects.forms import NewProjectForm
from system_users.forms import CustomUserChangeForm, CustomUserCreationForm
from wean_pups.forms import BatchFromBreedingCageForm
from website.forms import MouseSelectionForm


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
        data = RequestFormFactory.valid_data(**kwargs)
        return RequestForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "mice": kwargs.get("mice", [MouseFactory().pk, MouseFactory().pk]),
            "task_type": kwargs.get(
                "task_type", random.choice(["Clip", "Cull", "Move", "Wean"])
            ),
            "new_message": kwargs.get("new_message", "Test message"),
            "requested_by": kwargs.get("requested_by", UserFactory()),
        }


class RepositoryMiceFormFactory:
    @staticmethod
    def create(**kwargs):
        data = RepositoryMiceFormFactory.valid_data(**kwargs)
        return RepositoryMiceForm(data=data)

    @staticmethod
    def valid_data(**kwargs):

        # Need to strain.mice_count + 1 here to mock increment_mice_count()
        strain = kwargs.get("strain")
        if strain is not None:
            _tube = strain.mice_count + 1
        else:
            strain = StrainFactory()
            _tube = kwargs.get("_tube", strain.mice_count + 1)

        data = {
            "_tube": _tube,
            "sex": kwargs.get("sex", "M"),
            "dob": kwargs.get("dob", date.today()),
            "clipped_date": kwargs.get("clipped_date", date.today()),
            "project": kwargs.get("project", ""),
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


class NewProjectFormFactory:
    @staticmethod
    def create(**kwargs):
        data = NewProjectFormFactory.valid_data(**kwargs)
        return NewProjectForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "project_id": kwargs.get("project_id", 1),
            "project_name": kwargs.get("project_name", "testproject"),
            "research_area": kwargs.get("research_area", "TestArea"),
            "strains": kwargs.get("strains", [StrainFactory()]),
            # Not sure why this researchers line below breaks AddNewProjectViewTestCase but strains above doesnt
            # "researchers": kwargs.get("researchers", CustomUser.objects.filter(username="testuser")),
        }


class MouseSelectionFormFactory:
    @staticmethod
    def create(**kwargs):
        data = MouseSelectionFormFactory.valid_data(**kwargs)
        return MouseSelectionForm(data=data, project=kwargs.get("project", None))

    @staticmethod
    def valid_data(**kwargs):
        return {
            "mice": kwargs.get("mice"),
        }
