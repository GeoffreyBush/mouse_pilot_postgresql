from django.forms import MultipleHiddenInput
from django.test import TestCase

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
        self.culled_mouse1 = MouseFactory(culled=True)
        self.culled_mouse2 = MouseFactory(culled=True)
        self.form = RequestFormFactory.create(
            task_type="Cull",
            mice=[self.culled_mouse1, self.culled_mouse2],
        )
        self.assertEqual(
            self.form.errors["mice"],
            [
                f"Mouse {self.culled_mouse1} has already been culled.",
                f"Mouse {self.culled_mouse2} has already been culled.",
            ],
        )

    def test_mice_already_clipped_in_clip_request(self):
        self.clipped_mouse1 = MouseFactory(earmark="TL")
        self.clipped_mouse2 = MouseFactory(earmark="TR")
        self.form = RequestFormFactory.create(
            task_type="Clip",
            mice=[self.clipped_mouse1, self.clipped_mouse2],
        )
        self.assertEqual(
            self.form.errors["mice"],
            [
                f"Mouse {self.clipped_mouse1} has already been clipped.",
                f"Mouse {self.clipped_mouse2} has already been clipped.",
            ],
        )

    def test_mice_field_hidden(self):
        self.form = RequestFormFactory.create()
        self.assertIsInstance(self.form.fields["mice"].widget, MultipleHiddenInput)
