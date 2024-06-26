from django.test import Client, TestCase
from django.urls import reverse

from main.form_factories import MiceRequestFormFactory
from main.model_factories import (
    MiceRequestFactory,
    MouseFactory,
    ProjectFactory,
    UserFactory,
)
from mice_requests.forms import RequestForm
from mice_requests.models import Request


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class ShowRequestsViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.requests = [MiceRequestFactory() for _ in range(3)]
        cls.response = test_client.get(reverse("mice_requests:show_requests"))

    def test_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "show_requests.html")

    def test_requests_in_response(self):
        self.assertQuerysetEqual(
            self.response.context["requests"], self.requests, ordered=False
        )


class AddRequestViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mice = [MouseFactory(), MouseFactory()]
        test_client.session["selected_mice"] = [mouse.pk for mouse in cls.mice]
        test_client.session.save()
        cls.url = reverse(
            "mice_requests:add_request", args=[ProjectFactory().project_name]
        )
        cls.response = test_client.get(cls.url)

    def test_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "add_request.html")

    def test_form_in_context(self):
        self.assertIsInstance(self.response.context["form"], RequestForm)

    def test_mice_in_form(self):
        self.assertQuerysetEqual(
            self.response.context["form"].fields["mice"].queryset,
            self.mice,
            ordered=False,
        )


class AddRequestViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        cls.mice = [MouseFactory(), MouseFactory()]
        cls.url = reverse("mice_requests:add_request", args=[cls.project.project_name])
        cls.response = test_client.post(
            cls.url, MiceRequestFormFactory.valid_data(mice=cls.mice)
        )

    def test_code_302(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirects_to_project(self):
        self.assertRedirects(
            self.response,
            reverse("projects:show_project", args=[self.project.project_name]),
        )

    def test_request_created(self):
        self.assertEqual(Request.objects.count(), 1)

    def test_request_mice(self):
        self.assertQuerysetEqual(
            Request.objects.first().mice.all(), self.mice, ordered=False
        )
