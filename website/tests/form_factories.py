from website.forms import BreedingCageForm


class BreedingCageFormFactory:
    @staticmethod
    def create(**kwargs):
        return BreedingCageForm(data=kwargs)

    @staticmethod
    def create_valid(**kwargs):
        return BreedingCageForm(
            data={
                "name": "Cage 1",
                "description": "Description",
                "capacity": 10,
                #'breeding_cage_type': BreedingCageType.objects.first().pk,
                #'breeding_cage_status': BreedingCageStatus.objects.first().pk,
                #'breeding_cage_location': BreedingCageLocation.objects.first().pk,
            }
        )

    @staticmethod
    def create_invalid(**kwargs):
        return BreedingCageForm(
            data={
                "name": "",
                "description": "",
                "capacity": 0,
                #'breeding_cage_type': None,
                #'breeding_cage_status': None,
                #'breeding_cage_location': None,
            }
        )
