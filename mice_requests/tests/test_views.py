from django.test import Client, TestCase
from django.urls import reverse

from mice_requests.forms import ClipForm, CullForm, RequestForm
from mice_requests.models import Request
from mouse_pilot_postgresql.form_factories import RequestFormFactory
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    RequestFactory,
    UserFactory,
)


class ShowRequestsViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.client.force_login(UserFactory())
        cls.requests = [RequestFactory() for _ in range(3)]
        cls.response = cls.client.get(reverse("mice_requests:show_requests"))

    def test_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "show_requests.html")

    def test_requests_in_response(self):
        self.assertQuerysetEqual(
            self.response.context["requests"], self.requests, ordered=False
        )


class AddRequestViewGetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.mice = [MouseFactory(), MouseFactory()]
        cls.client.force_login(UserFactory())
        cls.client.session["selected_mice"] = [mouse.pk for mouse in cls.mice]
        cls.client.session.save()
        cls.url = reverse(
            "mice_requests:add_request", args=[ProjectFactory().project_name]
        )
        cls.response = cls.client.get(cls.url)

    def test_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "add_request.html")

    def test_form_in_context(self):
        self.assertIsInstance(self.response.context["form"], RequestForm)

    def test_mice_in_form(self):
        self.assertQuerysetEqual(
            self.response.context["form"].fields["mice"].queryset,
            self.mice,
            ordered=False,
        )


class AddRequestViewPostTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.project = ProjectFactory()
        cls.mice = [MouseFactory(), MouseFactory()]
        cls.client.force_login(UserFactory())
        cls.url = reverse("mice_requests:add_request", args=[cls.project.project_name])
        cls.response = cls.client.post(
            cls.url, RequestFormFactory.valid_data(mice=cls.mice)
        )

    def test_code_302(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirects_to_project(self):
        self.assertRedirects(
            self.response,
            reverse("projects:show_project", args=[self.project.project_name]),
        )

    def test_request_created(self):
        self.assertEqual(Request.objects.count(), 1)

    def test_request_mice(self):
        self.assertQuerysetEqual(
            Request.objects.first().mice.all(), self.mice, ordered=False
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


# Test additional behaviour added in the future to requests, such as earmark addition, moving, or clipping
