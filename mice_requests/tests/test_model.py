from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from mice_requests.models import Request
from mouse_pilot_postgresql.model_factories import MouseFactory, RequestFactory


class RequestModelTestCase(TestCase):
    def setUp(self):
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.request = RequestFactory(task_type="Clip")
        self.request.mice.add(self.mouse1, self.mouse2)

    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    def test_request_pk(self):
        self.assertEqual(self.request.pk, 1)

    def test_many_to_many_mice(self):
        self.assertQuerySetEqual(
            self.request.mice.all(), [self.mouse1, self.mouse2], ordered=False
        )

    def test_requested_by_cannot_be_none(self):
        with self.assertRaises(IntegrityError):
            RequestFactory(requested_by=None)

    def test_request_confirmed(self):
        assert self.request.confirmed is False
        self.request.confirm_clip("TL")
        assert self.request.confirmed

    def test_mice_genotyped_on_confirm_clip(self):
        assert all(not mouse.is_genotyped() for mouse in self.request.mice.all())
        self.request.confirm_clip("TL")
        assert all(mouse.is_genotyped() for mouse in self.request.mice.all())

    def test_confirm_clip_can_only_be_called_on_clip_request(self):
        self.request.task_type = "Cull"
        with self.assertRaises(ValidationError):
            self.request.confirm_clip("TL")

    def test_confirm_cull_can_only_be_called_on_cull_request(self):
        self.request.task_type = "Clip"
        with self.assertRaises(ValidationError):
            self.request.confirm_cull()

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

    # Test request messaging system
