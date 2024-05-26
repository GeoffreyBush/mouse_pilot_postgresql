from django.test import TestCase
from django.urls import reverse

from website.models import Request
from website.tests.factories import UserFactory


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


# Test the confirm behaviour
# Test additional behaviour added in the future to requests, such as earmark addition, moving, or clipping
