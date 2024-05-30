from django.test import TestCase
from django.urls import reverse

from test_factories.form_factories import CustomUserCreationFormFactory
from website.forms import CustomUserCreationForm
from website.models import CustomUser
from website.views import SignUpView


class SignUpViewTest(TestCase):

    def setUp(self):
        self.valid_data = CustomUserCreationFormFactory.valid_data()
        self.invalid_data = CustomUserCreationFormFactory.valid_data(username=None)

    # Correct form used
    def test_signup_view_attributes(self):
        self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    # GET CustomUseCreationrForm
    def test_signup_view_get_(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    # POST valid data
    def test_signup_view_post_valid_data(self):
        response = self.client.post(reverse("signup"), self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertIsNotNone(CustomUser.objects.first())

    # POST invalid data
    def test_signup_view_post_invalid_data(self):
        response = self.client.post(reverse("signup"), self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertTrue(response.context["form"].errors)
