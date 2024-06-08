from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)
from mouse_pilot_postgresql.form_factories import NewProjectFormFactory
from projects.filters import ProjectFilter
from projects.forms import NewProjectForm
from projects.models import Project
from system_users.models import CustomUser


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
        self.assertIsInstance(response.context["form"], NewProjectForm)

    def test_post_request_valid_data(self):
        self.client.force_login(self.user)
        data = NewProjectFormFactory.valid_data()
        self.assertEqual(Project.objects.all().count(), 0)
        response = self.client.post(
            reverse("projects:add_new_project"), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("projects:list_projects"))
        self.assertEqual(Project.objects.all().count(), 1)



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
        self.assertIsInstance(response.context["project_mice"], ProjectFilter)
        # self.assertIsInstance(response.context["form"], MouseSelectionForm)

    def test_show_non_existent_project(self):
        self.client.force_login(self.user)
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("projects:show_project", args=["AnyOtherName"]))
