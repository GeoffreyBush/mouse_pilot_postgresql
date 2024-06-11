from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from mice_requests.forms import RequestForm
from mice_requests.models import Request
from mouse_pilot_postgresql.form_factories import RequestFormFactory
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    RequestFactory,
    UserFactory,
)


class RequestModelTestCase(TestCase):
    def setUp(self):
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.request = RequestFactory()
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

    def test_request_is_confirmed(self):
        assert self.request.confirmed is False
        self.request.confirm_clip("TL")
        assert self.request.confirmed

    def test_mice_genotyped_on_confirm_clip(self):
        assert all(not mouse.is_genotyped() for mouse in self.request.mice.all())
        self.request.confirm_clip("TL")
        assert all(mouse.is_genotyped() for mouse in self.request.mice.all())

    def test_confirm_clip_request_must_pass_earmark(self):
        with self.assertRaises(ValidationError):
            self.request.confirm_clip(None)

    def test_confirm_clip_when_already_confirmed(self):
        self.request.confirm_clip("TL")
        with self.assertRaises(ValidationError):
            self.request.confirm_clip("TL")

    def test_confirm_clip_when_mice_already_clipped(self):
        self.mouse1.earmark = "TL"
        self.mouse1.save()
        self.mouse1.refresh_from_db()
        with self.assertRaises(ValidationError):
            self.request.confirm_clip("TL")

    def test_confirm_cull_when_mice_already_culled(self):
        self.mouse1.cull()
        self.mouse1.save()
        self.mouse1.refresh_from_db()
        with self.assertRaises(ValidationError):
            self.request.confirm_cull()

    # Test request messaging system


class RequestFormTestCase(TestCase):

    # Valid form
    def test_valid_data(self):
        self.user = UserFactory()
        self.form = RequestFormFactory.create(user=self.user)

    # There must be at least one mouse present in a request

    # Cannot try to clip or cull mice that are already genotyped or culled


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
        cls.request = Request.objects.create(
            requested_by=cls.user, task_type="Cl", confirmed=False
        )
        cls.request.mice.add(cls.mouse)
        cls.response = cls.client.get(
            reverse("mice_requests:confirm_request", args=[cls.request.request_id])
        )

    # What additional tests can be added here?

    def test_code_302(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirects_to_show_requests(self):
        self.assertRedirects(self.response, reverse("mice_requests:show_requests"))

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

    # Confirm clip view changes earmark of mice in request

# Test additional behaviour added in the future to requests, such as earmark addition, moving, or clipping
