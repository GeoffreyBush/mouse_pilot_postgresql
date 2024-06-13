from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from projects.models import Project

class ProjectModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory(project_name="testproject")
        cls.project.strains.add(StrainFactory(), StrainFactory())
        cls.project.researchers.add(UserFactory(), UserFactory())

    def test_project_created(self):
        self.assertIsInstance(self.project, Project)

    def test_project_pk_is_int(self):
        self.assertIsInstance(self.project.pk, int)

    def test_project_name(self):
        self.assertEqual(self.project.project_name, "testproject")

    def test_many_to_many_strains(self):
        self.assertEqual(self.project.strains.count(), 2)

    def test_many_to_many_researchers(self):
        self.assertEqual(self.project.researchers.count(), 2)

    def test_project_mice_count(self):
        self.assertEqual(self.project.mice.count(), 0)
        MouseFactory(project=self.project)
        self.assertEqual(self.project.mice.count(), 1)

    def test_project_name_doesnt_exist(self):
        with self.assertRaises(IntegrityError):
            ProjectFactory(project_name=None)

    def test_project_name_too_short(self):
        self.short_name = ProjectFactory(project_name="ab")
        with self.assertRaises(ValidationError):
            self.short_name.full_clean()

    def test_uniqueness_of_project_name(self):
        with self.assertRaises(IntegrityError):
            ProjectFactory(project_name="testproject")

    # Is it possible to require a researcher to be assigned to a project?
