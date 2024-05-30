from django.test import TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from stock_cage.forms import BatchFromBreedingCageForm
from stock_cage.models import StockCage
from test_factories.form_factories import BatchFromBreedingCageFormFactory
from test_factories.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StockCageFactory,
    UserFactory,
)
from website.models import Strain


class StockCageModelTestCase(TestCase):
    def setUp(self):
        self.cage = StockCageFactory()
        self.mouse1, self.mouse2 = MouseFactory(stock_cage=self.cage), MouseFactory(stock_cage=self.cage)

    # Check StockCageFactory works
    def test_stock_cage_factory(self):
        self.assertEqual(StockCage.objects.count(), 1)
        self.assertEqual(self.cage.cage_id, 1)

    # one-to-many relationship between StockCage and Mouse works with mouse.related_name attribute
    def test_stock_mice(self):
        self.assertEqual(self.cage.mice.count(), 2)

class BatchFromBreedingCageFormTestCase(TestCase):
    def setUp(self):
        self.strain = Strain.objects.create(strain_name="TestStrain")
        self.data = BatchFromBreedingCageFormFactory.valid_data(strain=self.strain)
        self.form = BatchFromBreedingCageForm(data=self.data)

    # Valid data
    def test_valid_data(self):
        self.assertEqual(self.form.data["strain"].strain_name, "TestStrain")
        self.assertTrue(self.form.is_valid())

    # Mouse is created with valid data
    def test_mouse_created(self):
        self.assertEqual(Mouse.objects.count(), 2)
        self.form.save()
        self.assertEqual(Mouse.objects.count(), 3)

    # Missing tube number
    def test_missing_tube_number(self):
        self.data.pop("_tube")
        form = BatchFromBreedingCageForm(data=self.data)
        self.assertFalse(form.is_valid())

    # _tube must be an integer
    def test_tube_number_not_integer(self):
        self.data["_tube"] = "str"
        self.form = BatchFromBreedingCageForm(data=self.data)
        self.assertFalse(self.form.is_valid())

    # Submitting a duplicate mouse._global_id is not valid
    def test_duplicate_global_id(self):
        self.mouse = MouseFactory(strain=self.strain)
        self.assertTrue(self.form.is_valid())
        self.data["_tube"] = self.mouse._tube
        self.form = BatchFromBreedingCageForm(data=self.data)
        self.assertFalse(self.form.is_valid())

    # _global_id is not a field in the form
    def test_altering_global_id(self):
        self.assertFalse("_global_id" in BatchFromBreedingCageForm().fields)


class TransferToStockCageViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.cage = BreedingCageFactory()
        self.valid_form = BatchFromBreedingCageFormFactory.valid_data(cage=self.cage)

    # Access Transfer to Stock Cage while logged in
    def test_transfer_to_stock_cage_authenticated_user(self):
        response = self.client.get(
            reverse("stock_cage:transfer_to_stock_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transfer_to_stock_cage.html")

    # POST TransferToStockCageForm with valid data
    def test_transfer_to_stock_cage_valid_data(self):
        pass


    # POST TransferToStockCageForm with invalid data

    # Access Transfer to Stock Cage while not logged in

    # None of the tube numbers in the formset can be identical

    # All tube numbers must exist and be integers

    # Can't transfer from the same breeding cage twice
