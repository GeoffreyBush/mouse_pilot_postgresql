from django.test import TestCase

from mouse_pilot_postgresql.form_factories import NewProjectFormFactory


class NewProjectFormTestCase(TestCase):
    def setUp(self):
        self.form = NewProjectFormFactory.create()

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())

    def test_no_project_name(self):
        self.form = NewProjectFormFactory.create(project_name="")
        self.assertFalse(self.form.is_valid())

    def test_uniqueness_of_project_name(self):
        pass

    def test_name_change_doesnt_create_duplicate(self):
        pass


# Filter form tests

# project_name required
