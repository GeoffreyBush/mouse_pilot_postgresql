from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from mice_repository.forms import RepositoryMiceForm
from mice_repository.models import Mouse
from test_factories.form_factories import RepositoryMiceFormFactory
from test_factories.model_factories import MouseFactory, StrainFactory, UserFactory


class MouseModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory(strain=self.strain)
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.manual_tube_mouse = MouseFactory(strain=self.strain, _tube=123)

    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)

    def test_mouse_correct_strain(self):
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    def test_mouse_correct_pk(self):
        self.assertEqual(self.mouse.pk, "teststrain-1")

    def test_mouse_auto_tube_increments_correctly(self):
        self.assertEqual(self.auto_tube_mouse._tube, 2)

    def test_mouse_auto_tube_increments_pk_correctly(self):
        self.assertEqual(self.auto_tube_mouse.pk, "teststrain-2")

    def test_mouse_manual_tube_correct_value(self):
        self.assertEqual(self.manual_tube_mouse._tube, 123)

    def test_mouse_manual_tube_correct_pk(self):
        self.assertEqual(self.manual_tube_mouse.pk, "teststrain-123")

    def test_mouse_cannot_be_overwritten_by_duplicate_tube(self):
        with self.assertRaises(ValidationError):
            self.mouse4 = MouseFactory(strain=self.strain, _tube=self.mouse.tube)

    def test_increment_when_validate_unique__mouse_passes(self):
        self.assertEqual(self.strain.mice_count, 3)
        self.mouse4 = MouseFactory(strain=self.strain, _tube=5)
        self.assertEqual(self.strain.mice_count, 4)

    def test_no_increment_when_validate_unique_mouse_fails(self):
        self.assertEqual(self.strain.mice_count, 3)
        with self.assertRaises(ValidationError):
            self.mouse4 = MouseFactory(strain=self.strain, _tube=self.mouse.tube)
        self.assertEqual(self.strain.mice_count, 3)

    def test_mouse_adding_earmark_auto_genotypes_mouse(self):
        self.assertFalse(self.mouse.is_genotyped())
        self.mouse.earmark = "TR"
        self.mouse.save()
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())

    # Mother must be female

    # Father must be male

    # Parents cannot be born after child

    # clipped_date must be after dob

    # If the mouse is genotyped, the genotyper must be set


class RepositoryMiceFormTestCase(TestCase):
    def setUp(self):
        self.strain = StrainFactory()
        self.assertEqual(self.strain.mice_count, 0)
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=1)
        self.mouse = self.form.save()
        self.strain.refresh_from_db()

    def test_mice_form_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_mouse_model_count(self):
        self.assertEqual(Mouse.objects.all().count(), 1)
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=2)
        self.form.save()
        self.assertEqual(Mouse.objects.all().count(), 2)

    def test_strain_mice_count_increment(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.form = RepositoryMiceFormFactory.create(strain=self.strain, _tube=2)
        self.form.save()
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.mice_count, 2)

    def test_save_manual_tube_correct_value(self):
        self.form = RepositoryMiceFormFactory.create(_tube=123)
        self.mouse2 = self.form.save()
        self.assertEqual(self.mouse2._tube, 123)

    def test_save_auto_tube_correct_strain_mice_count(self):
        self.assertEqual(self.strain.mice_count, self.mouse._tube)
        self.form = RepositoryMiceFormFactory.create(
            strain=self.strain, _tube=self.strain.mice_count
        )
        self.mouse2 = self.form.save()
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.mice_count, self.mouse2._tube)

    def test_save_manual_tube_correct_strain_mice_count(self):
        self.strain.mice_count = 999
        self.form = RepositoryMiceFormFactory.create(strain=self.strain)
        self.mouse2 = self.form.save()
        self.assertEqual(self.mouse2._tube, 999)

    def test_mice_form_invalid_dob(self):
        self.invalid_dob_form = RepositoryMiceFormFactory.create(dob=None)
        self.assertIn("dob", self.invalid_dob_form.errors)

    def test_mice_form_has_no_global_id_field(self):
        self.assertFalse("_global_id" in RepositoryMiceForm().fields)


class MiceRepositoryViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()

    # Correct form used
    # def test_signup_view_attributes(self):
    # self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    def test_mice_repository_view_get_request_authenticated(self):
        response = self.client.get(reverse("mice_repository:mice_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mice_repository.html")
        self.assertIn("mymice", response.context)
        self.assertIn(self.mouse, response.context["mymice"])


class AddMouseToRepositoryViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")

    # Correct form used
    # def test_signup_view_attributes(self):
    # self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    def test_get_request_authenticated(self):
        response = self.client.get(reverse("mice_repository:add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_mouse_to_repository.html")
        self.assertIsInstance(response.context["mice_form"], RepositoryMiceForm)

    def test_post_valid_form_data(self):
        self.assertEqual(Mouse.objects.all().count(), 0)
        data = RepositoryMiceFormFactory.valid_data()
        response = self.client.post(
            reverse("mice_repository:add_mouse_to_repository"), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("mice_repository:mice_repository"))
        self.assertEqual(Mouse.objects.all().count(), 1)

    # Test invalid form data
