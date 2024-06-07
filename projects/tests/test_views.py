from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)


class ListProjectsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.client = Client()
        cls.project1, cls.project2 = ProjectFactory(), ProjectFactory()
        cls.mouse1 = MouseFactory()
        cls.project1.mice.add(cls.mouse1)

    def test_get_request_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("projects:list_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["myprojects"].count(), 2)
        self.assertEqual(response.context["myprojects"][0].mice.count(), 1)

    def test_get_request_unauthenticated(self):
        response = self.client.get(reverse("projects:list_projects"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("projects:list_projects")}'
        )


class AddNewProjectViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(username="testuser")
        cls.client = Client()

    def test_get_request_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("projects:add_new_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_new_project.html")
        self.assertIn("form", response.context)

    def test_get_request_unauthenticated(self):
        self.client.logout()
        url = reverse("breeding_cage:add_breeding_cage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class ShowProjectViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory(username="testuser")
        cls.project = ProjectFactory()

    def test_get_request_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_project.html")
        self.assertIn("project", response.context)
        self.assertIn("project_mice", response.context)

    def test_get_request_unauthenticated(self):
        url = reverse("projects:show_project", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_show_non_existent_project(self):
        self.client.force_login(self.user)
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("projects:show_project", args=["AnyOtherName"]))
