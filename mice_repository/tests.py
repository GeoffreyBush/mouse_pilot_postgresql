from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from mice_repository.forms import RepositoryMiceForm
from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import RepositoryMiceFormFactory
from mouse_pilot_postgresql.model_factories import (
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


class MouseModelTestCase(TestCase):
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory(strain=self.strain)

    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)

    def test_mouse_correct_strain(self):
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    def test_mouse_correct_pk(self):
        self.assertEqual(self.mouse.pk, "teststrain-1")

    def test_mouse_auto_tube_increments_correctly(self):
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.auto_tube_mouse._tube, 2)

    def test_mouse_auto_tube_increments_pk_correctly(self):
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.auto_tube_mouse.pk, "teststrain-2")

    def test_mouse_manual_tube_correct_value(self):
        self.manual_tube_mouse = MouseFactory(strain=self.strain, _tube=123)
        self.assertEqual(self.manual_tube_mouse._tube, 123)

    def test_mouse_manual_tube_correct_pk(self):
        self.manual_tube_mouse = MouseFactory(strain=self.strain, _tube=123)
        self.assertEqual(self.manual_tube_mouse.pk, "teststrain-123")

    def test_correct_age(self):
        self.assertEqual(self.mouse.age, 0)

    def test_mouse_cannot_be_overwritten_by_duplicate_tube(self):
        with self.assertRaises(ValidationError):
            self.duplicate_mouse = MouseFactory(
                strain=self.strain, _tube=self.mouse.tube
            )

    def test_increment_strain_count_when_validate_unique_mouse_passes(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.extra_mouse = MouseFactory(strain=self.strain, _tube=5)
        self.assertEqual(self.strain.mice_count, 2)

    def test_no_increment_strain_count_when_validate_unique_mouse_fails(self):
        self.assertEqual(self.strain.mice_count, 1)
        with self.assertRaises(ValidationError):
            self.duplicate_mouse = MouseFactory(
                strain=self.strain, _tube=self.mouse.tube
            )
        self.assertEqual(self.strain.mice_count, 1)

    def test_mouse_adding_earmark_auto_genotypes_mouse(self):
        self.assertFalse(self.mouse.is_genotyped())
        self.mouse.earmark = "TR"
        self.mouse.save()
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())

    def test_mouse_cull_sets_culled(self):
        self.assertFalse(self.mouse.culled)
        self.mouse.cull()
        self.assertTrue(self.mouse.culled)

    def test_mouse_cull_raises_error_when_already_culled(self):
        self.assertFalse(self.mouse.culled)
        self.mouse.cull()
        with self.assertRaises(ValidationError):
            self.mouse.cull()

    # Mother must be female

    # Father must be male

    # Parents cannot be born after child

    # clipped_date must be after dob

    # If the mouse is genotyped, the genotyper must be set


class RepositoryMiceFormTestCase(TestCase):
    def setUp(self):
        self.strain = StrainFactory()

    def test_valid_data(self):
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=1)
        self.assertTrue(self.form.is_valid())

    def test_invalid_dob(self):
        self.invalid_dob_form = RepositoryMiceFormFactory.create(dob=None)
        self.assertIn("dob", self.invalid_dob_form.errors)

    def test_initial_strain_mice_count(self):
        self.assertEqual(self.strain.mice_count, 0)

    def test_no_global_id_field(self):
        self.assertFalse("_global_id" in RepositoryMiceForm().fields)

    def test_mouse_model_count(self):
        self.form = RepositoryMiceFormFactory.create()
        self.form.save()
        self.assertEqual(Mouse.objects.all().count(), 1)

    def test_manual_correct_tube_value(self):
        self.form = RepositoryMiceFormFactory.create(_tube=123)
        self.mouse = self.form.save()
        self.assertEqual(self.mouse._tube, 123)

    def test_manual_tube_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=123)
        self.mouse = self.form.save()
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.mice_count, 1)

    def test_auto_tube_correct_tube_value(self):
        self.form = RepositoryMiceFormFactory.create(strain=self.strain)
        self.mouse = self.form.save()
        self.assertEqual(self.mouse._tube, 1)

    def test_auto_tube_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.create(strain=self.strain)
        self.form.save()
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.mice_count, 1)

    def test_tube_is_none_correct_tube_value(self):
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=None)
        self.mouse = self.form.save()
        self.assertEqual(self.mouse._tube, 1)

    def test_tube_is_none_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=None)
        self.form.save()
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.mice_count, 1)

    # Mother choices are female

    # Father choices are male


class MiceRepositoryViewTestCase(TestCase):
    def setUp(self):
        self.mouse = MouseFactory()

    def test_get_request_authenticated(self):
        response = test_client.get(reverse("mice_repository:mice_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mice_repository.html")
        self.assertIn("mymice", response.context)
        self.assertIn(self.mouse, response.context["mymice"])


class AddMouseToRepositoryViewTestCase(TestCase):

    def test_get_request_authenticated(self):
        response = test_client.get(reverse("mice_repository:add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_mouse_to_repository.html")
        self.assertIsInstance(response.context["mice_form"], RepositoryMiceForm)

    def test_post_valid_form_data(self):
        self.assertEqual(Mouse.objects.all().count(), 0)
        data = RepositoryMiceFormFactory.valid_data()
        response = test_client.post(
            reverse("mice_repository:add_mouse_to_repository"), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("mice_repository:mice_repository"))
        self.assertEqual(Mouse.objects.all().count(), 1)
