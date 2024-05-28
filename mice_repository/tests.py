from django.test import TestCase
from mice_repository.models import Mouse
from website.models import StockCage
from django.urls import reverse

from test_factories.model_factories import MouseFactory, StockCageFactory, StrainFactory, UserFactory

class MouseTest(TestCase):

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

# Rework RepositoryMiceForm to have more attributes and then come back to this test
"""

class RepositoryMiceFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.strain = StrainFactory()
        self.user = UserFactory()

    # Valid data
    def test_mice_form_valid_data(self):
        strain = StrainFactory()
        form = RepositoryMiceForm(
            data={

            }
        )

    # Invalid data

    # Duplicate mice

"""

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

    # test for add mouse to repository
    def test_add_mouse_to_repository(self):
        response = self.client.get(reverse("mice_repository:add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_mouse_to_repository.html")
        # self.assertIsInstance(response.context["form"], RepositoryMiceForm)

    # POST RequestForm with valid data
    # def test_add_mouse_to_repository_post_valid(self):
    #   data = {


# Test for adding a mouse to the repository
