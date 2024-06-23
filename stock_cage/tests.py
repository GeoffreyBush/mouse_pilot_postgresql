from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    StockCageFactory,
    UserFactory,
)
from stock_cage.forms import StockCageForm
from stock_cage.models import StockCage


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class StockCageModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = StockCageFactory()
        cls.mouse1, cls.mouse2 = MouseFactory(stock_cage=cls.cage), MouseFactory(
            stock_cage=cls.cage
        )

    def test_stock_cage_created(self):
        self.assertEqual(StockCage.objects.count(), 1)

    def test_stock_cage_pk(self):
        self.assertEqual(self.cage.pk, 1)

    def test_box_no_uniqueness(self):
        with self.assertRaises(IntegrityError):
            StockCageFactory(box_no=self.cage.box_no)

    def test_stock_mice_count(self):
        self.assertEqual(self.cage.mice.count(), 2)


class StockCageFormTestCase(TestCase):

    def test_form_is_valid(self):
        form = StockCageForm(data={"box_no": "Test Box"})
        self.assertTrue(form.is_valid())


class StockCagesViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = StockCageFactory()
        cls.response = test_client.get(reverse("stock_cage:list_stock_cages"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "list_stock_cages.html")

    def test_cage_count(self):
        self.assertEqual(self.response.context["cages"].count(), 1)


class AddStockCageViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(reverse("stock_cage:add_stock_cage"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "add_stock_cage.html")

    def test_new_cage_form(self):
        self.assertIsInstance(self.response.context["form"], StockCageForm)


class AddStockCageViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.post(
            reverse("stock_cage:add_stock_cage"), data={"box_no": "Test Box"}
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect(self):
        self.assertEqual(self.response.url, reverse("stock_cage:list_stock_cages"))

    def test_cage_created(self):
        self.assertEqual(StockCage.objects.count(), 1)
