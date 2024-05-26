from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from website.tests.factories import UserFactory

from website.forms import (
    BreedingPairForm,
    CommentForm,
    CustomUserCreationForm,
    ProjectMiceForm,
    RequestForm,
)
from website.models import (
    BreedingCage,
    Comment,
    CustomUser,
    HistoricalMouse,
    Mouse,
    Project,
    Request,
    Strain,
)

class ResearcherDashboardViewTest(TestCase):

    # Create a test user and projects
    def setUp(self):
        self.user = UserFactory()
        self.project1 = Project.objects.create(project_name="TestProject1")
        self.project2 = Project.objects.create(project_name="TestProject2")

    # Access researcher dashboard logged in
    def test_researcher_dashboard_view_with_authenticated_user(self):
        self.client.login(username=self.user.username, password="testpassword")
        response = self.client.get(reverse("researcher_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.project1, response.context["myprojects"])
        self.assertIn(self.project2, response.context["myprojects"])
        self.assertEqual(self.project1.mice_count, 0)

    # Access the researcher dashboard view without logging in
    def test_researcher_dashboard_view_login_required(self):
        response = self.client.get(reverse("researcher_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("researcher_dashboard")}'
        )


####################
### SHOW PROJECT ###
####################
class ShowProjectViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.project = Project.objects.create(project_name="TestProject")

        # Add cage back in when experimental or stock cage is added to Mouse model
        """
        self.cage = Cage.objects.create(
            cageID=1, box_no="1-1", date_born=date.today(), date_wean=date.today()
        )
        """

        self.mouse1 = Mouse.objects.create(
            sex="M",
            dob=date.today(),
            genotyped=False,
            project=self.project,
            # cage=self.cage,
        )
        self.mouse2 = Mouse.objects.create(
            sex="F",
            dob=date.today(),
            genotyped=False,
            project=self.project,
            # cage=self.cage,
        )
        self.comment = Comment.objects.create(comment_id=1, comment_text="Test comment")
        self.request = Request.objects.create(researcher=self.user)

    # GET behaviour to show project
    def test_show_project_get(self):
        response = self.client.get(
            reverse("show_project", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "researcher/researcher_show_project.html")
        self.assertContains(response, self.project.project_name)
        self.assertIn("myproject", response.context)
        self.assertIn("mymice", response.context)
        self.assertIn("mycomment", response.context)
        self.assertIn("mice_ids_with_requests", response.context)
        self.assertIn("project_name", response.context)
        self.assertIn("filter", response.context)

    # POST MouseSelectionForm
    def test_show_project_post(self):
        response = self.client.post(
            reverse("add_request", args=[self.project.project_name])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")

    # Access non-existent project
    def test_show_non_existent_project(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("show_project", args=["AnyOtherName"]))

    # Access project without logging in
    def test_show_project_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("show_project", args=[self.project.project_name])
        )
        url = reverse("show_project", args=[self.project.project_name])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")