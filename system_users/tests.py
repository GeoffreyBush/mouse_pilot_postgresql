from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from system_users.forms import CustomUserChangeForm, CustomUserCreationForm
from system_users.models import CustomUser
from system_users.views import SignUpView
from test_factories.form_factories import CustomUserCreationFormFactory
from test_factories.model_factories import UserFactory


class CustomUserTest(TestCase):

    @classmethod
    def setUp(self):
        self.user = UserFactory(username="testuser", email="testuser@example.com")

    def test_user_creation(self):
        self.assertIsInstance(self.user, CustomUser)

    def test_user_correct_pk(self):
        self.assertEqual(self.user.pk, 1)

    def test_user_correct_username(self):
        self.assertEqual(self.user.username, "testuser")

    # Username top short

    # Username too long

    def test_user_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            UserFactory(username="testuser")

    def test_user_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            UserFactory(email="testuser@example.com")

    def test_password_minimum_length(self):
        with self.assertRaises(ValidationError):
            validate_password("short")

    # Password length too long

    def test_password_complexity(self):
        with self.assertRaises(ValidationError):
            validate_password("58472842931")

    def test_password_common(self):
        with self.assertRaises(ValidationError):
            validate_password("password")

    def test_password_similar_to_username(self):
        with self.assertRaises(ValidationError):
            validate_password("testuser", self.user)

    # Missing email

    # Email too short

    # Email too long

    # Incorrect email format


class CustomUserCreationFormTest(TestCase):

    def setUp(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data()
        )

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_min_username_length(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(username="1234")
        )
        self.assertIn("username", self.form.errors)

    def test_max_username_length(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                username="VeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongUsername"
            )
        )
        self.assertIn("username", self.form.errors)

    def test_empty_username(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(username=None)
        )
        self.assertIn("username", self.form.errors)

    def test_duplicate_username(self):
        UserFactory(username="testuser")
        form = CustomUserCreationForm(data=CustomUserCreationFormFactory.valid_data())
        self.assertIn("username", form.errors)

    def test_empty_password(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1=None, password2=None
            )
        )
        self.assertIn("password1", self.form.errors)
        self.assertIn("password2", self.form.errors)

    def test_min_password_length(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1="1234567", password2="1234567"
            )
        )
        self.assertIn("password1", self.form.errors)

    def test_max_password_length(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1="ijgAeiojg9Cg3490j9jfw09jfjf9j03$£%$Wr3wefi",
                password2="ijgAeiojg9Cg3490j9jfw09jfjf9j03$£%$Wr3wefi",
            )
        )
        self.assertIn("password1", self.form.errors)

    def test_password_mismatch(self):
        form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1="password1", password2="password2"
            )
        )
        self.assertIn("password2", form.errors)

    def test_empty_email(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(email=None)
        )
        self.assertIn("email", self.form.errors)

    def test_invalid_email(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(email="invalid_email")
        )
        self.assertIn("email", self.form.errors)

    # Email too short

    # Email too long


class CustomUserChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")

    def test_valid_data(self):
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "new@example.com"}
        )
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = CustomUserChangeForm(instance=self.user, data={})
        self.assertFalse(form.is_valid())

    # Username too short

    # Username too long

    # Password too short

    # Password too long

    def test_duplicate_username(self):
        UserFactory(username="newuser", email="old@example.com")
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "new@example.com"}
        )
        self.assertIn("username", form.errors)

    def test_invalid_email(self):
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "invalid_email"}
        )
        self.assertIn("email", form.errors)


class SignUpViewTest(TestCase):

    def setUp(self):
        self.valid_data = CustomUserCreationFormFactory.valid_data()

    def test_correct_form(self):
        self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    def test_get_request(self):
        response = self.client.get(reverse("system_users:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_post_valid_data(self):
        self.assertIsNone(CustomUser.objects.first())
        response = self.client.post(reverse("system_users:signup"), self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertIsNotNone(CustomUser.objects.first())

    def test_post_invalid_data(self):
        self.assertIsNone(CustomUser.objects.first())
        response = self.client.post(
            reverse("system_users:signup"),
            CustomUserCreationFormFactory.valid_data(username=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertTrue(response.context["form"].errors)
        self.assertIsNone(CustomUser.objects.first())

    # What if user is already logged in?


# Tests for each view associated with CustomUser: logout, password_reset, etc
