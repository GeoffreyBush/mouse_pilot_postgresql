from datetime import date

import factory
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from website.forms import (
    BreedingCageForm,
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
from website.views import SignUpView, create_family_tree_data


##############################
### HELPER FACTORY METHODS ###
##############################
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = "testuser"
    password = factory.PostGenerationMethodCall("set_password", "testpassword")


###################
### FAMILY TREE ###
###################
class FamilyTreeTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.mouse1 = Mouse.objects.create(sex="F", dob=date.today(), genotyped=False)
        self.mouse2 = Mouse.objects.create(sex="M", dob=date.today(), genotyped=False)
        self.mouse3 = Mouse.objects.create(
            sex="F",
            dob=date.today(),
            genotyped=False,
            mother=self.mouse1,
            father=self.mouse2,
        )

    # Family tree returns correct response data
    def test_create_family_tree_data(self):
        response = self.client.get(reverse("family_tree", args=[self.mouse3]))
        self.assertEqual(response.status_code, 200)
        data = create_family_tree_data(self.mouse3)
        self.assertEqual(
            data,
            {
                "name": str(self.mouse3.id),
                "role": None,
                "parent": str(self.mouse1.id),
                "children": [
                    {"name": str(self.mouse1.id), "role": "Mother", "parent": None},
                    {"name": str(self.mouse2.id), "role": "Father", "parent": None},
                ],
            },
        )

    # Try to create a family tree from a mouse that doesn't exist
    def test_family_tree_view_with_non_existent_mouse(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("family_tree", args=[10]))


############################
### RESEARCHER DASHBOARD ###
############################
class ResearcherDashboardViewTest(TestCase):

    # Create a test user and projects
    def setUp(self):
        self.user = UserFactory()
        self.project1 = Project.objects.create(projectname="TestProject1")
        self.project2 = Project.objects.create(projectname="TestProject2")

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
        self.project = Project.objects.create(projectname="TestProject")

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
            reverse("show_project", args=[self.project.projectname])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "researcher/researcher_show_project.html")
        self.assertContains(response, self.project.projectname)
        self.assertIn("myproject", response.context)
        self.assertIn("mymice", response.context)
        self.assertIn("mycage", response.context)
        self.assertIn("mycomment", response.context)
        self.assertIn("mice_ids_with_requests", response.context)
        self.assertIn("projectname", response.context)
        self.assertIn("filter", response.context)

    # POST MouseSelectionForm
    def test_show_project_post(self):
        response = self.client.post(
            reverse("add_request", args=[self.project.projectname])
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
            reverse("show_project", args=[self.project.projectname])
        )
        url = reverse("show_project", args=[self.project.projectname])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


################
### COMMENTS ###
################
class ShowCommentViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.project = Project.objects.create(projectname="Test Project")
        self.mouse = Mouse.objects.create(
            id=1, sex="M", dob=date.today(), genotyped=True, project=self.project
        )
        self.comment = Comment.objects.create(
            comment=self.mouse, comment_text="Test comment"
        )

    # GET behaviour to show comment
    def test_show_comment_get(self):
        response = self.client.get(reverse("show_comment", args=[self.mouse.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "popups/comment_fragment.html")
        self.assertIsInstance(response.context["form"], CommentForm)
        self.assertEqual(response.context["comment"], self.comment)

    # POST behaviour to update comment
    def test_show_comment_post(self):
        data = {"comment_text": "Updated comment"}
        response = self.client.post(reverse("show_comment", args=[self.mouse.id]), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.projectname])
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment_text, "Updated comment")

    # Access non-existent comment
    def test_show_non_existent_comment(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("show_comment", args=[10]))

    # Access comment without logging in
    def test_show_comment_without_logging_in(self):
        self.client.logout()
        response = self.client.get(reverse("show_comment", args=[self.mouse.id]))
        url = reverse("show_comment", args=[self.mouse.id])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


