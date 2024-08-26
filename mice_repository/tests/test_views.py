from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from main.form_factories import RepositoryMiceFormFactory
from main.model_factories import MouseCommentFactory, MouseFactory, UserFactory
from mice_repository.forms import MouseCommentForm, RepositoryMiceForm
from mice_repository.models import Mouse


def setUpModule():
    global test_user, test_client, test_dob
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)
    test_dob = date.fromisoformat("2020-01-01")


def tearDownModule():
    global test_user
    test_user.delete()


class MiceRepositoryViewGetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.response = test_client.get(reverse("mice_repository:mice_repository"))

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "mice_repository.html")

    def test_context_contains_repository_mice(self):
        self.assertIn("repository_mice_qs", self.response.context)

    def test_context_contains_mouse(self):
        self.assertIn(self.mouse, self.response.context["repository_mice_qs"])


class AddMouseToRepositoryViewGetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.get(
            reverse("mice_repository:add_mouse_to_repository")
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "add_mouse_to_repository.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], RepositoryMiceForm)


class AddMouseToRepositoryViewPostTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.response = test_client.post(
            reverse("mice_repository:add_mouse_to_repository"),
            RepositoryMiceFormFactory.valid_data(),
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertRedirects(self.response, reverse("mice_repository:mice_repository"))

    def test_mouse_created(self):
        self.assertEqual(Mouse.objects.all().count(), 1)


class EditMouseInRepositoryViewGetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.response = test_client.get(
            reverse("mice_repository:edit_mouse_in_repository", args=[cls.mouse.pk])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "edit_mouse_in_repository.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], RepositoryMiceForm)

    def test_context_contains_mouse(self):
        self.assertIn("mouse", self.response.context)

    def test_context_contains_mouse_instance(self):
        self.assertEqual(self.mouse, self.response.context["mouse"])


class EditMouseInRepositoryViewPostTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory(coat="Black")
        data = RepositoryMiceFormFactory.valid_data(coat="White")
        cls.response = test_client.post(
            reverse("mice_repository:edit_mouse_in_repository", args=[cls.mouse.pk]),
            data,
        )
        cls.mouse.refresh_from_db()

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertRedirects(self.response, reverse("mice_repository:mice_repository"))

    def test_mouse_updated(self):
        self.assertEqual(self.mouse.coat, "White")


class MouseCommentExistingGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.comment = MouseCommentFactory(comment_id=cls.mouse)
        cls.response = test_client.get(
            reverse("mice_repository:show_mouse_comment", args=[cls.mouse.pk]),
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "show_mouse_comment.html")

    def test_correct_form(self):
        self.assertIsInstance(self.response.context["form"], MouseCommentForm)

    def test_correct_text(self):
        pass


class MouseCommentMakeNewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.response = test_client.get(
            reverse("mice_repository:show_mouse_comment", args=[cls.mouse.pk]),
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "show_mouse_comment.html")


class MouseCommentPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse = MouseFactory()
        cls.comment = MouseCommentFactory(comment_id=cls.mouse)
        data = {"comment_id": cls.mouse, "comment_text": "New test comment"}
        cls.response = test_client.post(
            reverse("mice_repository:show_mouse_comment", args=[cls.mouse.pk]), data
        )
        cls.comment.refresh_from_db()

    def test_correct_text(self):
        self.assertEqual(self.comment.comment_text, "New test comment")
