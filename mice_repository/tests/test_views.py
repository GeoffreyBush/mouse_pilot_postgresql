from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from mice_repository.forms import RepositoryMiceForm
from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import RepositoryMiceFormFactory
from mouse_pilot_postgresql.model_factories import MouseFactory, UserFactory


def setUpModule():
    global test_user, test_client, test_dob
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)
    test_dob = date.fromisoformat("2020-01-01")


def tearDownModule():
    global test_user
    test_user.delete()


class MiceRepositoryViewGetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.response = test_client.get(reverse("mice_repository:mice_repository"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "mice_repository.html")

    def test_context_contains_mymice(self):
        self.assertIn("mymice", self.response.context)

    def test_context_contains_mouse(self):
        self.assertIn(self.mouse, self.response.context["mymice"])


class AddMouseToRepositoryViewGetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(
            reverse("mice_repository:add_mouse_to_repository")
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "add_mouse_to_repository.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["mice_form"], RepositoryMiceForm)


class AddMouseToRepositoryViewPostTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.post(
            reverse("mice_repository:add_mouse_to_repository"),
            RepositoryMiceFormFactory.valid_data(),
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertRedirects(self.response, reverse("mice_repository:mice_repository"))

    def test_mouse_created(self):
        self.assertEqual(Mouse.objects.all().count(), 1)


class EditMouseInRepositoryViewGetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.response = test_client.get(
            reverse("mice_repository:edit_mouse_in_repository", args=[cls.mouse.pk])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "edit_mouse_in_repository.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], RepositoryMiceForm)

    def test_context_contains_mouse(self):
        self.assertIn("mouse", self.response.context)

    def test_context_contains_mouse_instance(self):
        self.assertEqual(self.mouse, self.response.context["mouse"])


class EditMouseInRepositoryViewPostTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory(coat="Black")
        data = RepositoryMiceFormFactory.valid_data(coat="White")
        cls.response = test_client.post(
            reverse("mice_repository:edit_mouse_in_repository", args=[cls.mouse.pk]),
            data,
        )
        cls.mouse.refresh_from_db()

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertRedirects(self.response, reverse("mice_repository:mice_repository"))

    def test_mouse_updated(self):
        self.assertEqual(self.mouse.coat, "White")
