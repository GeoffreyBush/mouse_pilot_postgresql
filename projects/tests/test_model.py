from django.db.utils import IntegrityError
from django.test import TestCase

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)


class ProjectModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory(project_name="testproject")
        cls.project.strains.add(StrainFactory(), StrainFactory())
        cls.project.researchers.add(UserFactory(), UserFactory())

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

    def test_uniqueness_of_project_name(self):
        with self.assertRaises(IntegrityError):
            ProjectFactory(project_name="testproject")
