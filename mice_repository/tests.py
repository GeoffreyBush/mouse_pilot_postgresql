from datetime import date

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
    global test_user, test_client, test_dob
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)
    test_dob = date.fromisoformat("2020-01-01")


def tearDownModule():
    global test_user
    test_user.delete()


class MouseModelNoDBTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory.build(strain=self.strain, dob=test_dob)

    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)

    def test_correct_strain(self):
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    def test_clean_correct_pk(self):
        self.assertEqual(self.mouse.pk, "")
        self.mouse.clean()
        self.assertEqual(self.mouse.pk, "teststrain-1")

    # More clean() tests

    def test_manual_tube_correct_value(self):
        self.manual_tube_mouse = MouseFactory(strain=self.strain, tube=123)
        self.assertEqual(self.manual_tube_mouse.tube, 123)

    def test_manual_tube_correct_pk(self):
        self.manual_tube_mouse = MouseFactory(strain=self.strain, tube=123)
        self.assertEqual(self.manual_tube_mouse.pk, "teststrain-123")

    def test_correct_age(self):
        correct_age = (date.today() - self.mouse.dob).days
        self.assertEqual(self.mouse.age, correct_age)

    def test_adding_earmark_auto_genotypes_mouse(self):
        self.assertFalse(self.mouse.is_genotyped())
        self.mouse.earmark = "TR"
        self.assertTrue(self.mouse.is_genotyped())

    def test_cull_method_sets_culled_date(self):
        self.assertEqual(self.mouse.culled_date, None)
        self.mouse.cull(date.today())
        self.assertEqual(self.mouse.culled_date, date.today())

    def test_is_culled_method(self):
        self.assertFalse(self.mouse.is_culled())
        self.mouse.cull(date.today())
        self.assertTrue(self.mouse.is_culled())

    def test_cull_method_raises_error_when_already_culled(self):
        self.assertFalse(self.mouse.is_culled())
        self.mouse.cull(date.today())
        with self.assertRaises(ValidationError):
            self.mouse.cull(date.today())


class MouseModelWithDBTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory.create(strain=self.strain)

    def test_mouse_correct_auto_pk(self):
        self.assertEqual(self.mouse.pk, "teststrain-1")

    def test_mouse_auto_tube_increments_correctly(self):
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.auto_tube_mouse.tube, 2)

    def test_mouse_auto_tube_increments_pk_correctly(self):
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.auto_tube_mouse.pk, "teststrain-2")

    def test_mouse_cannot_be_overwritten_by_duplicate_tube(self):
        with self.assertRaises(ValidationError):
            self.duplicate_mouse = MouseFactory(
                strain=self.strain, tube=self.mouse.tube
            )

    def test_increment_strain_count_when_validate_unique_mouse_passes(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.extra_mouse = MouseFactory(strain=self.strain, tube=5)
        self.assertEqual(self.strain.mice_count, 2)

    def test_no_increment_strain_count_when_validate_unique_mouse_fails(self):
        self.assertEqual(self.strain.mice_count, 1)
        with self.assertRaises(ValidationError):
            self.duplicate_mouse = MouseFactory(
                strain=self.strain, tube=self.mouse.tube
            )
        self.assertEqual(self.strain.mice_count, 1)

    # Mother must be female

    # Father must be male

    # Parents cannot be born after child

    # clipped_date must be after dob. All dates must be after dob

    # dob must be in the past

    # If the mouse is genotyped, the genotyper must be set


class RepositoryMiceFormTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory.create()

    def test_valid_data(self):
        form = RepositoryMiceFormFactory.build()
        self.assertTrue(form.is_valid())

    def test_form_creates_mouse(self):
        self.form = RepositoryMiceFormFactory.build()
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.form.save()
        self.assertEqual(Mouse.objects.all().count(), 1)

    def test_invalid_dob(self):
        form = RepositoryMiceFormFactory.build(dob=None)
        self.assertIn("dob", form.errors)

    def test_no_global_id_field(self):
        self.assertFalse("_global_id" in RepositoryMiceForm().fields)

    def test_manual_correct_tube_value(self):
        self.form = RepositoryMiceFormFactory.build(tube=123)
        self.mouse = self.form.save()
        self.assertEqual(self.mouse.tube, 123)

    def test_manual_tube_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.build(strain=self.strain, tube=123)
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.mouse = self.form.save()
        self.assertEqual(self.strain.mice_count, 1)

    def test_auto_tube_correct_tube_value(self):
        self.mouse1 = MouseFactory.create(strain=self.strain)
        self.form = RepositoryMiceFormFactory.build(strain=self.strain)
        self.mouse2 = self.form.save()
        self.assertEqual(self.mouse2.tube, 2)

    def test_auto_tube_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.build(strain=self.strain)
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.form.save()
        self.assertEqual(self.strain.mice_count, 1)

    def test_tube_is_none_correct_tube_value(self):
        self.mouse1 = MouseFactory.create(strain=self.strain)
        self.form = RepositoryMiceFormFactory.build(strain=self.strain, tube=None)
        self.mouse2 = self.form.save()
        self.assertEqual(self.mouse2.tube, 2)

    def test_tube_is_none_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.build(strain=self.strain, tube=None)
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.form.save()
        self.assertEqual(self.strain.mice_count, 1)

    # Mother choices are female

    # Father choices are male


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


"""
class AddMouseToRepositoryViewPostTest(TestCase):

    def test_post_valid_form_data(self):
        self.assertEqual(Mouse.objects.all().count(), 0)
        data = RepositoryMiceFormFactory.valid_data()
        response = test_client.post(
            reverse("mice_repository:add_mouse_to_repository"), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("mice_repository:mice_repository"))
        self.assertEqual(Mouse.objects.all().count(), 1)
"""


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
