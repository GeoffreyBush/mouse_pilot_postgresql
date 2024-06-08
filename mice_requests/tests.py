from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError

from mice_requests.forms import RequestForm
from mice_requests.models import Request
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
    RequestFactory,
)
from mouse_pilot_postgresql.form_factories import RequestFormFactory


class RequestModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse1, cls.mouse2 = MouseFactory(), MouseFactory()
        cls.request = RequestFactory()
        cls.request.mice.add(cls.mouse1, cls.mouse2)

    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    def test_request_pk(self):
        self.assertEqual(self.request.pk, 1)

    def test_many_to_many_mice(self):
        self.assertQuerySetEqual(
            self.request.mice.all(), [self.mouse1, self.mouse2], ordered=False
        )

    def test_requested_by_is_none(self):
        with self.assertRaises(IntegrityError):
            RequestFactory(requested_by=None)

    # Test request message system
    
    def test_confirm_clip_request(self):
        assert all(not mouse.is_genotyped() for mouse in self.request.mice.all())
        self.request.confirm_clip("TL")
        self.request.refresh_from_db()
        [mouse.refresh_from_db() for mouse in self.request.mice.all()]
        assert self.request.confirmed
        assert all(mouse.is_genotyped() for mouse in self.request.mice.all())
    


class RequestFormTestCase(TestCase):

    # Valid form
    def test_valid_data(self):
        self.user = UserFactory()
        self.form = RequestFormFactory.create(user=self.user)

    # There must be at least one mouse present in a request



class ShowRequestsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.requests = [
            Request.objects.create(
                request_id=1, requested_by=self.user, task_type="Cl", confirmed=True
            )
        ]

    # Show requests whilelogged in
    def test_show_requests_view(self):
        response = self.client.get(reverse("mice_requests:show_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_requests.html")
        self.assertQuerysetEqual(
            response.context["requests"], self.requests, ordered=False
        )


class AddRequestViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(username="testuser")
        cls.project = ProjectFactory()
        cls.mouse1, cls.mouse2 = MouseFactory(), MouseFactory()
        cls.mice = [cls.mouse1, cls.mouse2]

    # Need to test that correct number of selected mice are carried over to add_request view
    # This test was copied from projects.tests. It checks the MouseSelectionForm carried over to the add_request view
    def test_get_request_authenticated(self):
        self.client.force_login(self.user)
        url = reverse("mice_requests:add_request", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)

    def test_add_request_post_valid(self):
        self.client.force_login(self.user)
        url = reverse("mice_requests:add_request", args=[self.project.project_name])
        data = RequestFormFactory.valid_data(mice=self.mice)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertEqual(Request.objects.count(), 1)


class ConfirmRequestViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()
        self.request = Request.objects.create(
            requested_by=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse)

    # Redirect to show_requests after confirming
    def test_confirm_request_view_get_request(self):
        response = self.client.get(
            reverse("mice_requests:confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("mice_requests:show_requests"))

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


# Test additional behaviour added in the future to requests, such as earmark addition, moving, or clipping
