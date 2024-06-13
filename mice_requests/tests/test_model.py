from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from mice_requests.models import Request
from mouse_pilot_postgresql.model_factories import MouseFactory, RequestFactory
from system_users.models import CustomUser


class RequestModelTest(TestCase):
    def setUp(self):
        self.mice = [MouseFactory() for _ in range(2)]
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
        self.request.confirm_clip("TL")
        assert self.request.confirmed


class RequestConfirmClipTest(TestCase):
    def setUp(self):
        self.mice = [MouseFactory() for _ in range(2)]
        self.request = RequestFactory(mice=self.mice, task_type="Clip")
    
    def test_mice_genotyped_on_confirm_clip(self):
        assert all(not mouse.is_genotyped() for mouse in self.request.mice.all())
        self.request.confirm_clip("TL")
        assert all(mouse.is_genotyped() for mouse in self.request.mice.all())

    def test_confirm_clip_can_only_be_called_on_clip_request(self):
        self.request.task_type = "Cull"
        with self.assertRaises(ValidationError):
            self.request.confirm_clip("TL")

    def test_confirm_clip_earmark_cannot_be_none(self):
        with self.assertRaises(ValidationError):
            self.request.confirm_clip(None)

    def test_confirm_clip_invalid_earmark(self):
        with self.assertRaises(ValidationError):
            self.request.confirm_clip("Invalid")

    def test_confirm_clip_when_already_confirmed(self):
        self.request.confirm_clip("TL")
        with self.assertRaises(ValidationError):
            self.request.confirm_clip("TL")
    
    # The confirm_cull and confirm_clip methods are very similar, could be refactored

class RequestConfirmCullTest(TestCase):

    def test_confirm_cull_can_only_be_called_on_cull_request(self):
        request = RequestFactory(task_type="Clip")
        with self.assertRaises(ValidationError):
            request.confirm_cull()

    # More cull tests
