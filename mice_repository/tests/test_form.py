from django.test import TestCase

from main.form_factories import RepositoryMiceFormFactory
from main.model_factories import MouseFactory, StrainFactory
from mice_repository.forms import MouseCommentForm, RepositoryMiceForm
from mice_repository.models import Mouse


class RepositoryMiceFormTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory.create()

    def test_valid_data(self):
        form = RepositoryMiceFormFactory.build()
        self.assertTrue(form.is_valid())

    def test_invalid_sex(self):
        form = RepositoryMiceFormFactory.build(sex="X")
        self.assertFalse(form.is_valid())

    def test_form_creates_mouse(self):
        self.form = RepositoryMiceFormFactory.build()
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.form.save()
        self.assertEqual(Mouse.objects.all().count(), 1)

    def test_invalid_dob(self):
        form = RepositoryMiceFormFactory.build(dob=None)
        self.assertIn("dob", form.errors)

    def test_no_global_id_field(self):
        self.assertFalse("_global_id" in RepositoryMiceForm().fields)

    def test_manual_correct_tube_value(self):
        self.form = RepositoryMiceFormFactory.build(tube=123)
        self.mouse = self.form.save()
        self.assertEqual(self.mouse.tube, 123)

    def test_manual_tube_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.build(strain=self.strain, tube=123)
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.mouse = self.form.save()
        self.assertEqual(self.strain.mice.count(), 1)

    def test_auto_tube_correct_tube_value(self):
        self.mouse1 = MouseFactory.create(strain=self.strain)
        self.form = RepositoryMiceFormFactory.build(strain=self.strain)
        self.mouse2 = self.form.save()
        self.assertEqual(self.mouse2.tube, 2)

    def test_auto_tube_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.build(strain=self.strain)
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.form.save()
        self.assertEqual(self.strain.mice.count(), 1)

    def test_tube_is_none_correct_tube_value(self):
        self.mouse1 = MouseFactory.create(strain=self.strain)
        self.form = RepositoryMiceFormFactory.build(strain=self.strain, tube=None)
        self.mouse2 = self.form.save()
        self.assertEqual(self.mouse2.tube, 2)

    def test_tube_is_none_correct_mice_count(self):
        self.form = RepositoryMiceFormFactory.build(strain=self.strain, tube=None)
        self.assertEqual(Mouse.objects.all().count(), 0)
        self.form.save()
        self.assertEqual(self.strain.mice.count(), 1)

    # Mother choices are female

    # Father choices are male

    # What happens if you try to edit a mouse's tube to:
    # 1. A tube that exists
    # 2. A tube that doesn't exist


class CommentFormTest(TestCase):
    def setUp(self):
        self.mouse = MouseFactory()
        data = {"comment_id": self.mouse, "comment_text": "Test comment"}
        self.form = MouseCommentForm(data=data)

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())
