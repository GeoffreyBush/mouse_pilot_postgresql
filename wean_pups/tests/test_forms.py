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
        # print("Test formset data:")
        # print()
        # for form in self.formset:
        #   for new_form in form:
        #      print(new_form)
        #     print()
        # print(form.data)
        # print()
        assert all(len(error) == 0 for error in self.formset.errors)

    def test_formset_is_valid(self):
        self.assertTrue(self.formset.is_valid())

    def test_no_formset_non_form_errors(self):
        self.assertEqual(len(self.formset.non_form_errors()), 0)


class PupsToStockCageInvalidFormSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = StrainFactory()
        cls.mother = MouseFactory(strain=cls.strain, sex="F")
        cls.father = MouseFactory(strain=cls.strain, sex="M")
        cls.cage = BreedingCageFactory(male_pups=1, female_pups=3)

    def setUp(self):
        self.formset = PupsToStockCageFormSetFactory.create(
            strain=self.strain,
            mother=self.mother.pk,
            father=self.father.pk,
            num_males=self.cage.male_pups,
            num_females=self.cage.female_pups,
        )

    # None of the tube numbers in the formset can be identical
    def test_duplicate_tube_numbers_in_formset_are_invalid(self):
        self.formset = PupsToStockCageFormSetFactory.alter_tube_numbers(
            self.formset, [20, 20, 21, 22]
        )
        self.assertFalse(self.formset.is_valid())

    # If no tube numbers given, correct default assignment when formset is loaded

    # All tube numbers must exist in the formset

    # Can't transfer from the same breeding cage twice

    # If any form in the formset is invalid, the entire formset is invalid
