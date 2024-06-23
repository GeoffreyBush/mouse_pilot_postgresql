from django.test import TestCase

from mouse_pilot_postgresql.form_factories import MouseSelectionFormFactory
from mouse_pilot_postgresql.forms import MouseSelectionForm
from mouse_pilot_postgresql.model_factories import (
    MouseCommentFactory,
    MouseFactory,
    ProjectFactory,
)
from website.forms import MouseCommentForm
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
        self.assertIn(
            "At least one mouse must be selected for a request", form.non_field_errors()
        )


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
