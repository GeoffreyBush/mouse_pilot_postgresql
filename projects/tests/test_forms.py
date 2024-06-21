from django.test import TestCase

from mouse_pilot_postgresql.form_factories import NewProjectFormFactory
from mouse_pilot_postgresql.model_factories import MouseFactory, StrainFactory
from projects.forms import AddMouseToProjectForm


class NewProjectFormTest(TestCase):
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


class AddMouseToProjectFormTest(TestCase):
    def setUp(self):
        self.strain1, self.strain2 = StrainFactory(), StrainFactory()
        self.strains = [self.strain1.pk, self.strain2.pk]
        self.data = {
            "mice": [
                MouseFactory(strain=self.strain1).pk,
                MouseFactory(strain=self.strain2).pk,
                MouseFactory(strain=self.strain2).pk,
            ]
        }
        self.form = AddMouseToProjectForm(strains=self.strains, data=self.data)

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())

    def test_strain_not_passed_to_form_raises_error(self):
        with self.assertRaises(ValueError):
            AddMouseToProjectForm(data=self.data)

    def test_strain_and_mice_do_not_match(self):
        self.form = AddMouseToProjectForm(
            strains=self.strains, data={"mice": [MouseFactory().pk]}
        )
        self.assertFalse(self.form.is_valid())

    # mouse cannot be in a project already