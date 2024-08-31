from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from main.model_factories import MouseCommentFactory, MouseFactory, StrainFactory
from mice_repository.models import Mouse, MouseComment


def setUpModule():
    global test_dob
    test_dob = date.fromisoformat("2020-01-01")


class MouseModelUnitTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory.build(strain=self.strain, dob=test_dob)

    def test_mouse_creation(self):
        self.assertIsInstance(self.mouse, Mouse)

    def test_correct_strain(self):
        self.assertEqual(self.mouse.strain.strain_name, "teststrain")

    def test_clean_correct_pk(self):
        self.assertEqual(self.mouse.pk, "")
        self.mouse.clean()
        self.assertEqual(self.mouse.pk, "teststrain-1")

    def test_manual_tube_correct_value(self):
        self.manual_tube_mouse = MouseFactory(strain=self.strain, tube=123)
        self.assertEqual(self.manual_tube_mouse.tube, 123)

    def test_manual_tube_correct_pk(self):
        self.manual_tube_mouse = MouseFactory(strain=self.strain, tube=123)
        self.assertEqual(self.manual_tube_mouse.pk, "teststrain-123")

    def test_correct_age_days(self):
        correct_days = (date.today() - self.mouse.dob).days
        self.assertEqual(self.mouse.age_days, correct_days)

    def test_correct_age_months(self):
        correct_months = (date.today() - self.mouse.dob).days / 30
        self.assertEqual(self.mouse.age_months, correct_months)

    def test_adding_earmark_auto_genotypes_mouse(self):
        self.assertFalse(self.mouse.is_genotyped())
        self.mouse.earmark = "TR"
        self.assertTrue(self.mouse.is_genotyped())

    def test_cull_method_sets_culled_date(self):
        self.assertEqual(self.mouse.culled_date, None)
        self.mouse.cull(date.today())
        self.assertEqual(self.mouse.culled_date, date.today())

    def test_is_culled_method(self):
        self.assertFalse(self.mouse.is_culled())
        self.mouse.cull(date.today())
        self.assertTrue(self.mouse.is_culled())

    def test_cull_method_raises_error_when_already_culled(self):
        self.assertFalse(self.mouse.is_culled())
        self.mouse.cull(date.today())
        with self.assertRaises(ValidationError):
            self.mouse.cull(date.today())

    def test_cull_method_raises_error_when_no_culled_date(self):
        with self.assertRaises(TypeError):
            self.mouse.cull()


class MouseModelIntegrationTest(TestCase):
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")
        self.mouse = MouseFactory.create(strain=self.strain)

    def test_mouse_correct_auto_pk(self):
        self.assertEqual(self.mouse.pk, "teststrain-1")

    def test_mouse_auto_tube_increments_correctly(self):
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.auto_tube_mouse.tube, 2)

    def test_mouse_auto_tube_increments_pk_correctly(self):
        self.auto_tube_mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.auto_tube_mouse.pk, "teststrain-2")

    def test_mouse_cannot_be_overwritten_by_duplicate_tube(self):
        with self.assertRaises(ValidationError):
            self.duplicate_mouse = MouseFactory(
                strain=self.strain, tube=self.mouse.tube
            )

    def test_increment_strain_count_when_validate_unique_mouse_passes(self):
        self.assertEqual(self.strain.mice.count(), 1)
        self.extra_mouse = MouseFactory(strain=self.strain, tube=5)
        self.assertEqual(self.strain.mice.count(), 2)

    def test_no_increment_strain_count_when_validate_unique_mouse_fails(self):
        self.assertEqual(self.strain.mice.count(), 1)
        with self.assertRaises(ValidationError):
            self.duplicate_mouse = MouseFactory(
                strain=self.strain, tube=self.mouse.tube
            )
        self.assertEqual(self.strain.mice.count(), 1)

    # Mother must be female

    # Father must be male

    # Parents cannot be born after child

    # clipped_date must be after dob. All dates must be after dob

    # dob must be in the past

    # If the mouse is genotyped, the genotyper must be set

    # Can be in either a breeding cage, stock cage, or experimental cage

    # Test how related_name = mouse_mother/father works. Does it mean you can see all children of a mouse?


class MouseCommentModelTest(TestCase):
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
