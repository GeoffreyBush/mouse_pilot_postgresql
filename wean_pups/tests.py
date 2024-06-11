from django.test import Client, TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import BatchFromBreedingCageFormFactory
from mouse_pilot_postgresql.model_factories import BreedingCageFactory, UserFactory
from wean_pups.forms import BatchFromBreedingCageForm
from website.models import Strain


class BatchFromBreedingCageFormTestCase(TestCase):
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
        self.assertEqual(self.mouse.pk, "TestStrain-3")

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


class PupsToStockCageViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory(username="testuser")
        cls.cage = BreedingCageFactory()
        cls.valid_form = BatchFromBreedingCageFormFactory.valid_data(cage=cls.cage)

    def test_get_request_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("wean_pups:pups_to_stock_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pups_to_stock_cage.html")
        formset = response.context["formset"]
        self.assertIsInstance(formset.forms[0], BatchFromBreedingCageForm)

    # POST TransferToStockCageForm with valid data
    # If tube numbers given, correct assignment
    def test_pups_to_stock_cage_valid_data(self):
        pass

    # None of the tube numbers in the formset can be identical

    # If no tube numbers given, correct default assignment when formset is loaded

    # All tube numbers must exist in the formset

    # Can't transfer from the same breeding cage twice

    # If any form in the formset is invalid, the entire formset is invalid
