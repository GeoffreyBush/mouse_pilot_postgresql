from django.test import TestCase

from mice_requests.forms import ClipForm, CullForm
from mice_requests.tests.test_model import RequestFactory
from mouse_pilot_postgresql.form_factories import RequestFormFactory
from mouse_pilot_postgresql.model_factories import MouseFactory, UserFactory


class RequestFormTestCase(TestCase):

    def test_valid_data(self):
        form = RequestFormFactory.create(user=UserFactory())
        self.assertTrue(form.is_valid())

    def test_no_mice_in_request(self):
        form = RequestFormFactory.create(mice=[])
        self.assertFalse(form.is_valid())

    def test_mice_already_culled_in_cull_request(self):
        form = RequestFormFactory.create(
            task_type="Cull",
            mice=[MouseFactory(culled=True), MouseFactory(culled=True)],
        )
        self.assertEqual(len(form.errors["mice"]), 2)

    def test_mice_already_clipped_in_clip_request(self):
        form = RequestFormFactory.create(
            task_type="Clip",
            mice=[MouseFactory(earmark="TL"), MouseFactory(earmark="TR")],
        )
        self.assertEqual(len(form.errors["mice"]), 2)

    def test_clip_request_already_exists_for_mouse(self):
        mouse = MouseFactory()
        existing_request = RequestFactory(task_type="Clip")
        existing_request.mice.add(mouse)
        duplicate_form = RequestFormFactory.create(task_type="Clip", mice=[mouse])
        self.assertEqual(
            duplicate_form.errors["mice"][0],
            f"Mouse {mouse} already has a clip request.",
        )

    def test_cull_request_already_exists_for_mouse(self):
        mouse = MouseFactory()
        existing_request = RequestFactory(task_type="Cull")
        existing_request.mice.add(mouse)
        duplicate_form = RequestFormFactory.create(task_type="Cull", mice=[mouse])
        self.assertEqual(
            duplicate_form.errors["mice"][0],
            f"Mouse {mouse} already has a cull request.",
        )


class ClipFormTestCase(TestCase):

    def test_valid_data(self):
        form = ClipForm(data={"earmark": "TL"})
        self.assertTrue(form.is_valid())

    def test_no_earmark(self):
        form = ClipForm(data={"earmark": ""})
        self.assertFalse(form.is_valid())

    def test_invalid_earmark(self):
        form = ClipForm(data={"earmark": "XX"})
        self.assertFalse(form.is_valid())


class CullFormTestCase(TestCase):

    def test_valid_data(self):
        form = CullForm(data={"culled": True})
        self.assertTrue(form.is_valid())

    def test_no_culled(self):
        form = CullForm(data={"culled": False})
        self.assertFalse(form.is_valid())
