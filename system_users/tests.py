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

    # User creation
    def test_user_creation(self):
        self.assertIsInstance(self.user, CustomUser)

    # Username top short

    # Username too long

    # Try to create a user with a duplicate username
    def test_user_with_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            UserFactory(username="testuser")

    # Try to create a user with a duplicate email
    def test_user_with_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            UserFactory(email="testuser@example.com")

    # Password length too short
    def test_password_length(self):
        with self.assertRaises(ValidationError):
            validate_password("short")

    # Password length too long

    # Password too simple
    def test_password_complexity(self):
        with self.assertRaises(ValidationError):
            validate_password("58472842931")

    # Password too common
    def test_password_common(self):
        with self.assertRaises(ValidationError):
            validate_password("password")

    # Password too similar to username
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

    # Valid data
    def test_custom_user_creation_form_valid_data(self):
        self.assertTrue(self.form.is_valid())

    # Username too short
    def test_custom_user_creation_form_short_username(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(username="1234")
        )
        self.assertIn("username", self.form.errors)

    # Username too long
    def test_custom_user_creation_form_long_username(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                username="12345678901234567890154354351234234"
            )
        )
        self.assertIn("username", self.form.errors)

    # Empty username
    def test_custom_user_creation_form_empty_username(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(username="")
        )
        self.assertIn("username", self.form.errors)

    # Duplicate username
    def test_custom_user_creation_form_duplicate_username(self):
        UserFactory(username="testuser")
        form = CustomUserCreationForm(data=CustomUserCreationFormFactory.valid_data())
        self.assertIn("username", form.errors)

    # Empty password
    def test_custom_user_creation_form_empty_password(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(password1="", password2="")
        )
        self.assertIn("password1", self.form.errors)
        self.assertIn("password2", self.form.errors)

    # Password too short
    def test_custom_user_creation_form_short_password(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1="1234567", password2="1234567"
            )
        )
        self.assertIn("password1", self.form.errors)

    # Password too long
    def test_custom_user_creation_form_long_password(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1="12345678901234567890154354351234234",
                password2="12345678901234567890154354351234234",
            )
        )
        self.assertIn("password1", self.form.errors)

    # Password mismatch
    def test_custom_user_creation_form_password_mismatch(self):
        form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(
                password1="password1", password2="password2"
            )
        )
        self.assertIn("password2", form.errors)

    # Empty email
    def test_custom_user_creation_form_empty_email(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(email="")
        )
        self.assertIn("email", self.form.errors)

    # Incorrect email format
    def test_custom_user_creation_form_invalid_email(self):
        self.form = CustomUserCreationForm(
            data=CustomUserCreationFormFactory.valid_data(email="invalid_email")
        )
        self.assertIn("email", self.form.errors)

    # Email too short

    # Email too long


class CustomUserChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")

    # Valid data
    def test_custom_user_change_form_valid_data(self):
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "new@example.com"}
        )
        self.assertTrue(form.is_valid())

    # Empty data
    def test_custom_user_change_form_empty_data(self):
        form = CustomUserChangeForm(instance=self.user, data={})
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)

    # Username too short

    # Username too long

    # Password too short

    # Password too long

    # Duplicate user
    def test_custom_user_change_form_duplicate_username(self):
        UserFactory(username="newuser", email="old@example.com")
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "new@example.com"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    # Invalid email
    def test_custom_user_change_form_invalid_email(self):
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "invalid_email"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class SignUpViewTest(TestCase):

    def setUp(self):
        self.valid_data = CustomUserCreationFormFactory.valid_data()

    # Correct form used
    def test_signup_view_attributes(self):
        self.assertEqual(SignUpView.form_class, CustomUserCreationForm)

    # GET CustomUseCreationrForm
    def test_signup_view_get_(self):
        response = self.client.get(reverse("system_users:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    # POST valid data
    def test_signup_view_post_valid_data(self):
        response = self.client.post(reverse("system_users:signup"), self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertIsNotNone(CustomUser.objects.first())

    # POST invalid data
    def test_signup_view_post_invalid_data(self):
        response = self.client.post(
            reverse("system_users:signup"),
            CustomUserCreationFormFactory.valid_data(username=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertTrue(response.context["form"].errors)


# Tests for each view associated with CustomUser: logout, password_reset, etc
