from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.form_factories import (
    MouseSelectionFormFactory,
    NewProjectFormFactory,
)
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from projects.filters import ProjectFilter
from projects.forms import AddMouseToProjectForm, NewProjectForm
from projects.models import Project
from projects.views import add_new_project
from website.forms import MouseSelectionForm


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class ListProjectsViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        cls.project.mice.add(MouseFactory())
        cls.response = test_client.get(reverse("projects:list_projects"))

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
        cls.response = test_client.get(reverse("projects:add_new_project"))

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
        cls.factory = RequestFactory()
        cls.request = cls.factory.post(
            reverse("projects:add_new_project"), NewProjectFormFactory.valid_data()
        )
        cls.request.user = test_user
        cls.response = add_new_project(cls.request)

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
        cls.response = test_client.get(
            reverse("projects:show_project", args=[ProjectFactory().project_name])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "show_project.html")

    def test_project_in_context(self):
        self.assertIn("project", self.response.context)

    def test_filter_in_context(self):
        self.assertIsInstance(self.response.context["filter_form"], ProjectFilter)

    def test_mouse_selection_form_in_context(self):
        self.assertIsInstance(self.response.context["select_form"], MouseSelectionForm)

    def test_query_params_in_context(self):
        self.assertIn("query_params", self.response.context)

    def test_show_non_existent_project(self):
        with self.assertRaises(ObjectDoesNotExist):
            test_client.get(reverse("projects:show_project", args=["AnyOtherName"]))

    # Add filter form in context


class ShowProjectViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        data = MouseSelectionFormFactory.data(project=cls.project)
        cls.response = test_client.post(
            reverse("projects:show_project", args=[cls.project.project_name]), data
        )
        cls.session = test_client.session

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


class ShowProjectViewInvalidPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        data = MouseSelectionFormFactory.data(mice=[])
        cls.response = test_client.post(
            reverse("projects:show_project", args=[cls.project.project_name]), data
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "show_project.html")

    def test_project_in_context(self):
        self.assertIn("project", self.response.context)

    def test_filter_in_context(self):
        self.assertIsInstance(self.response.context["filter_form"], ProjectFilter)

    def test_mouse_selection_form_in_context(self):
        self.assertIsInstance(self.response.context["select_form"], MouseSelectionForm)

    def test_query_params_in_context(self):
        self.assertIn("query_params", self.response.context)

    # def test_error_message_displayed_to_user(self):
    #   self.assertIn(
    #      "At least one mouse must be selected for a request",
    #     self.response.content.decode(),
    # )


class InfoPanelViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(
            reverse("projects:info_panel", args=[MouseFactory().pk])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "info_panel.html")

    def test_mouse_in_context(self):
        self.assertIn("mouse", self.response.context)


class AddMouseToProjectViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory.create()
        cls.strain = StrainFactory.create()
        cls.project.strains.add(cls.strain)
        cls.response = test_client.get(
            reverse("projects:add_mouse_to_project", args=[cls.project.project_name])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "add_mouse_to_project.html")

    def test_form_in_context(self):
        self.assertIsInstance(self.response.context["form"], AddMouseToProjectForm)

    def test_project_name_in_context(self):
        self.assertIn("project_name", self.response.context)

    
class AddMouseToProjectViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory.create()
        cls.strain = StrainFactory.create()
        cls.project.strains.add(cls.strain)
        data = {"mice": [MouseFactory(strain=cls.strain, project=None).pk, MouseFactory(strain=cls.strain, project=None).pk]}
        cls.response = test_client.post(
            reverse("projects:add_mouse_to_project", args=[cls.project.project_name]), data
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(self.response.url, reverse("projects:list_projects"))

    def test_mice_added_to_project(self):
        self.assertEqual(self.project.mice.count(), 2)
