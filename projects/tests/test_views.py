from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.form_factories import (
    MouseSelectionFormFactory,
    NewProjectFormFactory,
)
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)
from projects.filters import ProjectFilter
from projects.forms import NewProjectForm
from projects.models import Project
from website.forms import MouseSelectionForm


class ListProjectsViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.client = Client()
        cls.project = ProjectFactory()
        cls.project.mice.add(MouseFactory())
        cls.client.force_login(cls.user)
        cls.response = cls.client.get(reverse("projects:list_projects"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "list_projects.html")

    def test_project_count(self):
        self.assertEqual(self.response.context["myprojects"].count(), 1)

    def test_project_mice_count(self):
        self.assertEqual(self.response.context["myprojects"][0].mice.count(), 1)


class AddNewProjectViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.client = Client()
        cls.client.force_login(cls.user)
        cls.response = cls.client.get(reverse("projects:add_new_project"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "add_new_project.html")

    def test_new_project_form(self):
        self.assertIsInstance(self.response.context["form"], NewProjectForm)


class AddNewProjectViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(username="testuser")
        cls.client = Client()
        cls.client.force_login(cls.user)
        cls.response = cls.client.post(
            reverse("projects:add_new_project"), NewProjectFormFactory.valid_data()
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(self.response.url, reverse("projects:list_projects"))

    def test_project_created(self):
        self.assertEqual(Project.objects.all().count(), 1)


class ShowProjectViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory(username="testuser")
        cls.client.force_login(cls.user)
        cls.response = cls.client.get(
            reverse("projects:show_project", args=[ProjectFactory().project_name])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "show_project.html")

    def test_project_in_context(self):
        self.assertIn("project", self.response.context)

    def test_filter_in_context(self):
        self.assertIsInstance(self.response.context["project_mice"], ProjectFilter)

    def test_mouse_selection_form_in_context(self):
        self.assertIsInstance(self.response.context["form"], MouseSelectionForm)

    def test_show_non_existent_project(self):
        self.client.force_login(self.user)
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("projects:show_project", args=["AnyOtherName"]))


class ShowProjectViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = UserFactory()
        cls.project = ProjectFactory()
        cls.client.force_login(cls.user)
        data = MouseSelectionFormFactory.valid_data(project=cls.project)
        cls.response = cls.client.post(
            reverse("projects:show_project", args=[cls.project.project_name]), data
        )
        cls.session = cls.client.session

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(
            self.response.url,
            reverse("mice_requests:add_request", args=[self.project.project_name]),
        )

    def test_selected_mice_in_session(self):
        self.assertEqual(
            self.session["selected_mice"],
            [mouse.pk for mouse in self.project.mice.all()],
        )


# Test valid POST request
# Test that MouseSelection form values are saved in session data during valid POST request

# Test that the render in POST doesnt cause a NoReverseMatch error
