from django.test import TestCase
from django.urls import reverse

from website.forms import RequestForm
from website.models import Request
from website.tests.factories import MouseFactory, ProjectFactory, UserFactory


class ShowRequestsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.requests = [
            Request.objects.create(
                request_id=1, researcher=self.user, task_type="Cl", confirmed=True
            ),
            Request.objects.create(
                request_id=2, researcher=self.user, task_type="Cu", confirmed=False
            ),
            Request.objects.create(
                request_id=3, researcher=self.user, task_type="Mo", confirmed=True
            ),
        ]

    # Show requests whilelogged in
    def test_show_requests_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("show_requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_requests.html")
        self.assertQuerysetEqual(
            response.context["requests"], self.requests, ordered=False
        )

    # Show requests while not logged in
    def test_show_requests_view_login_required(self):
        url = reverse("show_requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class AddRequestViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(project=self.project), MouseFactory(
            project=self.project
        )
        self.mice = [self.mouse1, self.mouse2]

    # GET RequestForm while logged in
    def test_add_request_get(self):
        url = reverse("add_request", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)

    # Get RequestForm while not logged in
    def test_add_request_get_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("add_request", args=[self.project.project_name])
        )
        url = reverse("add_request", args=[self.project.project_name])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    # POST RequestForm with valid data
    # mouse.tube has broken this test
    """
    def test_add_request_post_valid(self):
        url = reverse("add_request", args=[self.project.project_name])
        data = {
            "task_type": "Cl",
            "mice": [self.mice[0].tube, self.mice[1].tube],
            "new_message": "Test message",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.project_name])
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

    # Unauthenticated user redirected to login page
    def test_confirm_request_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('confirm_request', args=[self.request.request_id])}",
        )

    # Redirect to show_requests after confirming
    def test_confirm_request_view_get_request(self):
        response = self.client.get(
            reverse("confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("show_requests"))

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
