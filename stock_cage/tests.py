from django.test import TestCase
from django.urls import reverse

from stock_cage.models import StockCage
from test_factories.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StockCageFactory,
    UserFactory,
)


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
        pass


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
