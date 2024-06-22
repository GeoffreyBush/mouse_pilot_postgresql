from django.db import IntegrityError
from django.test import Client, TestCase

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    StrainFactory,
    UserFactory,
)
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

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")

    def test_strain_creation(self):
        self.assertIsInstance(self.strain, Strain)

    def test_strain_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Strain.objects.create(strain_name="teststrain")

    def test_strain_increment_mice_count(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.mouse = MouseFactory.create(strain=self.strain)
        self.assertEqual(self.strain.mice_count, 1)

    def test_strain_mice_count_decrement_from_one(self):
        self.strain.mice_count = 1
        self.assertEqual(self.strain.mice_count, 1)
        self.strain.decrement_mice_count()
        self.assertEqual(self.strain.mice_count, 0)

    def test_strain_mice_count_cannot_decrement_below_zero(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.strain.decrement_mice_count()
        self.assertEqual(self.strain.mice_count, 0)

    # Decrement mice count from zero should never be possible for a user to do

    # Deleting a mouse should decrement the mice count

    # Changing the strain of a mouse should increment the new strain's mice count

    # Changing the strain of a mouse should decrement the old strain's mice count

    # Should the increment/decrement methods be a related_name instead?


class StrainManagementViewGetTest(TestCase):

    def test_strain_management_view(self):
        response = test_client.get("/strain/strain_management")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "strain_management.html")