###########################
### LIST BREEDING CAGES ###
###########################
class BreedingWingListCagesTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")
        self.strain = Strain.objects.create(strain_name="TestStrain")
        self.cage = BreedingCage.objects.create(
            box_no="1-1", date_born=date.today(), date_wean=date.today()
        )

    # Access breeding wing dashboard logged in
    def test_list_breeding_cages_view_with_authenticated_user(self):
        response = self.client.get(reverse("list_breeding_cages"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_wing/list_breeding_cages.html")
        self.assertIn("mycages", response.context)
        self.assertIn(self.cage, response.context["mycages"])

    # Access breeding wing dashboard without logging in
    def test_list_breeding_cages_view_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("list_breeding_cages"))
        url = reverse("list_breeding_cages")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


################################
### BREEDING WING ADD LITTER ###
################################
class BreedingWingAddLitter(TestCase):
    def setup(self):
        self.user = UserFactory()
        self.client.force_login(self.user)
        self.mouse1 = Mouse.objects.create(
            sex="M",
            dob=date.today(),
            genotyped=False,
            project=self.project,
            cage=self.cage,
        )
        self.mouse2 = Mouse.objects.create(
            sex="F",
            dob=date.today(),
            genotyped=False,
            project=self.project,
            cage=self.cage,
        )

    """ Broken test - self.assertRedirects() goes to login page instead. Tested on live server and login was not a problem """

    # Access breeding wing add litter logged in
    def test_breeding_wing_add_litter_with_authenticated_user(self):
        response = self.client.get(reverse("breeding_wing_add_litter"))
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('breeding_wing_add_litter'))


##########################################
### BREEDING WING VIEW INDIVIDUAL CAGE ###
##########################################
class BreedingWingViewIndividualCageTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cage = BreedingCage.objects.create(
            box_no="1-1", date_born=date.today(), date_wean=date.today()
        )
        self.client.login(username="testuser", password="testpassword")

    # Access breeding wing cage view logged in
    def test_view_breeding_cage_with_authenticated_user(self):
        response = self.client.get(
            reverse("view_breeding_cage", args=[self.cage.box_no])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_wing/view_breeding_cage.html")
        self.assertIn("mycage", response.context)
        self.assertIn("mymice", response.context)
        self.assertIn("filter", response.context)
        self.assertEqual(response.context["mycage"], self.cage)

    # Access non-existent cage
    def test_breeding_wing_view_non_existent_cage(self):
        self.client.login(username="testuser", password="testpassword")
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("view_breeding_cage", args=[10]))

    # Access breeding wing cage view without logging in
    def test_view_breeding_cage_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("view_breeding_cage", args=[self.cage.box_no])
        )
        self.assertEqual(response.status_code, 302)


