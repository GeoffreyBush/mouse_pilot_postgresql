from datetime import date


from breeding_cage.forms import BreedingCageForm
from mice_repository.forms import RepositoryMiceForm
from mice_requests.forms import RequestForm
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)
from projects.forms import NewProjectForm
from stock_cage.forms import BatchFromBreedingCageForm
from system_users.forms import CustomUserChangeForm, CustomUserCreationForm


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


class NewProjectFormFactory:
    @staticmethod
    def create(**kwargs):
        data = NewProjectFormFactory.valid_data(**kwargs)
        return NewProjectForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "project_name": kwargs.get("project_name", "testproject"),
            "research_area": kwargs.get("research_area", "TestArea"),
            "strains": kwargs.get("strains", [StrainFactory()]),
            "researchers": kwargs.get("researchers", [UserFactory()]),
        }
