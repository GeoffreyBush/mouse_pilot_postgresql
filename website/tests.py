
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from mice_repository.models import Mouse
from test_factories.form_factories import RequestFormFactory
from test_factories.model_factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)
from website.forms import MouseSelectionForm, RequestForm
from website.models import Request, Strain

# Need to test where home page, logout page redirect to


####################
### REQUEST FORM ###
####################
class RequestFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(project=self.project), MouseFactory(
            project=self.project
        )

    # Valid data
    def test_request_form_valid_data(self):
        form = RequestForm(
            project=self.project,
            data=RequestFormFactory.valid_data(self.mouse1, self.mouse2),
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.save().mice.count(), 2)

    # Invalid data
    def test_request_form_invalid_data(self):
        form = RequestForm(
            project=self.project,
            data=RequestFormFactory.missing_mice(),
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mice", form.errors)

    # There must be at least one mouse present in a request


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


###############
### REQUEST ###
###############


class RequestModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.strain = StrainFactory()
        self.mouse1, self.mouse2 = MouseFactory(strain=self.strain), MouseFactory(
            strain=self.strain
        )

        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse1, self.mouse2)

    # Request creation
    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)

    # Test is broken until confirming clip adds an earmark
    # Confirm method
    """
    def test_request_confirm(self):
        self.assertFalse(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertFalse(mouse.is_genotyped())

        self.request.confirm()

        self.request.refresh_from_db()
        for mouse in self.request.mice.all():
            mouse.refresh_from_db()

        self.assertTrue(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertTrue(mouse.is_genotyped())
    """

    # There must be at least one mouse present in a request


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


class ShowRequestsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.requests = [
            Request.objects.create(
                request_id=1, researcher=self.user, task_type="Cl", confirmed=True
            ),
            Request.objects.create(
                request_id=2, researcher=self.user, task_type="Cu", confirmed=False
            ),
            Request.objects.create(
                request_id=3, researcher=self.user, task_type="Mo", confirmed=True
            ),
        ]

    # Show requests whilelogged in
    def test_show_requests_view(self):
        response = self.client.get(reverse("website:show_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_requests.html")
        self.assertQuerysetEqual(
            response.context["requests"], self.requests, ordered=False
        )

    # Show requests while not logged in
    def test_show_requests_view_login_required(self):
        self.client.logout()
        url = reverse("website:show_requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class AddRequestViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(), MouseFactory()
        self.mice = [self.mouse1, self.mouse2]

    # GET RequestForm while logged in
    def test_add_request_get(self):
        url = reverse("website:add_request", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)

    # Get RequestForm while not logged in
    def test_add_request_get_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse("website:add_request", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    # POST RequestForm with valid data
    # mouse.tube has broken this test
    """
    def test_add_request_post_valid(self):
        url = reverse("add_request", args=[self.project.project_name])
        data = {
            "task_type": "Cl",
            "mice": [self.mice[0].tube, self.mice[1].tube],
            "new_message": "Test message",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.project_name])
        )
        self.assertTrue(
            Request.objects.filter(task_type="Cl", mice__in=self.mice).exists()
        )
        self.assertEqual(Request.objects.count(), 1)
        request = Request.objects.first()
        self.assertEqual(request.task_type, "Cl")
        self.assertEqual(request.new_message, "Test message")
        self.assertQuerySetEqual(
            request.mice.all(), [self.mouse1, self.mouse2], ordered=False
        )
    """

    # Can't trust this test because of the mouse.tube issue.
    # Must fix POST with valid data test first
    """
    # POST RequestForm with invalid data
    def test_add_request_post_invalid(self):
        url = reverse("add_request", args=[self.project.project_name])
        data = {"task_type": "Invalid", "mice": []}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)
        self.assertFalse(Request.objects.exists())

    # Try to add request to a non-existent project
    def test_add_request_with_non_existent_project(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("add_request", args=["AnyOtherName"]))
    """


class ConfirmRequestViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.mouse = MouseFactory()
        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse)

    # Unauthenticated user redirected to login page
    def test_confirm_request_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("website:confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('website:confirm_request', args=[self.request.request_id])}",
        )

    # Redirect to show_requests after confirming
    def test_confirm_request_view_get_request(self):
        response = self.client.get(
            reverse("website:confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("website:show_requests"))

    # Need to get the clip request to ask for an earmark input for this test to work now
    # Confirm request changes mice.genotyped to True
    """
    def test_confirm_request_view_updates_request_status(self):
        self.client.get(reverse("confirm_request", args=[self.request.request_id]))
        self.request.refresh_from_db()
        self.assertTrue(self.request.confirmed)
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.is_genotyped())
    """


# Test additional behaviour added in the future to requests, such as earmark addition, moving, or clipping
