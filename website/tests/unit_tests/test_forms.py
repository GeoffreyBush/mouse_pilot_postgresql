import random
from datetime import date

from django.test import TestCase

from website.constants import EARMARK_CHOICES
from website.forms import (
    BreedingCageForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    MouseSelectionForm,
    ProjectMiceForm,
    RequestForm,
)
from website.models import CustomUser
from website.tests.factories import (
    MouseFactory,
    ProjectFactory,
    StrainFactory,
    UserFactory,
)


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


################################
### CUSTOMUSER CREATION FORM ###
################################
class CustomUserCreationFormTestCase(TestCase):

    # Valid data
    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword"))

    # Empty form
    def test_custom_user_creation_form_empty_data(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)

    # Password mismatch
    def test_custom_user_creation_form_password_mismatch(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpass123",
                "password2": "wrongpass",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    # Duplicate user
    def test_custom_user_creation_form_duplicate_username(self):
        CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "another@example.com",
                "password1": "testpass123",
                "password2": "testpass123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


############################
### CUSTOMUSER EDIT FORM ###
############################
class CustomUserChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")

    # Valid data
    def test_custom_user_change_form_valid_data(self):
        self.assertEqual(self.user.username, "testuser")
        form = CustomUserChangeForm(
            instance=self.user, data={"username": "newuser", "email": "new@example.com"}
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "new@example.com")

    # Empty data
    def test_custom_user_change_form_empty_data(self):
        form = CustomUserChangeForm(instance=self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    # Duplicate user
    def test_custom_user_change_form_duplicate_username(self):
        UserFactory(username="newuser")
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
        self.user = UserFactory()
        self.mouse1, self.mouse2 = MouseFactory(project=self.project), MouseFactory(
            project=self.project
        )

    # Valid data
    def test_request_form_valid_data(self):
        form = RequestForm(
            project=self.project,
            data={
                "mice": [self.mouse1.pk, self.mouse2.pk],
                "task_type": "Cl",
                "researcher": self.user.id,
                "new_message": "Test message",
            },
        )
        self.assertTrue(form.is_valid())
        request = form.save()
        self.assertEqual(request.task_type, "Cl")
        self.assertEqual(request.researcher.id, self.user.id)
        self.assertEqual(request.new_message, "Test message")
        self.assertCountEqual(list(request.mice.all()), [self.mouse1, self.mouse2])

    # Invalid data
    def test_request_form_invalid_data(self):
        form = RequestForm(
            project=self.project,
            data={
                "mice": [],
                "task_type": "Invalid",
                "researcher": self.user.id,
                "new_message": "Test message",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mice", form.errors)
        self.assertIn("task_type", form.errors)


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
class BreedingCageFormTest(TestCase):

    def setUp(self):
        self.father, self.mother = MouseFactory(sex="M"), MouseFactory(sex="F")

    # Valid data
    def test_valid_form(self):
        data = {
            "box_no": "1-1",
            "mother": self.mother,
            "father": self.father,
            "date_born": date.today(),
            "number_born": "5",
            "cull_to": "2",
            "date_wean": date.today(),
            "number_wean": "3",
            "pwl": "2",
        }
        form = BreedingCageForm(data=data)
        self.assertTrue(form.is_valid())

    # Missing cage number
    def test_invalid_form(self):
        data = {
            "box_no": "",
            "mother": self.mother,
            "father": self.father,
            "date_born": date.today(),
            "number_born": "5",
            "cull_to": "2",
            "date_wean": date.today(),
            "number_wean": "3",
            "pwl": "2",
        }
        form = BreedingCageForm(data=data)
        self.assertFalse(form.is_valid())
