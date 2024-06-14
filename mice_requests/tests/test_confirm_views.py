from django.test import Client, TestCase
from django.urls import reverse

from mice_requests.forms import ClipForm, CullForm
from mouse_pilot_postgresql.model_factories import (
    MiceRequestFactory,
    MouseFactory,
    UserFactory,
)


class ConfirmRequestViewGetTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = Client()
        self.user = UserFactory()
        self.request = MiceRequestFactory(task_type="Clip")

    def test_code_200(self):
        self.client.force_login(self.user)
        self.response = self.client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_used(self):
        self.client.force_login(self.user)
        self.response = self.client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertTemplateUsed(self.response, "confirm_request.html")

    def test_correct_clip_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertIsInstance(response.context["form"], ClipForm)

    def test_correct_cull_form_in_context(self):
        self.client.force_login(self.user)
        request = MiceRequestFactory(task_type="Cull")
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[request.request_id])
        )
        self.assertIsInstance(response.context["form"], CullForm)


class ConfirmRequestViewPostTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = Client()
        self.user = UserFactory()
        self.mouse = MouseFactory(earmark="", culled=False)
        self.request = MiceRequestFactory(mice=[self.mouse], task_type="Clip")

    def test_code_302(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.assertEqual(response.status_code, 302)

    def test_correct_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.assertEqual(response.url, reverse("mice_requests:show_requests"))

    def test_mouse_genotyped(self):
        self.client.force_login(self.user)
        self.assertFalse(self.mouse.is_genotyped())
        self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())

    def test_mouse_culled(self):
        self.client.force_login(self.user)
        self.request.task_type = "Cull"
        self.request.save()
        self.assertFalse(self.mouse.culled)
        self.client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"culled": "True"},
        )
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.culled)
