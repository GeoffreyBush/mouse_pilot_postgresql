from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)

def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)

def tearDownModule():
    global test_user
    test_user.delete()


class ProjectMouseFilterViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        cls.project.mice.add(
            MouseFactory(sex="M", earmark="TL"),
            MouseFactory(sex="F", earmark="TL"),
            MouseFactory(sex="M"),
            MouseFactory(sex="F"),
        )

    def test_empty_filter(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertEqual(len(response.context["project_mice"].qs), 4)

    def test_filter_cancelled(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"cancel": ""},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 4)

    def test_sex_filter_applied(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "sex": "M"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)

    def test_earmark_filter(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)

    def test_earmark_and_sex_filter(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL", "sex": "F"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 1)

    def test_cancel_after_filter(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"cancel": ""},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 4)

    def test_no_matching_mice(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TR"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 0)

    def test_filter_replace_another_filter(self):
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TL"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 2)
        response = test_client.get(
            reverse("projects:show_project", args=[self.project.project_name]),
            {"search": "", "earmark": "TR"},
        )
        self.assertEqual(len(response.context["project_mice"].qs), 0)
