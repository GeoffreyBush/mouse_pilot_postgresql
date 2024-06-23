from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from breeding_cage.forms import BreedingCageForm
from breeding_cage.models import BreedingCage
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


class BreedingCageModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = StrainFactory()
        cls.mother = MouseFactory(sex="F", strain=cls.strain)
        cls.strain.save()
        cls.father = MouseFactory(sex="M", strain=cls.strain)
        cls.breeding_cage = BreedingCageFactory(
            strain=cls.strain,
            mother=cls.mother,
            father=cls.father,
            male_pups=2,
            female_pups=3,
        )
        cls.initial_data = cls.breeding_cage.get_initial_data_for_pups()

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

    def test_get_initial_data_method(self):
        self.assertEqual(len(self.initial_data), 5)

    def test_initial_data_method_return_male(self):
        self.assertEqual(sum(1 for item in self.initial_data if item["sex"] == "M"), 2)

    def test_initial_data_method_return_female(self):
        self.assertEqual(sum(1 for item in self.initial_data if item["sex"] == "F"), 3)


class BreedingCageFormTest(TestCase):

    def test_valid_form(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.valid_data())
        self.assertTrue(self.form.is_valid())

    def test_invalid_father(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.invalid_father())
        self.assertIn("father", self.form.errors)

    def test_invalid_mother(self):
        self.form = BreedingCageForm(data=BreedingCageFormFactory.invalid_mother())
        self.assertIn("mother", self.form.errors)


class ListBreedingCagesViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = StrainFactory()
        cls.cage = BreedingCageFactory()
        cls.response = test_client.get(reverse("breeding_cage:list_breeding_cages"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "list_breeding_cages.html")

    def test_context_contains_mycages(self):
        self.assertIn("mycages", self.response.context)

    def test_context_contains_cage(self):
        self.assertIn(self.cage, self.response.context["mycages"])


class ViewBreedingCageViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = BreedingCageFactory()
        cls.response = test_client.get(
            reverse("breeding_cage:view_breeding_cage", args=[cls.cage.box_no])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "view_breeding_cage.html")

    def test_context_contains_mycage(self):
        self.assertIn("mycage", self.response.context)

    def test_context_contains_cage(self):
        self.assertEqual(self.response.context["mycage"], self.cage)


class AddBreedingCageViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(reverse("breeding_cage:add_breeding_cage"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "add_breeding_cage.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], BreedingCageForm)


class AddBreedingCageViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.post(
            reverse("breeding_cage:add_breeding_cage"),
            BreedingCageFormFactory.valid_data(),
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect(self):
        self.assertRedirects(
            self.response, reverse("breeding_cage:list_breeding_cages")
        )

    def test_create_breeding_cage_post_valid(self):
        self.assertEqual(BreedingCage.objects.count(), 1)


class AddBreedingCageViewPostInvalidTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.post(
            reverse("breeding_cage:add_breeding_cage"),
            BreedingCageFormFactory.invalid_mother(),
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "add_breeding_cage.html")

    def test_no_breeding_cage_created(self):
        self.assertEqual(BreedingCage.objects.count(), 0)


class EditBreedingCageViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = BreedingCageFactory()
        cls.response = test_client.get(
            reverse("breeding_cage:edit_breeding_cage", args=[cls.cage])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "edit_breeding_cage.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], BreedingCageForm)


class EditBreedingCageViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = BreedingCageFactory(box_no="box0")
        data = BreedingCageFormFactory.valid_data()
        data["box_no"] = "new"
        cls.response = test_client.post(
            reverse("breeding_cage:edit_breeding_cage", args=[cls.cage]),
            data,
        )
        cls.cage.refresh_from_db()

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect(self):
        self.assertRedirects(
            self.response, reverse("breeding_cage:list_breeding_cages")
        )

    def test_breeding_cage_updated(self):
        self.assertEqual(self.cage.box_no, "new")


class EditBreedingCageViewInvalidPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = BreedingCageFactory(box_no="box0")
        data = BreedingCageFormFactory.invalid_mother()
        data["box_no"] = "new"
        cls.response = test_client.post(
            reverse("breeding_cage:edit_breeding_cage", args=[cls.cage]), data
        )
        cls.cage.refresh_from_db()

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "edit_breeding_cage.html")

    def test_breeding_cage_not_updated(self):
        self.assertEqual(self.cage.box_no, "box0")
