from django.test import Client, TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import BatchFromBreedingCageFormFactory
from mouse_pilot_postgresql.model_factories import BreedingCageFactory, UserFactory
from wean_pups.forms import BatchFromBreedingCageForm
from website.models import Strain

from mouse_pilot_postgresql.model_factories import MouseFactory, StrainFactory
from mouse_pilot_postgresql.form_factories import WeanPupsFormsetFactory

from django.urls.exceptions import NoReverseMatch


class BatchFromBreedingCageFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = Strain.objects.create(strain_name="TestStrain")
        cls.form = BatchFromBreedingCageFormFactory.create(strain=cls.strain)

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
        self.form = BatchFromBreedingCageFormFactory.create(_tube=None)
        self.assertFalse(self.form.is_valid())

    def test_tube_number_not_integer(self):
        self.form = BatchFromBreedingCageFormFactory.create(_tube="str")
        self.assertFalse(self.form.is_valid())

    def test_duplicate_global_id(self):
        self.assertTrue(self.form.is_valid())
        self.form = BatchFromBreedingCageFormFactory.create(_tube=2)
        self.assertFalse(self.form.is_valid())

    def test_global_id_input_field_not_visible(self):
        self.assertFalse("_global_id" in BatchFromBreedingCageForm().fields)


class PupsToStockCageViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory()
        cls.cage = BreedingCageFactory()
        cls.client.force_login(cls.user)
        cls.response = cls.client.get(
            reverse("wean_pups:pups_to_stock_cage", args=[cls.cage.box_no])
        )
        cls.formset = cls.response.context["formset"]

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "pups_to_stock_cage.html")

    def test_formset_in_context(self):
        self.assertIsNotNone(self.formset)
    
    def test_all_forms_in_formset_are_correct_type(self):
        assert all(isinstance(form, BatchFromBreedingCageForm) for form in self.formset)

    def test_formset_contains_correct_number_of_forms(self):
        self.assertEqual(len(self.formset.forms), self.cage.male_pups + self.cage.female_pups)

    def test_invalid_box_no_in_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("wean_pups:pups_to_stock_cage", args=["invalid"]))
        self.assertEqual(response.status_code, 404)

    def test_not_passing_box_no_in_url(self):
        self.client.force_login(self.user)
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse("wean_pups:pups_to_stock_cage"))



class PupsToStockCageViewValidPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory()
        cls.strain = StrainFactory()
        cls.cage = BreedingCageFactory(mother=MouseFactory(strain=cls.strain, sex="F"), father=MouseFactory(strain=cls.strain, sex="M"))
        cls.formset = WeanPupsFormsetFactory.create(cls.cage, strain=cls.strain)


    # If tube numbers given, correct assignment
    def test_pups_to_stock_cage_valid_data(self):
        pass

class PupsToStockCageViewInvalidPostTest(TestCase):
    def x(self):
        pass

    # None of the tube numbers in the formset can be identical

    # If no tube numbers given, correct default assignment when formset is loaded

    # All tube numbers must exist in the formset

    # Can't transfer from the same breeding cage twice

    # If any form in the formset is invalid, the entire formset is invalid
