from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.models import Request


class ProjectModelTestCase(TestCase):

    def setUp(self):
        self.project = ProjectFactory()
        self.project.strains.add(StrainFactory(), StrainFactory())
        self.project.researchers.add(UserFactory(), UserFactory())

    def test_many_to_many_strains(self):
        self.assertEqual(self.project.strains.count(), 2)

    def test_many_to_many_researchers(self):
        self.assertEqual(self.project.researchers.count(), 2)

    def test_project_mice_count(self):
        self.assertEqual(self.project.mice.count(), 0)
        MouseFactory(project=self.project)
        self.assertEqual(self.project.mice.count(), 1)


class ProjectMouseFilterTestCase(TestCase):

    def setUp(self):
        pass

    # Empty filter applied

    # Sex filter applied

    # Earmark filter applied

    # Combination of earmark and sex applied

    # Filter cancelled

    # Filter applied and then cancelled

    # Filter applied and then another filter applied

    # Filter applied and then another filter applied and then cancelled

    # Filter applied and then another filter applied

    # No mice match the applied filter


class ListProjectsViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.project1, self.project2 = ProjectFactory(), ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.project1.mice.add(self.mouse1, self.mouse2)

    def test_get_request_authenticated(self):
        self.client.login(username=self.user.username, password="testpassword")
        response = self.client.get(reverse("projects:list_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["myprojects"].count(), 2)
        self.assertEqual(response.context["myprojects"][0].mice.count(), 2)

    def test_get_request_unauthenticated(self):
        response = self.client.get(reverse("projects:list_projects"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("projects:list_projects")}'
        )


# Create new project


class ShowProjectViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory
        self.request = Request.objects.create(researcher=self.user)

    def test_get_request_authenticated(self):
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_project.html")
        # self.assertContains(response, self.project.project_name)
        # self.assertIn("myproject", response.context)
        # self.assertIn("mymice", response.context)
        # self.assertIn("mice_ids_with_requests", response.context)
        # self.assertIn("project_name", response.context)
        # self.assertIn("filter", response.context)

    def test_get_request_unauthenticated(self):
        self.client.logout()
        url = reverse("projects:show_project", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    # POST MouseSelectionForm
    # def test_show_project_post(self):
    #   response = self.client.post(
    #      reverse("add_request", args=[self.project.project_name])
    # )
    # self.assertEqual(response.status_code, 200)
    # self.assertTemplateUsed(response, "add_request.html")

    # Access non-existent project
    def test_show_non_existent_project(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("projects:show_project", args=["AnyOtherName"]))
