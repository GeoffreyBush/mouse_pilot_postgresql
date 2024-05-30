from django.test import TestCase

from test_factories.form_factories import (
    CustomUserCreationFormFactory,
    RequestFormFactory,
)
from test_factories.model_factories import MouseFactory, ProjectFactory, UserFactory
from website.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    MouseSelectionForm,
    RequestForm,
)

# Rework ProjectMiceForm and show_project.html first before using this test
"""
#################
### MICE FORM ###
#################
class ProjectMiceFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.strain = StrainFactory()
        self.user = UserFactory()

    # Valid data
    def test_mice_form_valid_data(self):
        strain = StrainFactory()
        form = ProjectMiceForm(
            data={
                "sex": "M",
                "dob": date.today(),
                "clipped_date": date.today(),
                "mother": None,
                "father": None,
                "project": self.project.project_name,
                "earmark": random.choice(EARMARK_CHOICES),
                "genotyper": self.user.id,
                "strain": strain.strain_name,
            }
        )
        self.assertTrue(form.is_valid())
        mouse = form.save()
        self.assertEqual(mouse.sex, "M")
        self.assertEqual(mouse.dob, date.today())
        self.assertEqual(mouse.clipped_date, date.today())
        self.assertTrue(mouse.is_genotyped())

    # Empty data
    def test_mice_form_empty_data(self):
        form = ProjectMiceForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("sex", form.errors)
        self.assertIn("dob", form.errors)

    # Invalid sex
    def test_mice_form_invalid_data(self):
        form = ProjectMiceForm(
            data={
                "sex": "X",
                "dob": date.today(),
                "clipped_date": date.today(),
                "mother": None,
                "father": None,
                "project": self.project.project_name,
                "earmark": "ABCD",
                "genotyper": self.user.id,
                "strain": self.strain.strain_name,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("sex", form.errors)
        self.assertIn("earmark", form.errors)
"""


################################
### CUSTOMUSER CREATION FORM ###
################################
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



############################
### CUSTOMUSER EDIT FORM ###
############################
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


####################
### REQUEST FORM ###
####################
class RequestFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.mouse1, self.mouse2 = MouseFactory(project=self.project), MouseFactory(
            project=self.project
        )

    # Valid data
    def test_request_form_valid_data(self):
        form = RequestForm(
            project=self.project,
            data=RequestFormFactory.valid_data(self.mouse1, self.mouse2),
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.save().mice.count(), 2)

    # Invalid data
    def test_request_form_invalid_data(self):
        form = RequestForm(
            project=self.project,
            data=RequestFormFactory.missing_mice(),
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mice", form.errors)

    # There must be at least one mouse present in a request


############################
### MOUSE SELECTION FORM ###
############################
class MouseSelectionFormTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.mouse1, self.mouse2, self.mouse3 = (
            MouseFactory(project=self.project),
            MouseFactory(project=self.project),
            MouseFactory(),
        )

    # Valid data
    def test_mouse_selection_form_valid_data(self):
        form = MouseSelectionForm(
            project=self.project, data={"mice": [self.mouse1.pk, self.mouse2.pk]}
        )
        self.assertTrue(form.is_valid())
        self.assertCountEqual(form.cleaned_data["mice"], [self.mouse1, self.mouse2])

    # Project mismatch
    def test_mouse_selection_form_invalid_data(self):
        form = MouseSelectionForm(
            project=self.project, data={"mice": [self.mouse1.pk, self.mouse3.pk]}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mice", form.errors)


##########################
### BREEDING CAGE FORM ###
##########################
