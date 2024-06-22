from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlencode

from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)


class PaginateCombinedWithFilterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(username="testuser")
        cls.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.project = ProjectFactory()
        cls.male_mice = MouseFactory.create_batch(15, project=cls.project, sex="M")
        cls.female_mice = MouseFactory.create_batch(15, project=cls.project, sex="F")

    def setUp(self):
        self.client.force_login(self.user)
        self.data = {
            "csrfmiddlewaretoken": "dummytoken",
            "sex": "M",
            "earmark": "",
            "search": "",
        }
        self.url = self.get_url()

    def get_url(self, page=None, **kwargs):
        url = reverse("projects:show_project", args=[self.project.project_name])
        if kwargs or page:
            params = kwargs.copy()
            if page:
                params["page"] = page
            url += f"?{urlencode(params)}"
        return url

    def test_initial_page_no_filter(self):
        response = self.client.get(self.get_url())
        self.assertEqual(len(response.context["project_mice"]), 10)
        self.assertEqual(response.context["project_mice"].paginator.count, 30)

    def test_count_pagination_stats_after_filter_applied(self):
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.context["project_mice"].number, 1)
        self.assertEqual(response.context["project_mice"].paginator.count, 15)

    def test_filter_applied_on_another_page(self):
        self.data["page"] = 2
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.context["project_mice"].number, 2)
        self.assertEqual(len(response.context["project_mice"]), 5)
        self.assertEqual(response.context["project_mice"].paginator.count, 15)

    def test_invalid_page_with_filter_shows_last_page(self):
        self.data["page"], self.data["sex"] = 999, "F"
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.context["project_mice"].number, 2)
