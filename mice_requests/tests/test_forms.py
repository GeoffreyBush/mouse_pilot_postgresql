from datetime import date

from django.test import TestCase

from main.form_factories import MiceRequestFormFactory
from main.model_factories import MiceRequestFactory, MouseFactory, UserFactory
from mice_requests.forms import ClipForm, CullForm


def setUpModule():
    global test_user
    test_user = UserFactory(username="testuser")


def tearDownModule():
    global test_user
    test_user.delete()


class RequestFormTest(TestCase):

    def test_valid_data(self):
        form = MiceRequestFormFactory.create()
        self.assertTrue(form.is_valid())

    def test_invalid_request_type(self):
        form = MiceRequestFormFactory.create(task_type="Invalid")
        self.assertFalse(form.is_valid())

    def test_no_mice_in_request(self):
        form = MiceRequestFormFactory.create(mice=[])
        self.assertFalse(form.is_valid())

    def test_mice_already_culled_in_cull_request(self):
        form = MiceRequestFormFactory.create(
            task_type="Cull",
            mice=[MouseFactory(culled_date=date.today()) for _ in range(2)],
        )
        self.assertEqual(len(form.errors["mice"]), 2)

    def test_mice_already_clipped_in_clip_request(self):
        form = MiceRequestFormFactory.create(
            task_type="Clip",
            mice=[MouseFactory(earmark="TL"), MouseFactory(earmark="TR")],
        )
        self.assertEqual(len(form.errors["mice"]), 2)

    def test_clip_request_already_exists_for_mouse(self):
        mouse = MouseFactory()
        MiceRequestFactory(mice=[mouse], task_type="Clip", requested_by=test_user)
        form = MiceRequestFormFactory.create(task_type="Clip", mice=[mouse])
        self.assertEqual(
            form.errors["mice"][0],
            f"Mouse {mouse} already has a clip request.",
        )

    def test_cull_request_already_exists_for_mouse(self):
        mouse = MouseFactory()
        MiceRequestFactory(mice=[mouse], task_type="Cull", requested_by=test_user)
        form = MiceRequestFormFactory.create(task_type="Cull", mice=[mouse])
        self.assertEqual(
            form.errors["mice"][0],
            f"Mouse {mouse} already has a cull request.",
        )

    # Cull is possibly a bad example to have here - if you were going to kill a mouse, why would you want it clipped?
    # Should ask clients which task_types possible conflict in similar ways.
    def test_different_task_types_for_same_mouse_is_allowed(self):
        mouse = MouseFactory()
        MiceRequestFactory(mice=[mouse], task_type="Clip", requested_by=test_user)
        form = MiceRequestFormFactory.create(task_type="Cull", mice=[mouse])
        self.assertTrue(form.is_valid())


class ClipFormTest(TestCase):

    def test_valid_data(self):
        form = ClipForm(data={"earmark": "TL"})
        self.assertTrue(form.is_valid())

    def test_no_earmark(self):
        form = ClipForm(data={"earmark": ""})
        self.assertFalse(form.is_valid())

    def test_invalid_earmark(self):
        form = ClipForm(data={"earmark": "XX"})
        self.assertFalse(form.is_valid())


class CullFormTest(TestCase):

    def test_valid_data(self):
        form = CullForm(data={"culled": True, "culled_date": date.today()})
        self.assertTrue(form.is_valid())

    def test_culled_is_none(self):
        form = CullForm(data={"culled": False, "culled_date": date.today()})
        self.assertFalse(form.is_valid())

    def test_no_culled_date(self):
        form = CullForm(data={"culled": True, "culled_date": ""})
        self.assertFalse(form.is_valid())
