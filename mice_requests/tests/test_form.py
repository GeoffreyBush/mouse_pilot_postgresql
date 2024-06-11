from django.test import TestCase
from django.forms import MultipleHiddenInput

from mouse_pilot_postgresql.form_factories import RequestFormFactory
from mouse_pilot_postgresql.model_factories import MouseFactory, UserFactory


class RequestFormTestCase(TestCase):

    def test_valid_data(self):
        self.form = RequestFormFactory.create(user=UserFactory())
        self.assertTrue(self.form.is_valid())

    def test_no_mice_in_request(self):
        self.form = RequestFormFactory.create(mice=[])
        self.assertFalse(self.form.is_valid())

    def test_mice_already_culled_in_cull_request(self):
        self.culled_mouse = MouseFactory(culled=True)
        self.form = RequestFormFactory.create(
            task_type="Cull",
            mice=[self.culled_mouse, MouseFactory(culled=False)],
        )
        self.assertEqual(self.form.errors["mice"], [f"Mouse {self.culled_mouse} has already been culled."])

    def test_mice_already_clipped_in_clip_request(self):
        self.clipped_mouse = MouseFactory(earmark="TL")
        self.form = RequestFormFactory.create(
            task_type="Clip",
            mice=[self.clipped_mouse, MouseFactory(earmark="")],
        )
        self.assertEqual(self.form.errors["mice"], [f"Mouse {self.clipped_mouse} has already been clipped."])

    def test_mice_field_hidden(self):
        self.form = RequestFormFactory.create()
        self.assertIsInstance(self.form.fields["mice"].widget, MultipleHiddenInput)

