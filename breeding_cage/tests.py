from datetime import date

from django.test import TestCase
from django.urls import reverse
from faker import Faker

from breeding_cage.forms import BreedingCageForm
from breeding_cage.models import BreedingCage
from website.models import Mouse, StockCage
from website.tests.form_factories import BreedingCageFormFactory
from website.tests.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StrainFactory,
    UserFactory,
)

fake = Faker()


class BreedingModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory()
        self.mother = MouseFactory(sex="F", strain=self.strain)
        self.father = MouseFactory(sex="M", strain=self.strain)
        self.breeding_cage = BreedingCageFactory(
            mother=self.mother, father=self.father, male_pups=5, female_pups=3
        )
        self.stock_cage = self.breeding_cage.transfer_to_stock()
        self.new_mouse = Mouse.objects.all().last()

    # Confirm creation of breeding cage
    def test_breeding_cage_creation(self):
        self.assertIsInstance(self.breeding_cage, BreedingCage)
        self.assertIsNotNone(self.breeding_cage.mother)
        self.assertIsNotNone(self.breeding_cage.father)

    # transfer_to_stock method creates a stock cage
    def test_transfer_creates_stock_cage(self):
        self.assertIsInstance(self.stock_cage, StockCage)

    # transfer_to_stock method changed boolean attribute on breeding cage
    def test_transfer_sets_breeding_cage_attributes(self):
        self.assertTrue(self.breeding_cage.transferred_to_stock)

    # transfer_to_stock method creates mice in stock cage
    def test_transfer_creates_mice(self):
        self.assertEqual(Mouse.objects.filter(sex="M").count(), 6)
        self.assertEqual(Mouse.objects.filter(sex="F").count(), 4)
        self.assertEqual(self.stock_cage.mice.count(), 8)

    # transfer_to_stock method creates mice with the correct attributes
    def test_mice_attributes_created_by_transfer(self):
        self.assertEqual(self.new_mouse.strain, self.mother.strain)
        self.assertEqual(self.new_mouse.mother, self.mother)
        self.assertEqual(self.new_mouse.father, self.father)
        self.assertEqual(self.new_mouse.dob, date.today())


class BreedingCageFormTestCase(TestCase):

    # Valid data
    def test_valid_form(self):
        form = BreedingCageForm(data=BreedingCageFormFactory.valid_data())
        self.assertTrue(form.is_valid())

    # Missing box_no
    def test_invalid_box_no(self):
        form = BreedingCageForm(data=BreedingCageFormFactory.invalid_box_no())
        self.assertFalse(form.is_valid())
        self.assertIn("box_no", form.errors)

    # Invalid mother
    def test_invalid_mother(self):
        form = BreedingCageForm(data=BreedingCageFormFactory.invalid_mother())
        self.assertFalse(form.is_valid())
        self.assertIn("mother", form.errors)


class ListBreedingCagesViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.strain = StrainFactory()
        self.cage = BreedingCageFactory()

    # Access breeding wing dashboard logged in
    def test_list_breeding_cages_view_authenticated_user(self):
        response = self.client.get(reverse("breeding_cage:list_breeding_cages"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_breeding_cages.html")
        self.assertIn("mycages", response.context)
        self.assertIn(self.cage, response.context["mycages"])

    # Access breeding wing dashboard without logging in
    def test_list_breeding_cages_view_unauthenticated_user(self):
        self.client.logout()
        url = reverse("breeding_cage:list_breeding_cages")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class ViewBreedingCageViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.cage = BreedingCageFactory()
        self.client.login(username="testuser", password="testpassword")

    # Access breeding wing cage view logged in
    def test_view_breeding_cage_with_authenticated_user(self):
        response = self.client.get(
            reverse("breeding_cage:view_breeding_cage", args=[self.cage.box_no])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_breeding_cage.html")
        self.assertIn("mycage", response.context)
        self.assertEqual(response.context["mycage"], self.cage)

    # Access breeding wing cage view without logging in
    def test_view_breeding_cage_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse("breeding_cage:view_breeding_cage", args=[self.cage.box_no])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class AddBreedingCageViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")

    # Access Create Breeding Cage while logged in
    def test_create_breeding_cage_get_with_authenticated_user(self):
        response = self.client.get(reverse("breeding_cage:add_breeding_cage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_breeding_cage.html")

    # POST BreedingCageForm with valid data
    def test_create_breeding_cage_post_valid(self):
        data = BreedingCageFormFactory.valid_data()
        response = self.client.post(reverse("breeding_cage:add_breeding_cage"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("breeding_cage:list_breeding_cages"))

    # POST BreedingCageForm with invalid mother
    def test_create_breeding_cage_post_invalid(self):
        data = BreedingCageFormFactory.invalid_mother()
        response = self.client.post(reverse("breeding_cage:add_breeding_cage"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_breeding_cage.html")

    # Access add cage while not logged in
    def test_create_breeding_cage_get_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse("breeding_cage:add_breeding_cage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


# Edit breeding cage view
