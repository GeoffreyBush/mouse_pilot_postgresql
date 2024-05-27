from datetime import date

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from website.models import BreedingCage, Mouse, Request, StockCage, Strain
from website.tests.factories import (
    BreedingCageFactory,
    MouseFactory,
    ProjectFactory,
    StockCageFactory,
    StrainFactory,
    UserFactory,
)

#############
### MOUSE ###
#############


class MouseTest(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory(strain=self.strain, stock_cage=StockCageFactory())

    # Check MouseFactory works
    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    # Tube attribute for breeding wing ID
    def test_mouse_tube_id(self):
        self.assertEqual(self.mouse.tube, "teststrain-1")

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


class BreedingCageTest(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory()
        self.mother = MouseFactory(sex="F", strain=self.strain)
        self.father = MouseFactory(sex="M", strain=self.strain)
        self.breeding_cage = BreedingCageFactory(
            mother=self.mother, father=self.father, male_pups=5, female_pups=3
        )
        self.stock_cage = self.breeding_cage.transfer_to_stock()
        self.new_mouse = Mouse.objects.all().last()

    # Confirm creation of breeding cage
    def test_breeding_cage_creation(self):
        self.assertIsInstance(self.breeding_cage, BreedingCage)
        self.assertIsNotNone(self.breeding_cage.mother)
        self.assertIsNotNone(self.breeding_cage.father)

    # Stock cage is created by transfer_to_stock method
    def test_transfer_creates_stock_cage(self):
        self.assertIsInstance(self.stock_cage, StockCage)

    # transfer_to_stock method changed boolean attribute on breeding cage
    def test_transfer_sets_breeding_cage_attributes(self):
        self.assertTrue(self.breeding_cage.transferred_to_stock)

    # transfer_to_stock method creates mice in stock cage
    def test_transfer_creates_mice(self):
        self.assertEqual(Mouse.objects.filter(sex="M").count(), 6)
        self.assertEqual(Mouse.objects.filter(sex="F").count(), 4)
        self.assertEqual(self.stock_cage.mice.count(), 8)

    # Mice created by transfer_to_stock have correct attributes
    def test_mice_attributes_created_by_transfer(self):
        self.assertEqual(self.new_mouse.strain, self.mother.strain)
        self.assertEqual(self.new_mouse.mother, self.mother)
        self.assertEqual(self.new_mouse.father, self.father)
        self.assertEqual(self.new_mouse.dob, date.today())
