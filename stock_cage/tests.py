from datetime import date

from django.test import TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from stock_cage.forms import CreateMouseFromBreedingCageForm
from stock_cage.models import StockCage
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
        self.cage.mice.add(MouseFactory(), MouseFactory())

    # Check StockCageFactory works
    def test_stock_cage_factory(self):
        self.assertEqual(StockCage.objects.count(), 1)
        self.assertEqual(self.cage.cage_id, 1)

    # Mice many-to-many
    def test_stock_mice(self):
        self.assertEqual(self.cage.mice.count(), 2)


class CreateMouseFromBreedingCageFormTestCase(TestCase):
    def setUp(self):
        self.strain = Strain.objects.create(strain_name="TestStrain")
        self.assertEqual(Strain.objects.count(), 1)
        self.data = {
            "_tube": 123,
            "sex": "M",
            "coat": "Black",
            "strain": self.strain,
            "mother": MouseFactory(sex="F", strain=self.strain),
            "father": MouseFactory(sex="M", strain=self.strain),
            "dob": date.today(),
        }
        self.form = CreateMouseFromBreedingCageForm(data=self.data)

    # Valid data
    def test_valid_data(self):
        self.assertEqual(self.form.data["strain"].strain_name, 'TestStrain')
        self.assertTrue(self.form.is_valid())

    # Mouse is created with valid data
    def test_mouse_created(self):
        self.assertEqual(Mouse.objects.count(), 2)
        self.form.save()
        self.assertEqual(Mouse.objects.count(), 3)

    # Missing tube number
    def test_missing_tube_number(self):
        self.data.pop("_tube")
        form = CreateMouseFromBreedingCageForm(data=self.data)
        self.assertFalse(form.is_valid())

    # All potential _global_id are unique before attempting to batch create mice


class TransferToStockCageViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.cage = BreedingCageFactory()

    # Access Transfer to Stock Cage while logged in
    def test_transfer_to_stock_cage_authenticated_user(self):
        response = self.client.get(
            reverse("stock_cage:transfer_to_stock_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transfer_to_stock_cage.html")

    # POST TransferToStockCageForm with valid data

    # POST TransferToStockCageForm with invalid data

    # Access Transfer to Stock Cage while not logged in
