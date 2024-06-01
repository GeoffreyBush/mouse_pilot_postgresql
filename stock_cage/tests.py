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
        self.mouse1, self.mouse2 = MouseFactory(stock_cage=self.cage), MouseFactory(
            stock_cage=self.cage
        )

    def test_stock_cage_factory_count(self):
        self.assertEqual(StockCage.objects.count(), 1)

    def test_stock_cage_pk(self):
        self.assertEqual(self.cage.pk, 1)

    def test_stock_mice(self):
        self.assertEqual(self.cage.mice.count(), 2)


class BatchFromBreedingCageFormTestCase(TestCase):
    def setUp(self):
        self.strain = Strain.objects.create(strain_name="TestStrain")
        self.form = BatchFromBreedingCageFormFactory.create(strain=self.strain)

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_correct_strain(self):
        self.assertEqual(self.form.data["strain"].strain_name, "TestStrain")

    def test_correct_pk(self):
        self.mouse = self.form.save()
        self.assertEqual(self.mouse.pk, "TestStrain-123")

    def test_mouse_created(self):
        self.assertEqual(Mouse.objects.count(), 2)
        self.form.save()
        self.assertEqual(Mouse.objects.count(), 3)

    #
    def test_missing_tube_number(self):
        #self.data.pop("tube")
        form = BatchFromBreedingCageFormFactory.create(_tube=None)
        self.assertFalse(form.is_valid())

    def test_tube_number_not_integer(self):

        #self.data["tube"] = "str"
        self.form = BatchFromBreedingCageFormFactory.create(_tube="str")
        self.assertFalse(self.form.is_valid())

    def test_duplicate_global_id(self):
        self.mouse = MouseFactory(strain=self.strain)
        self.assertTrue(self.form.is_valid())
        self.data.pop("tube")
        self.form = BatchFromBreedingCageFormFactory.create(_tube=self.mouse._tube)
        self.assertFalse(self.form.is_valid())

    def test_global_id_input_field_not_visible(self):
        self.assertFalse("_global_id" in BatchFromBreedingCageForm().fields)


class TransferToStockCageViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.cage = BreedingCageFactory()
        self.valid_form = BatchFromBreedingCageFormFactory.valid_data(cage=self.cage)

    # Correct form used
    # def test_signup_view_attributes(self):
    # self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    def test_get_request_authenticated(self):
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
