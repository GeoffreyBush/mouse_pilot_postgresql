from django.db.utils import IntegrityError
from django.test import Client, TestCase
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


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class BreedingCageModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = StrainFactory()
        cls.mother = MouseFactory(sex="F", strain=cls.strain)
        cls.father = MouseFactory(sex="M", strain=cls.strain)
        cls.breeding_cage = BreedingCageFactory(
            strain=cls.strain,
            mother=cls.mother,
            father=cls.father,
            male_pups=5,
            female_pups=3,
        )
        cls.new_mouse = Mouse.objects.all().last()

    def test_creation(self):
        self.assertIsInstance(self.breeding_cage, BreedingCage)

    def test_pk(self):
        self.assertEqual(self.breeding_cage.pk, 1)

    def test_transferred_to_stock_exists(self):
        self.assertIsNotNone(self.breeding_cage.transferred_to_stock)

    def test_box_no_unique(self):
        self.assertEqual(self.breeding_cage.box_no, "box0")
        with self.assertRaises(IntegrityError):
            self.breeding_cage2 = BreedingCageFactory(box_no="box0")


class BreedingCageFormTestCase(TestCase):

    def test_valid_form(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.valid_data())
        self.assertTrue(self.form.is_valid())

    def test_invalid_father(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.invalid_father())
        self.assertIn("father", self.form.errors)

    def test_invalid_mother(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.invalid_mother())
        self.assertIn("mother", self.form.errors)


class ListBreedingCagesViewTestCase(TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.strain = StrainFactory()
        cls.cage = BreedingCageFactory()

    def test_get_authenticated(self):
        response = test_client.get(reverse("breeding_cage:list_breeding_cages"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_breeding_cages.html")
        self.assertIn("mycages", response.context)
        self.assertIn(self.cage, response.context["mycages"])


class ViewBreedingCageViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = BreedingCageFactory()

    def test_get_authenticated(self):
        response = test_client.get(
            reverse("breeding_cage:view_breeding_cage", args=[self.cage.box_no])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_breeding_cage.html")
        self.assertIn("mycage", response.context)
        self.assertEqual(response.context["mycage"], self.cage)


class AddBreedingCageViewTestCase(TestCase):

    def test_get_authenticated(self):
        response = test_client.get(reverse("breeding_cage:add_breeding_cage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_breeding_cage.html")
        self.assertIsInstance(response.context["form"], BreedingCageForm)

    def test_create_breeding_cage_post_valid(self):
        data = BreedingCageFormFactory.valid_data()
        response = test_client.post(reverse("breeding_cage:add_breeding_cage"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("breeding_cage:list_breeding_cages"))
        self.assertEqual(BreedingCage.objects.count(), 1)

    def test_create_breeding_cage_post_invalid(self):
        data = BreedingCageFormFactory.invalid_mother()
        response = test_client.post(reverse("breeding_cage:add_breeding_cage"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_breeding_cage.html")


# Cannot easily use setUpClass here. Test cages need to be isolated.
class EditBreedingCageViewTestCase(TestCase):
    def setUp(self):
        self.cage = BreedingCageFactory()

    def test_get_authenticated(self):
        response = test_client.get(
            reverse("breeding_cage:edit_breeding_cage", args=[self.cage])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_breeding_cage.html")
        self.assertIsInstance(response.context["form"], BreedingCageForm)

    def test_edit_breeding_cage_post_valid(self):
        data = BreedingCageFormFactory.valid_data()
        data["box_no"] = "new"
        response = test_client.post(
            reverse("breeding_cage:edit_breeding_cage", args=[self.cage]), data
        )
        self.cage.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("breeding_cage:list_breeding_cages"))
        self.assertEqual(self.cage.box_no, "new")

    def test_edit_breeding_cage_post_invalid(self):
        data = BreedingCageFormFactory.invalid_mother()
        response = test_client.post(
            reverse("breeding_cage:edit_breeding_cage", args=[self.cage]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_breeding_cage.html")
