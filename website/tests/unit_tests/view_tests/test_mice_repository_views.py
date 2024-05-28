from django.test import TestCase
from django.urls import reverse

from website.tests.model_factories import MouseFactory, UserFactory


class MiceRepositoryViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()

    # GET mice_repository while logged in
    def test_mice_repository_view_get_request(self):
        response = self.client.get(reverse("mice_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "repository/mice_repository.html")
        self.assertIn("mymice", response.context)
        self.assertIn(self.mouse, response.context["mymice"])

    # test for add mouse to repository
    def test_add_mouse_to_repository(self):
        response = self.client.get(reverse("add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "repository/add_mouse_to_repository.html")
        # self.assertIsInstance(response.context["form"], RepositoryMiceForm)

    # POST RequestForm with valid data
    # def test_add_mouse_to_repository_post_valid(self):
    #   data = {


# Test for adding a mouse to the repository
