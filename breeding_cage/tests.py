from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from breeding_cage.forms import BreedingCageForm
from breeding_cage.models import BreedingCage
from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import BreedingCageFormFactory
from mouse_pilot_postgresql.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StrainFactory,
    UserFactory,
)


class BreedingCageModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory()
        self.mother = MouseFactory(sex="F", strain=self.strain)
        self.father = MouseFactory(sex="M", strain=self.strain)
        self.breeding_cage = BreedingCageFactory(
            mother=self.mother, father=self.father, male_pups=5, female_pups=3
        )
        self.new_mouse = Mouse.objects.all().last()

    # Confirm BreedingCageFactory works
    def test_breeding_cage_creation(self):
        self.assertIsInstance(self.breeding_cage, BreedingCage)
        self.assertIsNotNone(self.breeding_cage.mother)
        self.assertIsNotNone(self.breeding_cage.father)

    # transferred_to_stock attribute exists
    def test_transferred_to_stock(self):
        self.assertIsNotNone(self.breeding_cage.transferred_to_stock)

    # box_no is not a primary key (causes problems in duplication if it is) so its uniqueness is not enforced by Django by default
    def test_box_no_unique(self):
        self.assertEqual(self.breeding_cage.box_no, "box0")
        with self.assertRaises(IntegrityError):
            self.breeding_cage2 = BreedingCageFactory(box_no="box0")


class BreedingCageFormTestCase(TestCase):

    def setUp(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.valid_data())
        self.breeding_cage = self.form.save()

    # Valid data
    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(BreedingCage.objects.count(), 1)
        self.assertEqual(self.breeding_cage.box_no, "1")

    # Missing box_no
    def test_invalid_father(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.invalid_father())
        self.assertFalse(self.form.is_valid())
        self.assertIn("father", self.form.errors)

    # Invalid mother
    def test_invalid_mother(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.invalid_mother())
        self.assertFalse(self.form.is_valid())
        self.assertIn("mother", self.form.errors)


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
        self.assertEqual(BreedingCage.objects.count(), 1)

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


class EditBreedingCageViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.cage = BreedingCageFactory()

    # Access Edit Breeding Cage while logged in
    def test_edit_breeding_cage_get_authenticated_user(self):
        response = self.client.get(
            reverse("breeding_cage:edit_breeding_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_breeding_cage.html")

    # POST BreedingCageForm with valid data
    def test_edit_breeding_cage_post_valid(self):
        data = BreedingCageFormFactory.valid_data()
        data["box_no"] = "new"
        response = self.client.post(
            reverse("breeding_cage:edit_breeding_cage", args=[self.cage]), data
        )
        self.cage.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("breeding_cage:list_breeding_cages"))
        self.assertEqual(self.cage.box_no, "new")

    # POST BreedingCageForm with invalid mother
    def test_edit_breeding_cage_post_invalid(self):
        data = BreedingCageFormFactory.invalid_mother()
        response = self.client.post(
            reverse("breeding_cage:edit_breeding_cage", args=[self.cage]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_breeding_cage.html")

    # Access add cage while not logged in
    def test_edit_breeding_cage_get_unauthenticated_user(self):
        self.client.logout()
        url = reverse("breeding_cage:edit_breeding_cage", args=[self.cage])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")
