from django.test import Client, TestCase
from django.urls import reverse

from mice_requests.forms import ClipForm, CullForm
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    RequestFactory,
    UserFactory,
)


class ConfirmRequestViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory()
        cls.client.force_login(cls.user)
        cls.mouse = MouseFactory()
        cls.request = RequestFactory(task_type="Clip")
        cls.request.mice.add(cls.mouse)
        cls.response = cls.client.get(
            reverse("mice_requests:confirm_request", args=[cls.request.request_id])
        )

    def test_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.response, "confirm_request.html")

    def test_correct_clip_form_in_context(self):
        self.client.force_login(self.user)
        request = RequestFactory(task_type="Clip")
        request.mice.add(MouseFactory())
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[request.request_id])
        )
        self.assertIsInstance(response.context["form"], ClipForm)

    def test_correct_cull_form_in_context(self):
        self.client.force_login(self.user)
        request = RequestFactory(task_type="Cull")
        request.mice.add(MouseFactory())
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[request.request_id])
        )
        self.assertIsInstance(response.context["form"], CullForm)

    # Need to get the clip request to ask for an earmark input for this test to work now
    # Confirm request changes mice.genotyped to True
    """
    def test_confirm_request_view_updates_request_status(self):
        self.client.get(reverse("confirm_request", args=[self.request.request_id]))
        self.request.refresh_from_db()
        self.assertTrue(self.request.confirmed)
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())
    """

    # ConfirmRequestView gives the right form to the template

    # Confirm clip view changes earmark of mice in request
