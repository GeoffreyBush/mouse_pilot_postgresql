from django.test import TestCase

from mouse_pilot_postgresql.form_factories import MouseSelectionFormFactory
from mouse_pilot_postgresql.model_factories import MouseFactory, ProjectFactory, MouseCommentFactory
from website.forms import MouseSelectionForm, MouseCommentForm
from website.models import MouseComment


class MouseSelectionFormTest(TestCase):
    def setUp(self):
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.project = ProjectFactory()
        self.project.mice.add(self.mouse1)
        self.form = MouseSelectionFormFactory.build(
            project=self.project, mice=[self.mouse1]
        )

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_correct_queryset_without_project(self):
        self.form = MouseSelectionFormFactory.build(
            project=None, mice=[self.mouse1, self.mouse2]
        )
        self.assertEqual(self.form.fields["mice"].queryset.count(), 2)

    def test_correct_queryset_with_project(self):
        self.assertEqual(self.form.fields["mice"].queryset.count(), 1)

    def test_save_is_disabled(self):
        self.assertIsNone(self.form.save())

    def test_clean_mice_no_selection(self):
        form_data = {}
        form = MouseSelectionForm(form_data, project=self.project)
        self.assertIn("At least one mouse must be selected for a request", form.non_field_errors())


class CommentModelTest(TestCase):
    def setUp(self):
        self.mouse = MouseFactory()
        self.comment = MouseCommentFactory.build(comment_id=self.mouse)

    def test_comment_exists(self):
        self.assertIsInstance(self.comment, MouseComment)

    def test_correct_pk(self):
        self.assertEqual(self.comment.comment_id, self.mouse)

    def test_comment_deleted_with_mouse(self):
        self.mouse.delete()
        self.assertIsNone(MouseComment.objects.first())

    def test_text_can_be_changed(self):
        self.assertEqual(self.comment.comment_text, "Test comment")
        self.comment.comment_text = "Another test comment"
        self.assertEqual(self.comment.comment_text, "Another test comment")


class CommentFormTest(TestCase):
    def setUp(self):
        self.mouse = MouseFactory()
        data = {"comment_id": self.mouse, "comment_text": "Test comment"}
        self.form = MouseCommentForm(data=data)

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

"""
class DeleteMouseViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project = ProjectFactory()
        self.mouse = MouseFactory(project=self.project)

    def test_mouse_exists(self):
        self.assertIsInstance(Mouse.objects.first(), Mouse)

    # Delete mouse while logged in
    def test_delete_mouse_view_authenticated_user(self):
        response = self.client.get(
            reverse(
                "website:delete_mouse", args=[self.project.project_name, self.mouse.pk]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("projects:show_project", args=[self.project.project_name])
        )
        self.assertIsNone(Mouse.objects.first())
"""

# Edit history is broken by mice not being created with tube attribute
"""
class EditHistoryViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project1, self.project2 = ProjectFactory(), ProjectFactory()

        self.history1 = HistoricalMouse.objects.create(
            history_date=timezone.now(),
            sex="M",
            dob=date.today(),
            project=self.project1,
        )
        self.history2 = HistoricalMouse.objects.create(
            history_date=timezone.now(),
            sex="F",
            dob=date.today(),
            project=self.project2,
        )

    # Access edit history while logged in
    def test_edit_history_view_with_authenticated_user(self):
        response = self.client.get(reverse("edit_history"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_history.html")

    # Edit history contains correct data
    def test_edit_history_view(self):
        response = self.client.get(reverse("edit_history"))
        self.assertContains(response, self.history1.project)
        self.assertContains(response, self.history2.project)

    # Should test an actual edit of the mice here too
"""
# Need to test where home page, logout page redirect to
