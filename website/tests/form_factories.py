from datetime import date

from website.forms import BreedingCageForm
from website.tests.model_factories import MouseFactory

class BreedingCageFormFactory:
    @staticmethod
    def create(**kwargs):
        return BreedingCageForm(data=kwargs)

    @staticmethod
    def create_valid_data(**kwargs):
        father, mother = MouseFactory(sex="M"), MouseFactory(sex="F")
        return {
            "box_no": "1",
            "mother": mother,
            "father": father,
        }

    @staticmethod
    def create_invalid_mother(**kwargs):
        father = MouseFactory(sex="M")
        return {
            "box_no": "1",
            "father": father,
        }

    @staticmethod
    def create_invalid_box_no(**kwargs):
        father, mother = MouseFactory(sex="M"), MouseFactory(sex="F")
        return {
            "box_no": "",
            "mother": mother,
            "father": father,
        }
