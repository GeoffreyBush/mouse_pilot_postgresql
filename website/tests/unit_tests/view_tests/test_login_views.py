from django.test import TestCase
from django.urls import reverse, reverse_lazy

from website.forms import CustomUserCreationForm
from website.models import CustomUser
from website.views import SignUpView

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