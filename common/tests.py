from django.test import TestCase

from main.form_factories import MouseSelectionFormFactory
from common.forms import MouseSelectionForm
from main.model_factories import MouseFactory, ProjectFactory


class MouseSelectionFormTest(TestCase):
    def setUp(self):
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.project = ProjectFactory()
        self.project.mice.add(self.mouse1)
        self.form = MouseSelectionFormFactory.build(
            project=self.project, mice=[self.mouse1]
        )

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_correct_queryset_without_project(self):
        self.form = MouseSelectionFormFactory.build(
            project=None, mice=[self.mouse1, self.mouse2]
        )
        self.assertEqual(self.form.fields["mice"].queryset.count(), 2)

    def test_correct_queryset_with_project(self):
        self.assertEqual(self.form.fields["mice"].queryset.count(), 1)

    def test_save_is_disabled(self):
        self.assertIsNone(self.form.save())

    def test_clean_mice_no_selection(self):
        form_data = {}
        form = MouseSelectionForm(form_data, project=self.project)
        self.assertIn(
            "At least one mouse must be selected for a request", form.non_field_errors()
        )
