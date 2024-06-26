from datetime import date

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from mice_requests.models import Request
from main.model_factories import (
    MiceRequestFactory,
    MouseFactory,
    UserFactory,
)
from system_users.models import CustomUser


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")


def tearDownModule():
    global test_user
    test_user.delete()


class RequestModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mice = [MouseFactory() for _ in range(2)]

    def setUp(self):
        self.request = MiceRequestFactory(
            mice=self.mice, task_type="Clip", requested_by=test_user
        )

    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    def test_request_pk(self):
        self.assertEqual(self.request.pk, 1)

    def test_many_to_many_mice(self):
        self.assertQuerySetEqual(self.request.mice.all(), self.mice, ordered=False)

    def test_requested_by_cannot_be_none(self):  # Could change to must be a CustomUser?
        with self.assertRaises(IntegrityError):
            MiceRequestFactory(requested_by=None)

    def test_requested_by_value_is_user_instance(self):
        self.assertIsInstance(self.request.requested_by, CustomUser)

    def test_invalid_task_type(self):
        self.request.task_type = "Invalid"
        with self.assertRaises(ValidationError):
            self.request.confirm()

    def test_cannot_confirm_when_already_confirmed(self):
        self.request.confirm(earmark="TL")
        with self.assertRaises(ValidationError):
            self.request.confirm(earmark="TL")

    # Request is not confirmed if any error occurs


class RequestModelConfirmClipTest(TestCase):

    def setUp(self):
        self.mice = [MouseFactory() for _ in range(2)]
        self.request = MiceRequestFactory(
            mice=self.mice, task_type="Clip", requested_by=test_user
        )

    def test_clip_request_confirmed_after_calling_confirm(self):
        self.assertFalse(self.request.confirmed)
        self.request.confirm(earmark="TL")
        self.assertTrue(self.request.confirmed)

    def test_mice_genotyped_on_confirm(self):
        assert all(not mouse.is_genotyped() for mouse in self.request.mice.all())
        self.request.confirm(earmark="TL")
        assert all(mouse.is_genotyped() for mouse in self.request.mice.all())

    def test_confirm_earmark_cannot_be_none(self):
        with self.assertRaises(ValidationError):
            self.request.confirm(earmark=None)

    def test_confirm_invalid_earmark(self):
        with self.assertRaises(ValidationError):
            self.request.confirm(earmark="Invalid")

    def test_unsuccessful_confirm_of_clip_request_if_any_mouse_already_clipped(self):
        self.mice[0].earmark = "TL"
        self.mice[0].save()
        with self.assertRaises(ValidationError):
            self.request.confirm(earmark="TL")
        self.assertFalse(self.request.confirmed)

    # test no mice were recorded as clipped in an unsuccessful confirm


class RequestModelConfirmCullTest(TestCase):

    def setUp(self):
        self.mice = [MouseFactory(culled_date=None) for _ in range(2)]
        self.request = MiceRequestFactory(
            mice=self.mice, task_type="Cull", requested_by=test_user
        )

    def test_cull_request_confirmed_after_calling_confirm(self):
        self.assertFalse(self.request.confirmed)
        self.request.confirm(date=date.today())
        self.assertTrue(self.request.confirmed)

    def test_mice_culled_on_confirm(self):
        assert all(not mouse.is_culled() for mouse in self.request.mice.all())
        self.request.confirm(date=date.today())
        assert all(mouse.is_culled() for mouse in self.request.mice.all())

    def test_unsuccessful_confirm_of_cull_request_if_any_mouse_already_culled(self):
        self.mice[0].cull(date.today())
        with self.assertRaises(ValidationError):
            self.request.confirm(date=date.today())
        self.assertFalse(self.request.confirmed)

    # test no mice were recorded as culled in an unsuccessful confirm

    def test_date_required_to_confirm(self):
        with self.assertRaises(ValidationError):
            self.request.confirm()


# Request is only confirmed if all mice are successfully clipped, culled, etc.
