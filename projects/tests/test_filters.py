from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)

class ProjectMouseFilterViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(username="testuser")
        cls.client = Client()
        cls.project = ProjectFactory()
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(sex="M", project=cls.project, earmark="TL"),
            MouseFactory(sex="F", project=cls.project, earmark="TL"),
            MouseFactory(sex="M", project=cls.project),
            MouseFactory(sex="F", project=cls.project),
        )

    def test_empty_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertEqual(len(response.context["project_mice"].qs), 4)

    def test_filter_cancelled(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"cancel": ""},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 4)

    def test_sex_filter_applied(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "sex": "M"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)

    def test_earmark_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)

    def test_earmark_and_sex_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL", "sex": "F"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 1)

    def test_cancel_after_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"cancel": ""},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 4)

    def test_no_matching_mice(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TR"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 0)

    def test_filter_replace_another_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)
        response = self.client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TR"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 0)