from datetime import date, timedelta

from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from main.model_factories import StrainFactory, UserFactory, MouseFactory
from strain.forms import StrainForm
from strain.models import Strain


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class StrainModelTest(TestCase):

    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")

    def test_strain_creation(self):
        self.assertIsInstance(self.strain, Strain)

    def test_strain_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Strain.objects.create(strain_name="teststrain")

    # Decrement mice count from zero should never be possible for a user to do

    # Deleting a mouse should decrement the mice count

    # Changing the strain of a mouse should increment the new strain's mice count

    # Changing the strain of a mouse should decrement the old strain's mice count

    # Should the increment/decrement methods be a related_name instead?

class StrainModelAgeRangeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain = StrainFactory(strain_name="TestStrain")
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=40)), 
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=80)), 
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=80)), 
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=220)), 
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=220)), 
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=220)), 
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=400)),
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=400)),
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=400)),
        MouseFactory(strain=cls.strain, dob=date.today() - timedelta(days=400)),
        

    def test_lt_two_month_count(self):
        self.assertEqual(self.strain.lt_two_month_count, 1)

    def test_two_to_six_month_count(self):
        self.assertEqual(self.strain.two_to_six_month_count, 2)

    def test_six_to_twelve_month_count(self):
        self.assertEqual(self.strain.six_to_twelve_month_count, 3)

    def test_one_year_to_two_year_count(self):
        self.assertEqual(self.strain.one_to_two_year_count, 4)

    # Culled mice shouldn't be included in count

class StrainFormTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory()

    def test_form_is_valid(self):
        form = StrainForm(data={"strain_name": "teststrain"})
        self.assertTrue(form.is_valid())

    def test_duplicate_strain(self):
        form = StrainForm(data={"strain_name": self.strain.strain_name})
        self.assertFalse(form.is_valid())


class StrainManagementViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(reverse("strain:strain_management"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "strain_management.html")

    def test_strains_in_context(self):
        self.assertIsNotNone(self.response.context["strains"])


class AddStrainViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(reverse("strain:add_strain"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "add_strain.html")

    def test_form_is_add_strain_form(self):
        self.assertIsInstance(self.response.context["form"], StrainForm)


class AddStrainViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.post(
            reverse("strain:add_strain"), data={"strain_name": "teststrain"}
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect(self):
        self.assertEqual(self.response.url, reverse("strain:strain_management"))

    def test_strain_created(self):
        self.assertEqual(Strain.objects.count(), 1)
