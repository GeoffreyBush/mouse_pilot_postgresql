from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import MouseSelectionFormFactory
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.models import Strain


class MouseSelectionFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        (
            self.mouse1,
            self.mouse2,
        ) = (
            MouseFactory(project=self.project),
            MouseFactory(),
        )
        self.form = MouseSelectionFormFactory.create(
            project=self.project, mice=[self.mouse1]
        )

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_correct_queryset_without_project(self):
        self.form = MouseSelectionFormFactory.create()
        self.assertEqual(self.form.fields["mice"].queryset.count(), 2)

    def test_correct_queryset_with_project(self):
        self.assertEqual(self.form.fields["mice"].queryset.count(), 1)

    def test_save_is_disabled(self):
        self.assertIsNone(self.form.save())


##############
### STRAIN ###
##############
class StrainModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")

    def test_strain_creation(self):
        self.assertIsInstance(self.strain, Strain)

    # Duplicate strain name
    def test_strain_duplicates(self):
        with self.assertRaises(IntegrityError):
            Strain.objects.create(strain_name="teststrain")

    # Increment mice count of a strain by making a mouse
    def test_strain_mice_count(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.mouse = MouseFactory(strain=self.strain)
        self.assertEqual(self.strain.mice_count, 1)

    # Decrement mice count from 1 to 0
    def test_strain_mice_count_decrement_from_one(self):
        self.strain.mice_count = 1
        self.assertEqual(self.strain.mice_count, 1)
        self.strain.decrement_mice_count()
        self.assertEqual(self.strain.mice_count, 0)

    # Decrement mice count of a a strain should not go below 0
    def test_strain_mice_count_decrement_from_zero(self):
        self.assertEqual(self.strain.mice_count, 0)
        self.strain.decrement_mice_count()
        self.assertEqual(self.strain.mice_count, 0)

    # Deleting a mouse should decrement the mice count

    # Changing the strain of a mouse should increment the new strain's mice count

    # Changing the strain of a mouse should decrement the old strain's mice count


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
