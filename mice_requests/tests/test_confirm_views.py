from django.test import TestCase
from django.urls import reverse

from mice_requests.forms import ClipForm, CullForm
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    RequestFactory,
    UserFactory,
)


class ConfirmRequestViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.request = RequestFactory(task_type="Clip")

    def test_code_200(self):
        self.response = self.client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_used(self):
        self.response = self.client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertTemplateUsed(self.response, "confirm_request.html")

    def test_correct_clip_form_in_context(self):
        request = RequestFactory(task_type="Clip")
        request.mice.add(MouseFactory())
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[request.request_id])
        )
        self.assertIsInstance(response.context["form"], ClipForm)

    def test_correct_cull_form_in_context(self):
        request = RequestFactory(task_type="Cull")
        request.mice.add(MouseFactory())
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[request.request_id])
        )
        self.assertIsInstance(response.context["form"], CullForm)

    # Confirm request changes mice.genotyped to True


class ConfirmRequestPostTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory(earmark="", culled=False)
        self.request = RequestFactory(mice=[self.mouse], task_type="Clip")

    def test_code_302(self):
        response = self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.assertEqual(response.status_code, 302)

    def test_correct_redirect(self):
        response = self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.assertEqual(response.url, reverse("mice_requests:show_requests"))

    def test_mouse_genotyped(self):
        self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())

    def test_mouse_culled(self):
        self.request.task_type = "Cull"
        self.request.save()
        self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"culled": "True"},
        )
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.culled)
