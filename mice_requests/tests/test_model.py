from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from mice_requests.models import Request
from mouse_pilot_postgresql.model_factories import MouseFactory, RequestFactory
from system_users.models import CustomUser


class RequestModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mice = [MouseFactory() for _ in range(2)]

    def setUp(self):
        self.request = RequestFactory(mice=self.mice, task_type="Clip")

    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    def test_request_pk(self):
        self.assertEqual(self.request.pk, 1)

    def test_many_to_many_mice(self):
        self.assertQuerySetEqual(self.request.mice.all(), self.mice, ordered=False)

    def test_requested_by_cannot_be_none(self):  # Could change to must be a CustomUser?
        with self.assertRaises(IntegrityError):
            RequestFactory(requested_by=None)

    def test_requested_by_is_user(self):
        self.assertIsInstance(self.request.requested_by, CustomUser)

    def test_request_confirmed(self):
        assert self.request.confirmed is False
        self.request.confirm("TL")
        assert self.request.confirmed

    def test_invalid_task_type(self):
        self.request.task_type = "Invalid"
        with self.assertRaises(ValidationError):
            self.request.confirm()


class RequestConfirmClipTest(TestCase):
    
    def setUp(self):
        self.mice = [MouseFactory() for _ in range(2)]
        self.request = RequestFactory(mice=self.mice, task_type="Clip")

    def test_mice_genotyped_on_confirm(self):
        assert all(not mouse.is_genotyped() for mouse in self.request.mice.all())
        self.request.confirm("TL")
        assert all(mouse.is_genotyped() for mouse in self.request.mice.all())

    def test_confirm_earmark_cannot_be_none(self):
        with self.assertRaises(ValidationError):
            self.request.confirm(None)

    def test_confirm_invalid_earmark(self):
        with self.assertRaises(ValidationError):
            self.request.confirm("Invalid")

    def test_confirm_when_already_confirmed(self):
        self.request.confirm("TL")
        with self.assertRaises(ValidationError):
            self.request.confirm("TL")


class RequestConfirmCullTest(TestCase):

    def setUp(self):
        self.mice = [MouseFactory(culled="False") for _ in range(2)]
        self.request = RequestFactory(mice=self.mice, task_type="Cull")

    def test_mice_culled_on_confirm(self):
        assert all(not mouse.culled for mouse in self.request.mice.all())
        self.request.confirm()
        assert all(mouse.culled for mouse in self.request.mice.all())

    def test_confirm_when_already_confirmed(self):
        self.request.confirm()
        with self.assertRaises(ValidationError):
            self.request.confirm()
