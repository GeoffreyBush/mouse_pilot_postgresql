from django.http import Http404
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from main.filters import MouseFilter
from main.form_factories import MouseSelectionFormFactory, ProjectFormFactory
from main.forms import MouseSelectionForm
from main.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from projects.forms import AddMouseToProjectForm, ProjectForm
from projects.models import Project
from projects.views import ShowProjectView, add_project


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
        cls.response = test_client.get(reverse("projects:add_project"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "add_project.html")

    def test_new_project_form(self):
        self.assertIsInstance(self.response.context["form"], ProjectForm)


class AddNewProjectViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.request = cls.factory.post(
            reverse("projects:add_project"), ProjectFormFactory.valid_data()
        )
        cls.request.user = test_user
        cls.response = add_project(cls.request)

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(self.response.url, reverse("projects:list_projects"))

    def test_project_created(self):
        self.assertEqual(Project.objects.all().count(), 1)


class EditProjectViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        cls.response = test_client.get(
            reverse("projects:edit_project", args=[cls.project.project_name])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "edit_project.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], ProjectForm)

    def test_context_contains_mouse(self):
        self.assertIn("project", self.response.context)

    def test_correct_project_in_context(self):
        self.assertEqual(self.response.context["project"], self.project)


class EditProjectViewPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory(research_area="disease1")
        data = ProjectFormFactory.valid_data(research_area="disease2")
        cls.response = test_client.post(
            reverse("projects:edit_project", args=[cls.project.project_name]), data
        )
        cls.project.refresh_from_db()

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(self.response.url, reverse("projects:list_projects"))

    def test_project_updated(self):
        self.assertEqual(self.project.research_area, "disease2")


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
        self.assertIsInstance(self.response.context["filter_form"], MouseFilter)

    def test_mouse_selection_form_in_context(self):
        self.assertIsInstance(self.response.context["select_form"], MouseSelectionForm)

    def test_query_params_in_context(self):
        self.assertIn("query_params", self.response.context)

    def test_get_non_existent_project(self):
        view = ShowProjectView()
        with self.assertRaises(Http404):
            view.get_project("nonexistent")


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
        self.assertIsInstance(self.response.context["filter_form"], MouseFilter)

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
        data = {
            "mice": [
                MouseFactory(strain=cls.strain, project=None).pk,
                MouseFactory(strain=cls.strain, project=None).pk,
            ]
        }
        cls.response = test_client.post(
            reverse("projects:add_mouse_to_project", args=[cls.project.project_name]),
            data,
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(self.response.url, reverse("projects:list_projects"))

    def test_mice_added_to_project(self):
        self.assertEqual(self.project.mice.count(), 2)
