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

    @classmethod
    # Initial Project
    def setUp(self):
        self.project = ProjectFactory()
        self.project.strains.add(StrainFactory(), StrainFactory())
        self.project.researchers.add(UserFactory(), UserFactory())

    # Strains many-to-many
    def test_project_strains(self):
        self.assertEqual(self.project.strains.count(), 2)

    # Researchers many-to-many
    def test_project_researchers(self):
        self.assertEqual(self.project.researchers.count(), 2)

    # Mouse count
    """ Replace this test to use the future class method, Project.mice_count() instead """

    def test_project_mice_count(self):
        self.assertEqual(self.project.mice.count(), 0)
        MouseFactory(project=self.project)
        self.assertEqual(self.project.mice.count(), 1)


class ListProjectsTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.project1, self.project2 = ProjectFactory(), ProjectFactory()

    # Access project list logged in
    def test_list_projects_view_with_authenticated_user(self):
        self.client.login(username=self.user.username, password="testpassword")
        response = self.client.get(reverse("projects:list_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.project1, response.context["myprojects"])
        self.assertIn(self.project2, response.context["myprojects"])
        # correct number of total mice in project

    # Access the project listview without logging in
    def test_list_projects_view_login_required(self):
        response = self.client.get(reverse("projects:list_projects"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("projects:list_projects")}'
        )


class ShowProjectViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory
        self.request = Request.objects.create(researcher=self.user)

    # Broken test. Likely many issues
    """
    # GET behaviour to show project
    def test_show_project_get(self):
        response = self.client.get(
            reverse("show_project", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "researcher/show_project.html")
        self.assertContains(response, self.project.project_name)
        self.assertIn("myproject", response.context)
        self.assertIn("mymice", response.context)
        self.assertIn("mice_ids_with_requests", response.context)
        self.assertIn("project_name", response.context)
        self.assertIn("filter", response.context)

    # POST MouseSelectionForm
    def test_show_project_post(self):
        response = self.client.post(
            reverse("add_request", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")

    # Access non-existent project
    def test_show_non_existent_project(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("show_project", args=["AnyOtherName"]))

    # Access project without logging in
    def test_show_project_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("show_project", args=[self.project.project_name])
        )
        url = reverse("show_project", args=[self.project.project_name])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")
    """
