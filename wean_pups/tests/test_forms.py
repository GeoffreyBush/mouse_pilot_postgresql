from django.test import TestCase

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import (
    PupsToStockCageFormFactory,
    PupsToStockCageFormSetFactory,
)
from mouse_pilot_postgresql.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StrainFactory,
)
from wean_pups.forms import PupsToStockCageForm
from website.models import Strain


class PupsToStockCageFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = Strain.objects.create(strain_name="TestStrain")
        cls.form = PupsToStockCageFormFactory.create(strain=cls.strain)

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_correct_strain(self):
        self.assertEqual(self.form.data["strain"].strain_name, "TestStrain")

    def test_correct_pk(self):
        self.mouse = self.form.save()
        self.assertEqual(self.mouse.pk, "TestStrain-100")

    def test_mouse_created(self):
        self.assertEqual(Mouse.objects.count(), 2)
        self.form.save()
        self.assertEqual(Mouse.objects.count(), 3)

    def test_missing_tube_number(self):
        self.form = PupsToStockCageFormFactory.create(_tube=None)
        self.assertFalse(self.form.is_valid())

    def test_tube_number_not_integer(self):
        self.form = PupsToStockCageFormFactory.create(_tube="str")
        self.assertFalse(self.form.is_valid())

    def test_duplicate_global_id(self):
        self.assertTrue(self.form.is_valid())
        self.form = PupsToStockCageFormFactory.create(_tube=2)
        self.assertFalse(self.form.is_valid())

    def test_global_id_input_field_not_visible(self):
        self.assertFalse("_global_id" in PupsToStockCageForm().fields)


class PupsToStockCageValidFormSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = StrainFactory()
        cls.mother = MouseFactory(strain=cls.strain, sex="F")
        cls.father = MouseFactory(strain=cls.strain, sex="M")
        cls.cage = BreedingCageFactory(male_pups=3, female_pups=5)
        cls.formset = PupsToStockCageFormSetFactory.create(
            strain=cls.strain,
            mother=cls.mother.pk,
            father=cls.father.pk,
            num_males=cls.cage.male_pups,
            num_females=cls.cage.female_pups,
        )

    def test_each_form_in_formset_is_valid(self):
        assert all(len(error) == 0 for error in self.formset.errors)

    def test_formset_is_valid(self):
        self.assertTrue(self.formset.is_valid())

    def test_no_formset_non_form_errors(self):
        self.assertEqual(len(self.formset.non_form_errors()), 0)

class PupsToStockCageInvalidFormSetTest:
    pass
