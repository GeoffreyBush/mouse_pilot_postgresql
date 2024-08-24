import itertools
import random
from datetime import date

from django.forms import formset_factory

from breeding_cage.forms import BreedingCageForm
from main.forms import MouseSelectionForm
from main.model_factories import (
    MouseFactory,
    ProjectFactory,
    StockCageFactory,
    StrainFactory,
)
from mice_repository.forms import RepositoryMiceForm
from mice_requests.forms import RequestForm
from projects.forms import ProjectForm
from system_users.forms import CustomUserChangeForm, CustomUserCreationForm
from wean_pups.forms import PupsToStockCageForm, PupsToStockCageFormSet

# These factories are used in automated testing to create forms with consistent, predictable data 

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
            "strain": StrainFactory(),
        }

    @staticmethod
    def invalid_mother(**kwargs):
        return {
            "box_no": "1",
            "father": MouseFactory(sex="M"),
            "strain": StrainFactory(),
        }

    @staticmethod
    def invalid_father(**kwargs):
        return {
            "box_no": "1",
            "mother": MouseFactory(sex="F"),
            "strain": StrainFactory(),
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


class MiceRequestFormFactory:

    @staticmethod
    def create(**kwargs):
        data = MiceRequestFormFactory.valid_data(**kwargs)
        return RequestForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        return {
            "mice": kwargs.get("mice", [MouseFactory().pk, MouseFactory().pk]),
            "task_type": kwargs.get("task_type", random.choice(["Clip", "Cull"])),
            "requested_by": kwargs.get("requested_by", ""),
        }


class RepositoryMiceFormFactory:
    @staticmethod
    def build(**kwargs):
        data = RepositoryMiceFormFactory.valid_data(**kwargs)
        return RepositoryMiceForm(data=data)

    @staticmethod
    def valid_data(**kwargs):

        strain = kwargs.get("strain")
        if strain is not None:
            tube = strain.mice.count() + 1
        else:
            strain = StrainFactory()
            tube = kwargs.get("tube", strain.mice.count() + 1)

        data = {
            "tube": tube,
            "sex": kwargs.get("sex", "M"),
            "dob": kwargs.get("dob", date.today()),
            "strain": strain,
            "clipped_date": kwargs.get("clipped_date", ""),
            "project": kwargs.get("project", ""),
            "earmark": kwargs.get("earmark", ""),
            "genotyper": kwargs.get("genotyper", ""),
            "culled_date": kwargs.get("culled_date", ""),
            "coat": kwargs.get("coat", ""),
            "result": kwargs.get("result", ""),
            "fate": kwargs.get("fate", ""),
        }
        return data


class PupsToStockCageFormFactory:
    @staticmethod
    def build(**kwargs):
        data = PupsToStockCageFormFactory.valid_data(**kwargs)
        return PupsToStockCageForm(data=data)

    @staticmethod
    def valid_data(**kwargs):
        strain = kwargs.get("strain", StrainFactory())
        tube_counter = itertools.count(100)
        return {
            "tube": kwargs.get("tube", next(tube_counter)),
            "sex": kwargs.get("sex", "M"),
            "coat": kwargs.get("coat", "Black"),
            "strain": strain,
            "mother": kwargs.get("mother", MouseFactory(sex="F", strain=strain)),
            "father": kwargs.get("father", MouseFactory(sex="M", strain=strain)),
            "dob": kwargs.get("dob", date.today()),
            "cage": kwargs.get("cage", StockCageFactory()),
        }


class PupsToStockCageFormSetFactory:
    @staticmethod
    def build(num_males=0, num_females=0, prefix="mouse", **kwargs):
        num_forms = num_males + num_females
        MouseFormSet = formset_factory(
            PupsToStockCageForm, formset=PupsToStockCageFormSet, extra=0
        )

        # formset management data
        data = {
            f"{prefix}-TOTAL_FORMS": str(num_forms),
            f"{prefix}-INITIAL_FORMS": "0",
            f"{prefix}-MAX_NUM_FORMS": "",
            "form-TOTAL_FORMS": str(num_forms),
            "form-INITIAL_FORMS": "0",
        }

        # mice form data
        strain = kwargs.get("strain", StrainFactory())
        mother = kwargs.get("mother", MouseFactory(sex="F", strain=strain))
        father = kwargs.get("father", MouseFactory(sex="M", strain=strain))
        dob = kwargs.get("dob", date.today())
        stock_cage = kwargs.get("stock_cage", StockCageFactory().pk)

        default_tube_counter = itertools.count(100)
        passed_tubes = kwargs.get("passed_tubes", [])

        # Create a form for each mouse
        for i in range(num_forms):
            sex = "M" if i < num_males else "F"
            if len(passed_tubes) > 0:
                next_tube = passed_tubes.pop(0)
            else:
                next_tube = next(default_tube_counter)
            form_data = PupsToStockCageFormFactory.valid_data(
                strain=strain,
                mother=mother,
                father=father,
                dob=dob,
                cage=stock_cage,
                tube=next_tube,
                sex=sex,
            )
            for field, value in form_data.items():
                data[f"{prefix}-{i}-{field}"] = str(value)
        return MouseFormSet(data)

    @staticmethod
    def alter_tube_numbers(formset, new_tube_numbers):
        data = formset.data.copy()
        for i, tube in enumerate(new_tube_numbers):
            data[f"mouse-{i}-tube"] = tube
        formset.data = data
        return formset


class ProjectFormFactory:
    @staticmethod
    def create(**kwargs):
        data = ProjectFormFactory.valid_data(**kwargs)
        return ProjectForm(data=data)

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


# This factory causes phantom mice to be created in tests
class MouseSelectionFormFactory:
    @staticmethod
    def build(**kwargs):
        data = MouseSelectionFormFactory.data(**kwargs)
        return MouseSelectionForm(
            data=data, project=kwargs.get("project", ProjectFactory())
        )

    @staticmethod
    def data(**kwargs):
        if kwargs.get("mice") is None:
            mouse1, mouse2 = MouseFactory(), MouseFactory()
            if kwargs.get("project") is not None:
                kwargs["project"].mice.add(mouse1, mouse2)
                return {"mice": [mouse1, mouse2]}
            else:
                project = ProjectFactory()
                project.mice.add(mouse1, mouse2)
                return {"mice": [mouse1, mouse2]}
        return {
            "mice": kwargs.get("mice"),
        }
