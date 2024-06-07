from django.test import TestCase
from django.urls import reverse

from mice_requests.forms import RequestForm
from mice_requests.models import Request
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)


class RequestModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.strain = StrainFactory()
        self.mouse1, self.mouse2 = MouseFactory(strain=self.strain), MouseFactory(
            strain=self.strain
        )

        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse1, self.mouse2)

    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    def test_request_pk(self):
        self.assertEqual(self.request.pk, 1)

    def test_many_to_many_mice(self):
        self.assertQuerySetEqual(
            self.request.mice.all(), [self.mouse1, self.mouse2], ordered=False
        )

    """
    def test_request_confirm(self):
        self.assertFalse(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertFalse(mouse.is_genotyped())

        self.request.confirm()

        self.request.refresh_from_db()
        for mouse in self.request.mice.all():
            mouse.refresh_from_db()

        self.assertTrue(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertTrue(mouse.is_genotyped())
    """


class RequestFormTestCase(TestCase):
    def setUp(self):
        pass

    # There must be at least one mouse present in a request


class ShowRequestsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.requests = [
            Request.objects.create(
                request_id=1, researcher=self.user, task_type="Cl", confirmed=True
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
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.mice = [self.mouse1, self.mouse2]

    # Need to test that correct number of selected mice are carried over to add_request view
    # This test was copied from projects.tests. It checks the MouseSelectionForm carried over to the add_request view
    def test_post_mice_add_request(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("mice_requests:add_request", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")

    # GET RequestForm while logged in
    def test_add_request_get(self):
        url = reverse("mice_requests:add_request", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)

    """
    def test_add_request_post_valid(self):
        url = reverse("mice_requests:add_request", args=[self.project.project_name])
        data = {
            "task_type": "Cl",
            "mice": [self.mice[0]._tube, self.mice[1]._tube],
            "new_message": "Test message",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertTrue(
            Request.objects.filter(task_type="Cl", mice__in=self.mice).exists()
        )
        self.assertEqual(Request.objects.count(), 1)
        request = Request.objects.first()
        self.assertEqual(request.task_type, "Cl")
        self.assertEqual(request.new_message, "Test message")
        self.assertQuerySetEqual(
            request.mice.all(), [self.mouse1, self.mouse2], ordered=False
        )
    """

    # Can't trust this test because of the mouse.tube issue.
    # Must fix POST with valid data test first
    """
    # POST RequestForm with invalid data
    def test_add_request_post_invalid(self):
        url = reverse("add_request", args=[self.project.project_name])
        data = {"task_type": "Invalid", "mice": []}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)
        self.assertFalse(Request.objects.exists())

    # Try to add request to a non-existent project
    def test_add_request_with_non_existent_project(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("add_request", args=["AnyOtherName"]))
    """


class ConfirmRequestViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()
        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
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
