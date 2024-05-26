from datetime import date

from django.test import TestCase
from django.urls import reverse, reverse_lazy

from website.forms import CustomUserCreationForm
from website.models import CustomUser, Mouse, Request
from website.tests.factories import UserFactory
from website.views import SignUpView


#######################
### CONFIRM REQUEST ###
#######################



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
