from django.test import TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from test_factories.model_factories import (
    MouseFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)
from test_factories.form_factories import RepositoryMiceFormFactory
from website.models import StockCage
from mice_repository.forms import RepositoryMiceForm


class MouseTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory(strain=self.strain, stock_cage=StockCageFactory())

    # Check MouseFactory works
    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    # Primary key is "<strain>-<tube>"
    def test_mouse_pk(self):
        self.assertEqual(self.mouse.pk, "teststrain-1")

    # Tube attribute for breeding wing ID
    def test_mouse_tube_id(self):
        self.assertEqual(self.mouse.tube, 1)

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

    # Overwritten __init__ method with custom_tube
    def test_init_with_custom_tube(self):
        mouse = MouseFactory(strain=self.strain, custom_tube=123)
        self.assertEqual(mouse._tube, 123)

    # Overwritten __init__ method without custom_tube
    def test_init_without_custom_tube(self):
        mouse = Mouse(strain=self.strain)
        #self.assertIsNotNone(mouse._tube)

    # Overwritten save method with custom_tube
    def test_save_with_custom_tube(self):
        mouse = Mouse(strain=self.strain, custom_tube=123)
        mouse.save()
        self.assertEqual(mouse._tube, 123)


class RepositoryMiceFormTestCase(TestCase):    
    def setUp(self):
        self.strain = StrainFactory()

    # Valid data
    def test_mice_form_valid_data(self):
        form = RepositoryMiceForm(data=RepositoryMiceFormFactory.valid_data())
        self.assertTrue(form.is_valid())

    # Invalid dob
    def test_mice_form_invalid_dob(self):
        form = RepositoryMiceForm(data=RepositoryMiceFormFactory.invalid_dob())
        self.assertFalse(form.is_valid())

    # No duplicate mice
    """
    def test_mice_form_duplicate_mice(self):
        self.mouse = MouseFactory()
        form = RepositoryMiceForm(data=RepositoryMiceFormFactory.duplicate_mice(strain=self.mouse.strain, _tube=self.mouse.tube))
        self.assertFalse(form.is_valid())
    """

    # Can't alter mouse._global_id on form
    def test_mice_form_global_id(self):
        self.assertFalse("_global_id" in RepositoryMiceForm().fields)

    def test_save_custom_tube(self):
        form = RepositoryMiceForm(data=RepositoryMiceFormFactory.valid_data(custom_tube=123))
        self.assertTrue(form.is_valid())
        mouse = form.save()
        self.assertEqual(mouse._tube, 123)

    def test_save_without_custom_tube(self):
        form = RepositoryMiceForm(data=RepositoryMiceFormFactory.valid_data())
        self.assertTrue(form.is_valid())
        mouse = form.save()
        self.assertIsNotNone(mouse._tube)


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
    """
    def test_add_mouse_to_repository_view_get_request(self):
        response = self.client.get(reverse("mice_repository:add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mice_repository.html")
        self.assertIsInstance(response.context["mice_form"], RepositoryMiceForm)
    """

    # POST RequestForm with valid data
    def test_add_mouse_to_repository_post_valid(self):
        data = RepositoryMiceFormFactory.valid_data()
        response = self.client.post(reverse("mice_repository:add_mouse_to_repository"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Mouse.objects.count(), 2)
        self.assertRedirects(response, reverse("mice_repository:add_mouse_to_repository"))
