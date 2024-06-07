from django.test import Client, TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import BatchFromBreedingCageFormFactory
from mouse_pilot_postgresql.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StockCageFactory,
    UserFactory,
)
from stock_cage.forms import BatchFromBreedingCageForm
from stock_cage.models import StockCage
from website.models import Strain


class PupsToStockCageViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory(username="testuser")
        cls.cage = BreedingCageFactory()
        cls.valid_form = BatchFromBreedingCageFormFactory.valid_data(cage=cls.cage)

    # Correct form used
    # def test_signup_view_attributes(self):
    # self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    def test_get_request_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("wean_pups:pups_to_stock_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pups_to_stock_cage.html")

    # POST TransferToStockCageForm with valid data
    # If tube numbers given, correct assignment
    def test_pups_to_stock_cage_valid_data(self):
        pass

    # POST TransferToStockCageForm with invalid data

    # Access Transfer to Stock Cage while not logged in

    # None of the tube numbers in the formset can be identical

    # If no tube numbers given, correct default assignment when formset is loaded

    # All tube numbers must exist in the formset

    # Can't transfer from the same breeding cage twice
