
from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError

from mice_repository.forms import RepositoryMiceForm
from mice_repository.models import Mouse
from test_factories.form_factories import RepositoryMiceFormFactory
from test_factories.model_factories import (
    MouseFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)
from website.models import StockCage


class MouseTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory(strain=self.strain, stock_cage=StockCageFactory())

    # Check MouseFactory works
    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    # No duplicate mice
    def test_mouse_duplicate(self):
        with self.assertRaises(IntegrityError):
            self.mouse2 = MouseFactory(strain=self.strain, _tube=self.mouse.tube)

    # _tube field increments automatically from strain.mice_count
    def test_mouse_without_custom_tube(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.mouse2 = MouseFactory(strain=self.strain)
        self.assertEqual(self.strain.mice_count, 2)
        self.assertEqual(self.mouse2._tube, 2)
        self.assertEqual(self.mouse2.pk, "teststrain-2")

    # _tube can be manually set
    def test_mouse_custom_tube(self):
        self.assertEqual(self.strain.mice_count, 1)
        self.mouse2 = MouseFactory(strain=self.strain, _tube=123)
        self.assertEqual(self.strain.mice_count, 2)
        self.assertEqual(self.mouse2._tube, 123)
        self.assertEqual(self.mouse2.pk, "teststrain-123")

    # Count mice from a stock cage using related_name="mice" argument
    def test_mouse_stock_cage(self):
        self.assertIsInstance(self.mouse.stock_cage, StockCage)
        self.assertEqual(self.mouse.stock_cage.cage_id, 1)
        self.assertEqual(self.mouse.stock_cage.mice.count(), 1)

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
        self.form = RepositoryMiceForm(data=RepositoryMiceFormFactory.valid_data())
        self.mouse = self.form.save()

    # Valid data
    def test_mice_form_valid_data(self):
        self.assertTrue(self.form.is_valid())
        self.assertIsInstance(self.mouse, Mouse)

    # If no tube is provided on form, tube value is set to strain.mice_count
    def test_save_without_custom_tube(self):
        self.assertEqual(self.mouse._tube, self.mouse.strain.mice_count)

    # Invalid dob
    def test_mice_form_invalid_dob(self):
        self.invalid_dob_form = RepositoryMiceForm(data=RepositoryMiceFormFactory.invalid_dob())
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
        self.assertRedirects(
            response, reverse("mice_repository:mice_repository")
        )