from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.forms import MouseSelectionForm
from website.models import Strain

# Need to test where home page, logout page redirect to


############################
### MOUSE SELECTION FORM ###
############################
class MouseSelectionFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.mouse1, self.mouse2, self.mouse3 = (
            MouseFactory(project=self.project),
            MouseFactory(project=self.project),
            MouseFactory(),
        )
        self.form = MouseSelectionForm(
            project=self.project, data={"mice": [self.mouse1.pk, self.mouse2.pk]}
        )

    # Valid data
    def test_mouse_selection_form_valid_data(self):
        self.assertTrue(self.form.is_valid())

    # Correct mice count in request
    def test_mouse_selection_form_mice_count(self):
        self.form.is_valid()
        self.assertEqual(len(self.form.cleaned_data["mice"]), 2)

    # Correct project in request
    def test_mouse_selection_form_project(self):
        self.assertEqual(self.form.project, self.project)

    # Invalid form when mice from different projects are selected
    def test_mouse_selection_form_invalid_data(self):
        self.form = MouseSelectionForm(
            project=self.project, data={"mice": [self.mouse1.pk, self.mouse3.pk]}
        )
        self.assertFalse(self.form.is_valid())
        self.assertIn("mice", self.form.errors)

    # What happens when the form is saved? Need to test this too


##############
### STRAIN ###
##############
class StrainModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.strain = StrainFactory(strain_name="teststrain")

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

    # Delete mouse while not logged in
    def test_delete_mouse_view_unauthenticated_user(self):
        self.client.logout()
        url = reverse(
            "website:delete_mouse", args=[self.project.project_name, self.mouse.pk]
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")
        self.assertIsInstance(Mouse.objects.first(), Mouse)


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

    # Access edit history while not logged in
    def test_edit_history_view_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse("edit_history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    # Edit history contains correct data
    def test_edit_history_view(self):
        response = self.client.get(reverse("edit_history"))
        self.assertContains(response, self.history1.project)
        self.assertContains(response, self.history2.project)

    # Should test an actual edit of the mice here too
"""