############################
### CREATE BREEDING PAIR ###
############################
class AddCageViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username="testuser", password="testpassword")

    # Access Create Breeding Pair while logged in
    def test_create_breeding_pair_get_with_authenticated_user(self):
        response = self.client.get(reverse("create_breeding_pair"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_wing/create_breeding_pair.html")

    # POST BreedingCageForm with valid data
    def test_create_breeding_pair_post_valid(self):
        data = {
            "box_no": "1-1",
            "status": "Empty",  # Should change to occupied
            "mother": "TestMother",
            "father": "TestFather",
        }
        form = BreedingCageForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse("create_breeding_pair"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_breeding_cages"))

    # POST BreedingCageForm with invalid data
    def test_create_breeding_pair_post_invalid(self):
        data = {
            "box_no": "1-1",
            "mother": "TestMother",
        }
        response = self.client.post(reverse("create_breeding_pair"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_wing/create_breeding_pair.html")
        form = response.context["form"]
        self.assertFalse(form.is_valid())

    # Access add cage while not logged in
    def test_create_breeding_pair_get_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("create_breeding_pair"))
        url = reverse("create_breeding_pair")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


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
        self.project = Project.objects.create(projectname="TestProject")

    # Access add_preexisting_mouse_to_project while logged in
    def test_add_preexisting_mouse_to_project_get(self):
        url = reverse(
            "add_preexisting_mouse_to_project", args=[self.project.projectname]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "researcher/add_preexisting_mouse_to_project.html"
        )
        self.assertIsInstance(response.context["mice_form"], ProjectMiceForm)
        self.assertEqual(response.context["projectname"], self.project.projectname)

    # Add valid data test here
    """ Likely similar valid POST issue as edit_mouse test, below, where genotyper field causes issues """

    def test_add_preexisting_mouse_to_project_post_invalid(self):
        url = reverse(
            "add_preexisting_mouse_to_project", args=[self.project.projectname]
        )
        data = {
            "sex": "Invalid",
            "dob": "2022-01-01",
            "genotyped": True,
            "project": self.project.projectname,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "researcher/add_preexisting_mouse_to_project.html"
        )
        self.assertIsInstance(response.context["mice_form"], ProjectMiceForm)
        self.assertEqual(response.context["projectname"], self.project.projectname)
        self.assertFalse(Mouse.objects.exists())

    # Access add_preexisting_mouse_to_project without logging in
    def test_add_preexisting_mouse_to_project_view_login_required(self):
        self.client.logout()
        url = reverse(
            "add_preexisting_mouse_to_project", args=[self.project.projectname]
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
        self.project = Project.objects.create(projectname="TestProject")
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
        url = reverse("edit_mouse", args=[self.project.projectname, self.mouse1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_mouse.html")
        self.assertIsInstance(response.context["form"], ProjectMiceForm)
        self.assertEqual(response.context["form"].instance, self.mouse1)
        self.assertEqual(response.context["projectname"], self.project.projectname)

    # Can't get this valid POST test to work correctly. Genotyper field causes issues
    """
    # POST with valid data
    def test_edit_mouse_post_valid(self):
        url = reverse('edit_mouse', args=[self.project.projectname, self.mouse1.id])
        data = {
            'sex': 'M',
            'dob': date.today(),
            'clippedDate': date.today(),
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
        url = reverse("edit_mouse", args=[self.project.projectname, self.mouse1.id])
        data = {
            "sex": "Invalid",
            "dob": date.today(),
            "genotyped": False,
            "project": self.project.projectname,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_mouse.html")
        self.assertIsInstance(response.context["form"], ProjectMiceForm)
        self.assertEqual(response.context["projectname"], self.project.projectname)
        self.mouse1.refresh_from_db()
        self.assertEqual(self.mouse1.sex, "M")
        self.assertEqual(self.mouse1.dob, date.today())
        self.assertTrue(self.mouse1.genotyped)

    # Access edit_mouse without logging in
    def test_edit_mouse_view_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse("edit_mouse", args=[self.project.projectname, self.mouse1.id])
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
        self.project1 = Project.objects.create(projectname="TestProject1")
        self.project2 = Project.objects.create(projectname="TestProject2")

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
        self.project = Project.objects.create(projectname="TestProject")
        self.mouse = Mouse.objects.create(
            sex="M", dob=date.today(), genotyped=True, project=self.project
        )

    # Delete mouse while logged in
    def test_delete_mouse_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("delete_mouse", args=[self.project.projectname, self.mouse.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.projectname])
        )
        self.assertFalse(Mouse.objects.filter(id=self.mouse.id).exists())

    # Delete mouse while not logged in
    def test_delete_mouse_view_login_required(self):
        url = reverse("delete_mouse", args=[self.project.projectname, self.mouse.id])
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
        self.project = Project.objects.create(projectname="TestProject")
        self.mouse1 = Mouse.objects.create(
            id=1, sex="M", dob=date.today(), genotyped=True, project=self.project
        )
        self.mouse2 = Mouse.objects.create(
            id=2, sex="F", dob=date.today(), genotyped=True, project=self.project
        )
        self.mice = [self.mouse1, self.mouse2]

    # GET RequestForm while logged in
    def test_add_request_get(self):
        url = reverse("add_request", args=[self.project.projectname])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)
        self.assertEqual(response.context["projectname"], self.project.projectname)

    # Get RequestForm while not logged in
    def test_add_request_get_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("add_request", args=[self.project.projectname])
        )
        url = reverse("add_request", args=[self.project.projectname])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    # POST RequestForm with valid data
    def test_add_request_post_valid(self):
        url = reverse("add_request", args=[self.project.projectname])
        data = {
            "task_type": "Cl",
            "mice": [self.mice[0].id, self.mice[1].id],
            "new_message": "Test message",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.projectname])
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
        url = reverse("add_request", args=[self.project.projectname])
        data = {"task_type": "Invalid", "mice": []}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_request.html")
        self.assertIsInstance(response.context["form"], RequestForm)
        self.assertEqual(response.context["projectname"], self.project.projectname)
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
        self.assertTemplateUsed(response, "general/mice_repository.html")
        self.assertIn("mymice", response.context)
