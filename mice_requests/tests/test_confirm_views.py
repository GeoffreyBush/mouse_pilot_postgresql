from django.test import Client, TestCase
from django.urls import reverse

from mice_requests.forms import ClipForm, CullForm
from mouse_pilot_postgresql.model_factories import (
    MiceRequestFactory,
    MouseFactory,
    UserFactory,
)


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class ConfirmRequestViewGetTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.request = MiceRequestFactory(task_type="Clip")

    def test_code_200(self):
        self.response = test_client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_used(self):
        self.response = test_client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertTemplateUsed(self.response, "confirm_request.html")

    def test_correct_clip_form_in_context(self):
        response = test_client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertIsInstance(response.context["form"], ClipForm)

    def test_correct_cull_form_in_context(self):
        request = MiceRequestFactory(task_type="Cull")
        response = test_client.get(
            reverse("mice_requests:confirm_request", args=[request.request_id])
        )
        self.assertIsInstance(response.context["form"], CullForm)


class ConfirmRequestViewPostTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.mouse = MouseFactory(earmark="", culled=False)
        self.request = MiceRequestFactory(mice=[self.mouse], task_type="Clip")

    def test_code_302(self):
        response = test_client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.assertEqual(response.status_code, 302)

    def test_correct_redirect(self):
        response = test_client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.assertEqual(response.url, reverse("mice_requests:show_requests"))

    def test_mouse_genotyped(self):
        self.assertFalse(self.mouse.is_genotyped())
        test_client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"earmark": "TL"},
        )
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())

    def test_mouse_culled(self):
        self.request.task_type = "Cull"
        self.request.save()
        self.assertFalse(self.mouse.culled)
        test_client.post(
            reverse("mice_requests:confirm_request", args=[self.request.request_id]),
            data={"culled": "True"},
        )
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.culled)
