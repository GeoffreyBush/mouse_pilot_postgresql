from breeding_cage.forms import BreedingCageForm
from test_factories.model_factories import MouseFactory, UserFactory
from website.forms import CustomUserCreationForm, RequestForm


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
    
class RepositoryFormFactory:
    @staticmethod
    def create(**kwargs):
        #return RepositoryMiceForm(data=kwargs)
        pass

    @staticmethod
    def valid_data(**kwargs):
        return {
            #"strain": StrainFactory(),
            "tube": 1,
        }