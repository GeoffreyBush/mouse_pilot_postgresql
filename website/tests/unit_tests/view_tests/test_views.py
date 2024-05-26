from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from website.forms import (
    CustomUserCreationForm,
    ProjectMiceForm,
    RequestForm,
)
from website.models import (
    CustomUser,
    HistoricalMouse,
    Mouse,
    Project,
    Request,
    Strain,
)
from website.tests.factories import UserFactory
from website.views import SignUpView

##########################
### EDIT BREEDING CAGE ###
##########################


############################
### ADD INDIVIDUAL MOUSE ###
############################
class AddMouseViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.project = Project.objects.create(project_name="TestProject")

    # Access add_preexisting_mouse_to_project while logged in
    def test_add_preexisting_mouse_to_project_get(self):
        url = reverse(
            "add_preexisting_mouse_to_project", args=[self.project.project_name]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "researcher/add_preexisting_mouse_to_project.html"
        )
        self.assertIsInstance(response.context["mice_form"], ProjectMiceForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)

    # Add valid data test here
    """ Likely similar valid POST issue as edit_mouse test, below, where genotyper field causes issues """

    def test_add_preexisting_mouse_to_project_post_invalid(self):
        url = reverse(
            "add_preexisting_mouse_to_project", args=[self.project.project_name]
        )
        data = {
            "sex": "Invalid",
            "dob": "2022-01-01",
            "genotyped": True,
            "project": self.project.project_name,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "researcher/add_preexisting_mouse_to_project.html"
        )
        self.assertIsInstance(response.context["mice_form"], ProjectMiceForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)
        self.assertFalse(Mouse.objects.exists())

    # Access add_preexisting_mouse_to_project without logging in
    def test_add_preexisting_mouse_to_project_view_login_required(self):
        self.client.logout()
        url = reverse(
            "add_preexisting_mouse_to_project", args=[self.project.project_name]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


##################
### EDIT MOUSE ###
##################
class EditMouseViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.project = Project.objects.create(project_name="TestProject")
        self.genotyper = CustomUser.objects.create_user(
            username="TestGenotyper",
            email="testgenotyper@example.com",
            password="testpassword",
        )
        self.mouse1 = Mouse.objects.create(
            sex="M", dob=date.today(), genotyped=True, project=self.project
        )
        self.mouse2 = Mouse.objects.create(
            sex="F", dob=date.today(), genotyped=True, project=self.project
        )
        self.mouse3 = Mouse.objects.create(
            sex="M", dob=date.today(), genotyped=True, project=self.project
        )

        # Add cage back in when stock or experimental cage is added to Mouse model
        """
        self.cage = Cage.objects.create(
            cageID=1, box_no="1-1", date_born=date.today(), date_wean=date.today()
        )
        """
        self.strain = Strain.objects.create(strain_name="TestStrain")

    # Access edit_mouse while logged in
    def test_edit_mouse_get(self):
        url = reverse("edit_mouse", args=[self.project.project_name, self.mouse1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_mouse.html")
        self.assertIsInstance(response.context["form"], ProjectMiceForm)
        self.assertEqual(response.context["form"].instance, self.mouse1)
        self.assertEqual(response.context["project_name"], self.project.project_name)

    # Can't get this valid POST test to work correctly. Genotyper field causes issues
    """
    # POST with valid data
    def test_edit_mouse_post_valid(self):
        url = reverse('edit_mouse', args=[self.project.project_name, self.mouse1.id])
        data = {
            'sex': 'M',
            'dob': date.today(),
            'clipped_date': date.today(),
            'genotyped': True,
            'mother': self.mouse2,
            'father': self.mouse3,
            'cage': self.cage,
            'project': self.project,
            'genotyper': self.genotyper,
            'strain': self.strain,
            'earmark': 'BR',
        }
        response = self.client.post(url, data)
        form = response.context['form']
        print("form.errors")
        print(form.errors)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'show_project.html')
    """

    # POST with invalid data
    def test_edit_mouse_post_invalid(self):
        url = reverse("edit_mouse", args=[self.project.project_name, self.mouse1.id])
        data = {
            "sex": "Invalid",
            "dob": date.today(),
            "genotyped": False,
            "project": self.project.project_name,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_mouse.html")
        self.assertIsInstance(response.context["form"], ProjectMiceForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)
        self.mouse1.refresh_from_db()
        self.assertEqual(self.mouse1.sex, "M")
        self.assertEqual(self.mouse1.dob, date.today())
        self.assertTrue(self.mouse1.genotyped)

    # Access edit_mouse without logging in
    def test_edit_mouse_view_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse("edit_mouse", args=[self.project.project_name, self.mouse1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


#########################
### SHOW EDIT HISTORY ###
#########################
class EditHistoryViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.project1 = Project.objects.create(project_name="TestProject1")
        self.project2 = Project.objects.create(project_name="TestProject2")

        self.history1 = HistoricalMouse.objects.create(
            id=1,
            history_date=timezone.now(),  # Using timezone to avoid warnings about a 'naive datetime'
            sex="M",
            dob=date.today(),
            genotyped=False,
            project=self.project1,
        )
        self.history2 = HistoricalMouse.objects.create(
            id=2,
            history_date=timezone.now(),
            sex="F",
            dob=date.today(),
            genotyped=True,
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

    def test_edit_history_view(self):
        response = self.client.get(reverse("edit_history"))
        self.assertContains(response, self.history1.project)
        self.assertContains(response, self.history2.project)


####################
### DELETE MOUSE ###
####################
class DeleteMouseViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.project = Project.objects.create(project_name="TestProject")
        self.mouse = Mouse.objects.create(
            sex="M", dob=date.today(), genotyped=True, project=self.project
        )

    # Delete mouse while logged in
    def test_delete_mouse_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("delete_mouse", args=[self.project.project_name, self.mouse.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.project_name])
        )
        self.assertFalse(Mouse.objects.filter(id=self.mouse.id).exists())

    # Delete mouse while not logged in
    def test_delete_mouse_view_login_required(self):
        url = reverse("delete_mouse", args=[self.project.project_name, self.mouse.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


#####################
### SHOW REQUESTS ###
#####################
class ShowRequestsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
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
        self.client.login(username="testuser", password="testpassword")
        url = reverse("show_requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_requests.html")
        self.assertQuerysetEqual(
            response.context["requests"], self.requests, ordered=False
        )

    # Show requests while not logged in
    def test_show_requests_view_login_required(self):
        url = reverse("show_requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


###################
### ADD REQUEST ###
###################
class AddRequestViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123",
        )
        self.client.login(username="testuser", password="strongpassword123")
        self.project = Project.objects.create(project_name="TestProject")
        self.mouse1 = Mouse.objects.create(
            id=1, sex="M", dob=date.today(), genotyped=True, project=self.project
        )
        self.mouse2 = Mouse.objects.create(
            id=2, sex="F", dob=date.today(), genotyped=True, project=self.project
        )
        self.mice = [self.mouse1, self.mouse2]

    # GET RequestForm while logged in
    def test_add_request_get(self):
        url = reverse("add_request", args=[self.project.project_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)
        self.assertEqual(response.context["project_name"], self.project.project_name)

    # Get RequestForm while not logged in
    def test_add_request_get_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("add_request", args=[self.project.project_name])
        )
        url = reverse("add_request", args=[self.project.project_name])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    # POST RequestForm with valid data
    def test_add_request_post_valid(self):
        url = reverse("add_request", args=[self.project.project_name])
        data = {
            "task_type": "Cl",
            "mice": [self.mice[0].id, self.mice[1].id],
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


#######################
### CONFIRM REQUEST ###
#######################
class ConfirmRequestViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123",
        )
        self.client.login(username="testuser", password="strongpassword123")
        self.mouse = Mouse.objects.create(dob=date.today(), genotyped=False)
        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse)

    # User needs to be logged in
    def test_confirm_request_view_login_required(self):
        self.client.logout()
        response = self.client.get(
            reverse("confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('confirm_request', args=[self.request.request_id])}",
        )

    # Redirect to show_requests after confirming
    def test_confirm_request_view_get_request(self):
        response = self.client.get(
            reverse("confirm_request", args=[self.request.request_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("show_requests"))

    # Confirm request changes mice.genotyped to True
    def test_confirm_request_view_updates_request_status(self):
        self.client.get(reverse("confirm_request", args=[self.request.request_id]))
        self.request.refresh_from_db()
        self.assertTrue(self.request.confirmed)
        self.mouse.refresh_from_db()
        self.assertTrue(self.mouse.genotyped)


######################
### CREATE ACCOUNT ###
######################
class SignUpViewTest(TestCase):

    # GET CustomUseCreationrForm
    def test_signup_view_get_request(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    # POST valid data
    def test_signup_view_post_valid_data(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())

    # POST invalid data
    def test_signup_view_post_invalid_data(self):
        data = {
            "username": "",
            "email": "invalid_email",
            "password1": "weakpassword",
            "password2": "mismatchedpassword",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(CustomUser.objects.count(), 0)

    # Metadata
    def test_signup_view_attributes(self):
        self.assertEqual(SignUpView.form_class, CustomUserCreationForm)
        self.assertEqual(SignUpView.success_url, reverse_lazy("login"))
        self.assertEqual(SignUpView.template_name, "registration/signup.html")


#######################
### MICE REPOSITORY ###
#######################


class MiceRepositoryViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")

    # GET mice_repository while logged in
    def test_mice_repository_view_get_request(self):
        response = self.client.get(reverse("mice_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "repository/mice_repository.html")
        self.assertIn("mymice", response.context)

    # test for add mouse to repository
    def test_add_mouse_to_repository(self):
        response = self.client.get(reverse("add_mouse_to_repository"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "repository/add_mouse_to_repository.html")
        # self.assertIsInstance(response.context["form"], RepositoryMiceForm)

    # POST RequestForm with valid data
    # def test_add_mouse_to_repository_post_valid(self):
    #   data = {
