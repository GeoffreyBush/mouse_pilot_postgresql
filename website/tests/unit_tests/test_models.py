from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from website.models import CustomUser, Mouse, Project, Request, Strain
from website.tests.factories import UserFactory

#############
### MOUSE ###
#############


class MouseTest(TestCase):
    pass


##################
### CUSTOMUSER ###
##################
class CustomUserTest(TestCase):

    @classmethod
    # Create test user
    def setUp(self):
        self.user = UserFactory(username="testuser", email="testuser@example.com")

    # No duplicate usernames
    def test_user_with_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            UserFactory().create_valid_user(username="testuser")

    # No duplicate emails
    def test_user_with_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            UserFactory().create_valid_user(email="testuser@example.com")


###############
### REQUEST ###
###############


class RequestModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123",
        )
        self.mouse1 = Mouse.objects.create(dob=date.today())
        self.mouse2 = Mouse.objects.create(dob=date.today())
        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse1, self.mouse2)

    # Request creation
    def test_request_creation(self):
        self.assertEqual(self.request.request_id, 1)
        self.assertEqual(self.request.researcher, self.user)
        self.assertEqual(self.request.task_type, "Cl")
        self.assertFalse(self.request.confirmed)
        self.assertIsNone(self.request.new_message)
        self.assertIsNone(self.request.message_history)

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


##############
### STRAIN ###
##############
class StrainTestCase(TestCase):

    @classmethod
    # Initial Strain
    def setUpTestData(cls):
        Strain.objects.create(strain_name="CRE1")

    # Uniqueness
    def test_strain_uniqueness(self):
        with self.assertRaises(Exception):
            Strain.objects.create(strain_name="CRE1")


###############
### PROJECT ###
###############
class ProjectModelTest(TestCase):

    @classmethod
    # Initial Project
    def setUpTestData(cls):
        strain1 = Strain.objects.create(strain_name="FLOX")
        strain2 = Strain.objects.create(strain_name="CMV")
        user1 = CustomUser.objects.create(
            username="TestUser1", password="testpassword", email="testemail1@test.com"
        )
        user2 = CustomUser.objects.create(
            username="TestUser2", password="testpassword", email="testemail2@test.com"
        )
        project = Project.objects.create(
            projectname="TestName",
            researcharea="TestArea",
        )
        project.strains.add(strain1, strain2)
        project.researchers.add(user1, user2)

    # Strains many-to-many
    def test_project_strains(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(
            project.strains.count(),
            2,
            "Incorrect number of strains associated with the project.",
        )

    # Researchers many-to-many
    def test_project_researchers(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(
            project.researchers.count(),
            2,
            "Incorrect number of researchers associated with the project.",
        )

    # Mouse count
    def test_project_mice_count(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(project.mice_count, 0)
        project.mice_count += 1
        self.assertEqual(project.mice_count, 1)
