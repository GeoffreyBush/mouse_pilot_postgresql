import random
from datetime import date

from django.test import TestCase

from website.constants import EARMARK_CHOICES
from website.forms import (
    BreedingCageForm,
    BreedingPairForm,
    CommentForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    MouseSelectionForm,
    ProjectMiceForm,
    RequestForm,
)
from website.models import CustomUser, Mouse, Project, Strain


#################
### MICE FORM ###
#################
class ProjectMiceFormTestCase(TestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass", email="testemail@gmail.com"
        )
        self.project = Project.objects.create(projectname="TestProject")
        self.strain = Strain.objects.create(strain_name="Test Strain")

    # Valid data
    def test_mice_form_valid_data(self):
        form = ProjectMiceForm(
            data={
                "sex": "M",
                "dob": date.today(),
                "clippedDate": date.today(),

                "earmark": random.choice(EARMARK_CHOICES),
            }
        )
        self.assertTrue(form.is_valid())
        mouse = form.save()
        self.assertEqual(mouse.sex, "M")
        self.assertEqual(mouse.dob, date.today())
        self.assertEqual(mouse.clippedDate, date.today())
        self.assertTrue(mouse.is_genotyped())

    # Empty data
    def test_mice_form_empty_data(self):
        form = ProjectMiceForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("sex", form.errors)
        self.assertIn("dob", form.errors)

    # Invalid sex
    def test_mice_form_invalid_sex(self):
        form = ProjectMiceForm(
            data={
                "sex": "X",
                "dob": date.today(),
                "clippedDate": date.today(),
                "mother": None,
                "father": None,
                "project": self.project.projectname,
                "earmark": "ABCD",
                "genotyper": self.user.id,
                "strain": self.strain.strain_name,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("sex", form.errors)
        self.assertIn("earmark", form.errors)


####################
### COMMENT FORM ###
####################
class CommentFormTestCase(TestCase):
    def setUp(self):
        self.mouse = Mouse.objects.create(
            id=1, sex="M", dob=date.today()
        )

    # Valid data
    def test_comment_form_valid_data(self):
        form = CommentForm(data={"comment_text": "This is a test comment."})
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.comment = self.mouse
        comment.save()
        self.assertEqual(comment.comment_text, "This is a test comment.")
        self.assertEqual(comment.comment.id, self.mouse.id)

    # Exceed max length
    def test_comment_form_long_text(self):
        long_text = "A" * 501
        form = CommentForm(data={"comment_text": long_text})
        self.assertFalse(form.is_valid())
        self.assertIn("comment_text", form.errors)


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
                "password1": "testpass123",
                "password2": "testpass123",
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

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
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    # Valid data
    def test_custom_user_change_form_valid_data(self):
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
        CustomUser.objects.create_user(
            username="newuser", email="another@example.com", password="testpass123"
        )
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
        self.project1 = Project.objects.create(projectname="Project 1")
        self.project2 = Project.objects.create(projectname="Project 2")
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.mouse1 = Mouse.objects.create(
            id=1, sex="M", dob=date.today(), project=self.project1
        )
        self.mouse2 = Mouse.objects.create(
            id=2, sex="F", dob=date.today(), project=self.project1
        )
        self.mouse3 = Mouse.objects.create(
            id=3, sex="M", dob=date.today(), project=self.project2
        )

    # Valid data
    def test_request_form_valid_data(self):
        form = RequestForm(
            project=self.project1,
            data={
                "mice": [self.mouse1.id, self.mouse2.id],
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
            project=self.project1,
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


###########################
### MOUSE CHECKBOX FORM ###
###########################
class MouseSelectionFormTestCase(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(projectname="Project 1")
        self.project2 = Project.objects.create(projectname="Project 2")
        self.mouse1 = Mouse.objects.create(
            id=1, sex="M", dob=date.today(), project=self.project1
        )
        self.mouse2 = Mouse.objects.create(
            id=2, sex="F", dob=date.today(), project=self.project1
        )
        self.mouse3 = Mouse.objects.create(
            id=3, sex="M", dob=date.today(), project=self.project2
        )

    # Valid data
    def test_mouse_selection_form_valid_data(self):
        form = MouseSelectionForm(
            project=self.project1, data={"mice": [self.mouse1.id, self.mouse2.id]}
        )
        self.assertTrue(form.is_valid())
        self.assertCountEqual(form.cleaned_data["mice"], [self.mouse1, self.mouse2])

    # Project mismatch
    def test_mouse_selection_form_invalid_data(self):
        form = MouseSelectionForm(
            project=self.project1, data={"mice": [self.mouse1.id, self.mouse3.id]}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mice", form.errors)


##########################
### BREEDING PAIR FORM ###
##########################
class BreedingPairFormTest(TestCase):

    def setUp(self):
        self.father = Mouse.objects.create(
            id=1, sex="M", dob=date.today()
        )
        self.mother = Mouse.objects.create(
            id=2, sex="M", dob=date.today()
        )

    def test_valid_form(self):
        data = {
            "box_no": "1-1",
            "mother": self.mother,
            "father": self.father,
        }
        form = BreedingPairForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "mother": self.mother,
            "father": self.father,
        }
        form = BreedingPairForm(data=data)
        self.assertFalse(form.is_valid())


##########################
### BREEDING CAGE FORM ###
##########################
class BreedingCageFormTest(TestCase):

    def setUp(self):
        self.father = Mouse.objects.create(
            id=1, sex="M", dob=date.today()
        )
        self.mother = Mouse.objects.create(
            id=2, sex="M", dob=date.today()
        )

    # Valid data
    def test_valid_form(self):
        data = {
            "box_no": "1-1",
            "status": "Empty",
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
            "status": "Empty",
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
