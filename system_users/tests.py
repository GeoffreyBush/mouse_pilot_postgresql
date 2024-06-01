from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from system_users.forms import CustomUserCreationForm
from system_users.models import CustomUser
from system_users.views import SignUpView
from test_factories.form_factories import (
    CustomUserChangeFormFactory,
    CustomUserCreationFormFactory,
)
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

    def test_password_minimum_length_8(self):
        with self.assertRaises(ValidationError):
            validate_password("1_a4R-7")

    # Password length too long

    def test_password_complexity(self):
        with self.assertRaises(ValidationError):
            validate_password("58472842931")

    # make sure this is not password complexity
    def test_password_common(self):
        with self.assertRaises(ValidationError):
            validate_password("password")

    # make sure this is not password complexity
    def test_password_similar_to_username(self):
        # self.user = UserFactory(username="testuser")
        with self.assertRaises(ValidationError):
            validate_password("testuser", self.user)

    # Missing email

    # Email too short

    # Email too long

    # Incorrect email format


class CustomUserCreationFormTest(TestCase):

    def setUp(self):
        self.form = CustomUserCreationFormFactory.create()

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_min_username_length_5(self):
        self.form = CustomUserCreationFormFactory.create(username="bob")
        self.assertIn("username", self.form.errors)

    def test_max_username_length(self):
        self.form = CustomUserCreationFormFactory.create(
            username="VeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongUsername"
        )
        self.assertIn("username", self.form.errors)

    def test_empty_username(self):
        self.form = CustomUserCreationFormFactory.create(username=None)
        self.assertIn("username", self.form.errors)

    def test_duplicate_username(self):
        UserFactory(username="testuser")
        self.form = CustomUserCreationFormFactory.create()
        self.assertIn("username", self.form.errors)

    def test_empty_password(self):
        self.form = CustomUserCreationFormFactory.create(password1=None, password2=None)
        self.assertIn("password1", self.form.errors)
        self.assertIn("password2", self.form.errors)

    def test_min_password_length_8(self):
        self.form = CustomUserCreationFormFactory.create(
            password1="1_a4R-7", password2="1_a4R-7"
        )
        self.assertIn("password1", self.form.errors)

    def test_max_password_length(self):
        self.form = CustomUserCreationFormFactory.create(
            password1="ijgAeiojg9Cg3490j9jfw09jfjf9j03$£%$Wr3wefi",
            password2="ijgAeiojg9Cg3490j9jfw09jfjf9j03$£%$Wr3wefi",
        )
        self.assertIn("password1", self.form.errors)

    def test_password_mismatch(self):
        form = CustomUserCreationFormFactory.create(
            password1="w3-Fsw_rd1", password2="w2-Xsw_rd1"
        )
        self.assertIn("password2", form.errors)

    def test_empty_email(self):
        self.form = CustomUserCreationFormFactory.create(email=None)
        self.assertIn("email", self.form.errors)

    def test_invalid_email(self):
        self.form = CustomUserCreationFormFactory.create(email="invalid_email_format")
        self.assertIn("email", self.form.errors)

    # Email too short

    # Email too long


class CustomUserChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="old_user")
        self.form = CustomUserChangeFormFactory.create(self.user)

    def test_valid_data(self):

        self.assertTrue(self.form.is_valid())

    #  self.assertIn("username", self.form.errors)
    #

    # def test_empty_username(self):
    #   form = CustomUserChangeFormFactory.create(new_user=None, email=None)
    #  self.assertFalse(form.is_valid())

    # New username too short

    # New username too long

    # New password too short

    # New password too long

    # def test_duplicate_username(self):
    #   UserFactory(username="newuser", email="old@example.com")
    #  form = CustomUserChangeFormFactory.create(newuser="newuser")
    # self.assertIn("username", form.errors)

    def test_duplicate_email(self):
        pass

    # def test_invalid_email(self):
    #   form = CustomUserChangeForm(
    #      instance=self.user, data={"username": "newuser", "email": "invalid_email"}
    # )
    # self.assertIn("email", form.errors)


class CustomUserPasswordResetFormTest(TestCase):

    def setUp(self):
        pass


# Additional tests for other CustomUser forms


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


# Additional tests for each view associated with CustomUser: logout, password_reset, etc
