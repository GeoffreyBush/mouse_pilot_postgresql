from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from mice_repository.forms import RepositoryMiceForm
from mice_repository.models import Mouse
from test_factories.form_factories import RepositoryMiceFormFactory
from test_factories.model_factories import (
    MouseFactory,
    StrainFactory,
    UserFactory,
)


class MouseModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory(strain=self.strain)

    # Check MouseFactory works
    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")
        self.assertEqual(self.mouse.pk, "teststrain-1")

    # _tube field increments automatically from strain.mice_count and sets correct _global_id
    def test_mouse_without_custom_tube(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.mouse2 = MouseFactory(strain=self.strain)
        self.assertEqual(self.strain.mice_count, 2)
        self.assertEqual(self.mouse2._tube, 2)
        self.assertEqual(self.mouse2.pk, "teststrain-2")

    # _tube can be manually set and correct _global_id created from it
    def test_mouse_custom_tube(self):
        self.mouse2 = MouseFactory(strain=self.strain, _tube=123)
        self.assertEqual(self.mouse2._tube, 123)
        self.assertEqual(self.mouse2.pk, "teststrain-123")

    # Regression test to prevent a mouse being overwritten by another
    def test_mouse_duplicate(self):
        with self.assertRaises(ValidationError):
            self.mouse2 = MouseFactory(strain=self.strain, _tube=self.mouse.tube)

    # mouse.save() method increments strain.mice.count if validate_unique() passes
    def test_mouse_count_increment_good_save(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.mouse2 = MouseFactory(strain=self.strain, _tube=123)
        self.assertEqual(self.strain.mice_count, 2)

    # mouse.save() method doesn't increment strain.mice.count if validate_unique() fails
    def test_mouse_count_no_increment_bad_save(self):
        self.assertEqual(self.strain.mice_count, 1)
        with self.assertRaises(ValidationError):
            self.mouse2 = MouseFactory(strain=self.strain, _tube=self.mouse.tube)
        self.assertEqual(self.strain.mice_count, 1)

    # is_genotyped method
    def test_mouse_genotyped(self):
        self.assertFalse(self.mouse.is_genotyped())
        self.mouse.earmark = "TR"
        self.mouse.save()
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())


class RepositoryMiceFormTestCase(TestCase):
    def setUp(self):
        self.strain = StrainFactory()
        self.form = RepositoryMiceForm(
            data=RepositoryMiceFormFactory.valid_data(strain=self.strain, _tube=1)
        )
        self.mouse = self.form.save()
        self.strain.refresh_from_db()

    # Valid data
    def test_mice_form_valid_data(self):
        self.assertTrue(self.form.is_valid())

    # Correct mice count
    def test_mice_form_mice_count(self):
        self.assertEqual(Mouse.objects.all().count(), 1)
        self.assertEqual(self.strain.mice_count, 1)

    # If no tube is provided on form, tube value is set to strain.mice_count
    def test_save_without_custom_tube(self):
        self.assertEqual(self.mouse._tube, self.mouse.strain.mice_count)

    # Invalid dob
    def test_mice_form_invalid_dob(self):
        self.invalid_dob_form = RepositoryMiceForm(
            data=RepositoryMiceFormFactory.invalid_dob()
        )
        self.assertFalse(self.invalid_dob_form.is_valid())
        self.assertIn("dob", self.invalid_dob_form.errors)

    # Can't alter mouse._global_id on form
    def test_mice_form_global_id(self):
        self.assertFalse("_global_id" in RepositoryMiceForm().fields)

    # Can set a custom tube on form
    def test_save_custom_tube(self):
        form = RepositoryMiceForm(data=RepositoryMiceFormFactory.valid_data(_tube=123))
        self.assertTrue(form.is_valid())
        self.mouse2 = form.save()
        self.assertEqual(self.mouse2._tube, 123)


class MiceRepositoryViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()

    # GET mice_repository while logged in
    def test_mice_repository_view_get_request(self):
        response = self.client.get(reverse("mice_repository:mice_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mice_repository.html")
        self.assertIn("mymice", response.context)
        self.assertIn(self.mouse, response.context["mymice"])


class AddMouseToRepositoryViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()

    # GET add_mouse_to_repository while logged in
    def test_add_mouse_to_repository_view_get_request(self):
        response = self.client.get(reverse("mice_repository:add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_mouse_to_repository.html")
        self.assertIsInstance(response.context["mice_form"], RepositoryMiceForm)

    # POST RequestForm with valid data
    def test_add_mouse_to_repository_post_valid(self):
        data = RepositoryMiceFormFactory.valid_data()
        response = self.client.post(
            reverse("mice_repository:add_mouse_to_repository"), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("mice_repository:mice_repository"))
        self.assertEqual(Mouse.objects.all().count(), 2)
