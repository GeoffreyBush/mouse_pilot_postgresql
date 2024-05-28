from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from test_factories.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.models import Request, Strain


##################
### CUSTOMUSER ###
##################
class CustomUserTest(TestCase):

    @classmethod
    def setUp(self):
        self.user = UserFactory(username="testuser", email="testuser@example.com")

    # Try to create a user with a duplicate username
    def test_user_with_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            UserFactory(username="testuser")

    # Try to create a user with a duplicate email
    def test_user_with_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            UserFactory(email="testuser@example.com")

    # Password length too short
    def test_password_length(self):
        with self.assertRaises(ValidationError):
            validate_password("short")

    # Password too simple
    def test_password_complexity(self):
        with self.assertRaises(ValidationError):
            validate_password("12345678")

    # Password too common
    def test_password_common(self):
        with self.assertRaises(ValidationError):
            validate_password("password")

    # Password too similar to username
    def test_password_similar_to_username(self):
        with self.assertRaises(ValidationError):
            validate_password("testuser", self.user)


###############
### REQUEST ###
###############


class RequestModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.strain = StrainFactory()
        self.mouse1, self.mouse2 = MouseFactory(strain=self.strain), MouseFactory(
            strain=self.strain
        )

        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse1, self.mouse2)

    # Request creation
    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    # Test is broken until confirming clip adds an earmark
    # Confirm method
    """
    def test_request_confirm(self):
        self.assertFalse(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertFalse(mouse.is_genotyped())

        self.request.confirm()

        self.request.refresh_from_db()
        for mouse in self.request.mice.all():
            mouse.refresh_from_db()

        self.assertTrue(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertTrue(mouse.is_genotyped())
    """

    # There must be at least one mouse present in a request


##############
### STRAIN ###
##############
class StrainTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")

    # Duplicate strain name
    def test_strain_duplicates(self):
        with self.assertRaises(IntegrityError):
            Strain.objects.create(strain_name="teststrain")

    # Incremenet mice count of a strain
    def test_strain_mice_count(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.strain.mice_count, 1)


###############
### PROJECT ###
###############
class ProjectModelTest(TestCase):

    @classmethod
    # Initial Project
    def setUp(self):
        self.project = ProjectFactory()
        self.project.strains.add(StrainFactory(), StrainFactory())
        self.project.researchers.add(UserFactory(), UserFactory())

    # Strains many-to-many
    def test_project_strains(self):
        self.assertEqual(self.project.strains.count(), 2)

    # Researchers many-to-many
    def test_project_researchers(self):
        self.assertEqual(self.project.researchers.count(), 2)

    # Mouse count
    """ Replace this test to use the future class method, Project.mice_count() instead """

    def test_project_mice_count(self):
        self.assertEqual(self.project.mice_count, 0)
        self.project.mice_count += 1
        self.assertEqual(self.project.mice_count, 1)


#####################
### BREEDING CAGE ###
#####################
