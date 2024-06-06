from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from mouse_pilot_postgresql.form_factories import NewProjectFormFactory
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)


class ProjectModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory(project_name="testproject")
        cls.project.strains.add(StrainFactory(), StrainFactory())
        cls.project.researchers.add(UserFactory(), UserFactory())

    def test_project_pk_is_int(self):
        self.assertIsInstance(self.project.pk, int)

    def test_project_name(self):
        self.assertEqual(self.project.project_name, "testproject")

    def test_many_to_many_strains(self):
        self.assertEqual(self.project.strains.count(), 2)

    def test_many_to_many_researchers(self):
        self.assertEqual(self.project.researchers.count(), 2)

    def test_project_mice_count(self):
        self.assertEqual(self.project.mice.count(), 0)
        MouseFactory(project=self.project)
        self.assertEqual(self.project.mice.count(), 1)

    def test_uniqueness_of_project_name(self):
        with self.assertRaises(IntegrityError):
            ProjectFactory(project_name="testproject")


class NewProjectFormTestCase(TestCase):
    def setUp(self):
        self.form = NewProjectFormFactory.create()

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())

    def test_no_project_name(self):
        pass

    def test_uniqueness_of_project_name(self):
        pass

    def test_name_change_doesnt_create_duplicate(self):
        pass


# Filter form tests


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

    def test_get_request_unauthenticated(self):
        response = self.client.get(reverse("projects:list_projects"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("projects:list_projects")}'
        )


# Create new project


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
        self.assertIn("project_mice", response.context)

    def test_get_request_unauthenticated(self):
        url = reverse("projects:show_project", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_show_non_existent_project(self):
        self.client.force_login(self.user)
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("projects:show_project", args=["AnyOtherName"]))


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
