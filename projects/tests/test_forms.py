from django.test import TestCase

from mouse_pilot_postgresql.form_factories import NewProjectFormFactory


class NewProjectFormTestCase(TestCase):
    def setUp(self):
        self.form = NewProjectFormFactory.create()

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())

    def test_empty_project_name(self):
        self.form = NewProjectFormFactory.create(project_name="")
        self.assertFalse(self.form.is_valid())

    def test_none_project_name(self):
        self.form = NewProjectFormFactory.create(project_name=None)
        self.assertFalse(self.form.is_valid())


# Filter form tests

# project_name required
