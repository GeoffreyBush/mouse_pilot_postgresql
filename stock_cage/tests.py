from django.test import TestCase, Client
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


class StockCageModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = StockCageFactory()
        cls.mouse1, cls.mouse2 = MouseFactory(stock_cage=cls.cage), MouseFactory(
            stock_cage=cls.cage
        )

    def test_stock_cage_factory_count(self):
        self.assertEqual(StockCage.objects.count(), 1)

    def test_stock_cage_pk(self):
        self.assertEqual(self.cage.pk, 1)

    # Test box_no equivalent when that information is provided by breeding wing

    def test_stock_mice(self):
        self.assertEqual(self.cage.mice.count(), 2)


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


class TransferToStockCageViewTestCase(TestCase):
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
            reverse("stock_cage:transfer_to_stock_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transfer_to_stock_cage.html")

    # POST TransferToStockCageForm with valid data
    # If tube numbers given, correct assignment
    def test_transfer_to_stock_cage_valid_data(self):
        pass

    # POST TransferToStockCageForm with invalid data

    # Access Transfer to Stock Cage while not logged in

    # None of the tube numbers in the formset can be identical

    # If no tube numbers given, correct default assignment when formset is loaded

    # All tube numbers must exist in the formset

    # Can't transfer from the same breeding cage twice
