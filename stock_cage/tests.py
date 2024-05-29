from django.test import TestCase
from django.urls import reverse

from test_factories.model_factories import BreedingCageFactory, UserFactory


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
