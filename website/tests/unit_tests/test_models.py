from django.db import IntegrityError
from django.test import TestCase

from test_factories.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.models import Request, Strain

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
class StrainModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")

    # Duplicate strain name
    def test_strain_duplicates(self):
        with self.assertRaises(IntegrityError):
            Strain.objects.create(strain_name="teststrain")

    # Increment mice count of a strain by making a mouse
    def test_strain_mice_count(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.strain.mice_count, 1)

    # Decrement mice count from 1 to 0
    def test_strain_mice_count_decrement_from_one(self):
        self.strain.mice_count = 1
        self.assertEqual(self.strain.mice_count, 1)
        self.strain.decrement_mice_count()
        self.assertEqual(self.strain.mice_count, 0)

    # Decrement mice count of a a strain should not go below 0
    def test_strain_mice_count_decrement_from_zero(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.strain.decrement_mice_count()
        self.assertEqual(self.strain.mice_count, 0)

    # Deleting a mouse should decrement the mice count

    # Changing the strain of a mouse should increment the new strain's mice count

    # Changing the strain of a mouse should decrement the old strain's mice count


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
