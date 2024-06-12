from django.forms import MultipleHiddenInput
from django.test import TestCase

from mouse_pilot_postgresql.form_factories import RequestFormFactory
from mouse_pilot_postgresql.model_factories import MouseFactory, UserFactory

from mice_requests.tests.test_model import RequestFactory

class RequestFormTestCase(TestCase):

    def test_valid_data(self):
        self.form = RequestFormFactory.create(user=UserFactory())
        self.assertTrue(self.form.is_valid())

    def test_no_mice_in_request(self):
        self.form = RequestFormFactory.create(mice=[])
        self.assertFalse(self.form.is_valid())

    def test_mice_already_culled_in_cull_request(self):
        self.form = RequestFormFactory.create(
            task_type="Cull",
            mice=[MouseFactory(culled=True), MouseFactory(culled=True)],
        )
        self.assertEqual(len(self.form.errors["mice"]), 2)

    def test_mice_already_clipped_in_clip_request(self):
        self.form = RequestFormFactory.create(
            task_type="Clip",
            mice=[MouseFactory(earmark="TL"), MouseFactory(earmark="TR")],
        )
        self.assertEqual(len(self.form.errors["mice"]), 2)

    def test_mice_field_hidden(self):
        self.form = RequestFormFactory.create()
        self.assertIsInstance(self.form.fields["mice"].widget, MultipleHiddenInput)

    def test_clip_request_already_exists_for_mouse(self):
        self.mouse = MouseFactory()
        self.existing_request = RequestFactory(task_type="Clip")
        self.existing_request.mice.add(self.mouse)
        self.duplicate_form = RequestFormFactory.create(task_type="Clip", mice=[self.mouse])
        self.assertEqual(self.duplicate_form.errors["mice"][0], f"Mouse {self.mouse} already has a clip request.")

    def test_cull_request_already_exists_for_mouse(self):
        self.mouse = MouseFactory()
        self.existing_request = RequestFactory(task_type="Cull")
        self.existing_request.mice.add(self.mouse)
        self.duplicate_form = RequestFormFactory.create(task_type="Cull", mice=[self.mouse])
        self.assertEqual(self.duplicate_form.errors["mice"][0], f"Mouse {self.mouse} already has a cull request.")