from django.test import TestCase
from django.urls import reverse

from website.models import Mouse
from website.tests.model_factories import MouseFactory, ProjectFactory, UserFactory

"""
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
    #Likely similar valid POST issue as edit_mouse test, below, where genotyper field causes issues

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
            reverse("delete_mouse", args=[self.project.project_name, self.mouse.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("show_project", args=[self.project.project_name])
        )
        self.assertIsNone(Mouse.objects.first())

    # Delete mouse while not logged in
    def test_delete_mouse_view_unauthenticated_user(self):
        self.client.logout()
        url = reverse("delete_mouse", args=[self.project.project_name, self.mouse.pk])
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
