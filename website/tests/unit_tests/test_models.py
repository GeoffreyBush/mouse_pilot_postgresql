import random
from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from website.constants import EARMARK_CHOICES_PAIRED
from website.models import (
    BreedingCage,
    Comment,
    CustomUser,
    Mouse,
    Project,
    Request,
    Strain,
)


############
### MICE ###
############
class MiceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Create foreign keys

        # Add cage back in when stock or experimental cage is added to Mouse model
        """
        cage = Cage.objects.create(date_born=date.today(), date_wean=date.today())
        """

        project = Project.objects.create(projectname="Test Project")
        earmark = random.choice(EARMARK_CHOICES_PAIRED)
        strain = Strain.objects.create(strain_name="Strain1")

        # Create some Mouse objects for testing
        Mouse.objects.create(
            sex="M",
            dob=date.today(),
            genotyped=True,
            project=project,
            earmark=earmark,
            strain=strain,
        )
        Mouse.objects.create(
            sex="F", dob=date.today(), clippedDate=date.today(), genotyped=False
        )

    # String method
    def test_mice_str_method(self):
        mice = Mouse.objects.first()
        self.assertEqual(str(mice), str(mice.id), "Mouse .str() method is incorrect")

    # Only male or female
    def test_mice_sex_choices(self):
        mice = Mouse.objects.first()
        self.assertIn(
            mice.sex,
            ["M", "F"],
            "Sex attribute of Mouse was able to be something other than 'M' or 'F'",
        )

    # DOB must exist
    def test_mice_dob_not_null(self):
        mice = Mouse.objects.first()
        self.assertIsNotNone(mice.dob, "Mouse model instance without a date of birth")

    # Clipped date can be blank
    def test_mice_clippedDate_blank(self):
        mice = Mouse.objects.first()
        self.assertIsNone(
            mice.clippedDate, "Clipped date was not able to be set to null"
        )

    # Genotyped not null
    def test_mice_genotyped_not_null(self):
        mice = Mouse.objects.first()
        self.assertIsNotNone(
            mice.genotyped,
            "Genotyped attribute for Mouse should not be able to be null",
        )

    # Add cage back in when stock or experimental cage is added to Mouse model
    """
    # Cage key exists
    def test_mice_cage_id_key(self):
        mice = Mouse.objects.first()
        self.assertIsNotNone(mice.cage_id, "Cage foreign key in Mouse does not exist")
    """

    # Project key exists
    def test_mice_project_key(self):
        mice = Mouse.objects.first()
        self.assertIsNotNone(
            mice.project, "Project foreign key in Mouse does not exist"
        )

    # Strain key exists
    def test_mice_strain_foreign_key(self):
        mice = Mouse.objects.first()
        self.assertIsNotNone(mice.strain, "Strain foreign key in Mouse does not exist")

    # Earmark exists
    def test_mice_earmark_foreign_key(self):
        mice = Mouse.objects.first()
        self.assertIsNotNone(mice.earmark, "Earmark in Mouse does not exist")


##################
### CUSTOMUSER ###
##################
class CustomUserTest(TestCase):

    @classmethod
    # Create test user
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    # User can be created
    def test_user_creation(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.password, "testpassword")

    # String method
    def test_user_str_method(self):
        self.assertEqual(
            str(self.user), "testuser", "CustomUser .str() method is incorrect"
        )

    # DB table name
    def test_user_table_name(self):
        self.assertEqual(
            CustomUser._meta.db_table, "user", "CustomUser table name mismatch"
        )

    # Managed by Django
    def test_user_is_managed(self):
        self.assertTrue(self.user._meta.managed)

    # No duplicate users
    def test_user_with_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(
                username="testuser",
                email="anotheruser@example.com",
                password="testpassword",
            )


###############
### REQUEST ###
###############


class RequestModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123",
        )
        self.mouse1 = Mouse.objects.create(dob=date.today(), genotyped=False)
        self.mouse2 = Mouse.objects.create(dob=date.today(), genotyped=False)
        self.request = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request.mice.add(self.mouse1, self.mouse2)

    # Request creation
    def test_request_creation(self):
        self.assertEqual(self.request.request_id, 1)
        self.assertEqual(self.request.researcher, self.user)
        self.assertEqual(self.request.task_type, "Cl")
        self.assertFalse(self.request.confirmed)
        self.assertIsNone(self.request.new_message)
        self.assertIsNone(self.request.message_history)

    # Confirm method
    def test_request_confirm(self):
        self.assertFalse(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertFalse(mouse.genotyped)

        self.request.confirm()

        self.request.refresh_from_db()
        for mouse in self.request.mice.all():
            mouse.refresh_from_db()

        self.assertTrue(self.request.confirmed)
        for mouse in self.request.mice.all():
            self.assertTrue(mouse.genotyped)

    # Str method
    def test_request_string_representation(self):
        self.assertEqual(str(self.request), "1")


##############
### STRAIN ###
##############
class StrainTestCase(TestCase):

    @classmethod
    # Initial Strain
    def setUpTestData(cls):
        Strain.objects.create(strain_name="CRE1")

    # String method
    def test_strain_str_method(self):
        strain = Strain.objects.get(strain_name="CRE1")
        self.assertEqual(str(strain), "CRE1", "Strain .str() method is incorrect")

    # Primary key
    def test_strain_primary_key(self):
        self.assertTrue(
            Strain._meta.get_field("strain_name").primary_key,
            "Primary key for 'strain' is not set",
        )

    # DB table name
    def test_strain_table_name(self):
        self.assertEqual(Strain._meta.db_table, "strain", "Strain table name mismatch")

    # Creation
    def test_strain_creation(self):
        strain = Strain.objects.create(strain_name="FLOX")
        self.assertIsInstance(
            strain, Strain, "Created strain was somehow not an instance of Strain model"
        )
        self.assertEqual(
            strain.strain_name, "FLOX", "strain_name mismatch in Strain creation"
        )

    # Uniqueness
    def test_strain_uniqueness(self):
        with self.assertRaises(Exception):
            Strain.objects.create(strain_name="CRE1")


############
### CAGE ###
############
class BreedingCageModelTest(TestCase):

    @classmethod
    # Initial Cage
    def setUp(self):
        self.cage = BreedingCage.objects.create(
            box_no="1-1",
            status="Empty",
            date_born=date.today(),
            number_born="5",
            date_wean=date.today(),
            number_wean="4",
            pwl="PWL1",
        )

    # Cage creation
    def test_cage_creation(self):
        self.assertIsInstance(self.cage, BreedingCage)
        self.assertEqual(self.cage.box_no, "1-1")
        self.assertEqual(self.cage.status, "Empty")
        self.assertEqual(self.cage.date_born, date.today())
        self.assertEqual(self.cage.number_born, "5")
        self.assertEqual(self.cage.date_wean, date.today())
        self.assertEqual(self.cage.number_wean, "4")
        self.assertEqual(self.cage.pwl, "PWL1")

    # String method
    def test_cage_str(self):
        self.assertEqual(
            str(self.cage), str(self.cage.box_no), "Cage .str() method is incorrect"
        )

    # Primary key
    def test_cage_key(self):
        self.assertTrue(
            BreedingCage._meta.get_field("box_no").primary_key,
            "Primary key for 'cage' is not set",
        )

    # Managed by Django
    def test_cage_is_managed(self):
        self.assertTrue(self.cage._meta.managed, "Cage is not managed by Django")

    # DB table name
    def test_cage_table(self):
        self.assertEqual(
            BreedingCage._meta.db_table, "breedingcage", "Cage table name mismatch"
        )

    # IntegrityError with missing attributes


###############
### PROJECT ###
###############
class ProjectModelTest(TestCase):

    @classmethod
    # Initial Project
    def setUpTestData(cls):
        strain1 = Strain.objects.create(strain_name="FLOX")
        strain2 = Strain.objects.create(strain_name="CMV")
        user1 = CustomUser.objects.create(
            username="TestUser1", password="testpassword", email="testemail1@test.com"
        )
        user2 = CustomUser.objects.create(
            username="TestUser2", password="testpassword", email="testemail2@test.com"
        )
        project = Project.objects.create(
            projectname="TestName",
            researcharea="TestArea",
        )
        project.strains.add(strain1, strain2)
        project.researchers.add(user1, user2)

    # Creation
    def test_project_creation(self):
        project = Project.objects.create(projectname="TestName2", researcharea="Flu")
        self.assertIsInstance(project, Project, "Project creation failed.")

    # String method
    def test_project_str(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(
            str(project), "TestName", "Project .str() method is incorrect."
        )

    # Primary key
    def test_project_key(self):
        self.assertTrue(
            Project._meta.get_field("projectname").primary_key,
            "Primary key for 'projectname' is not set.",
        )

    # Research area
    def test_project_area(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(project.researcharea, "TestArea")

    # DB table name
    def test_project_table(self):
        self.assertEqual(
            Project._meta.db_table, "project", "Project table name mismatch."
        )

    # Strains many-to-many
    def test_project_strains(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(
            project.strains.count(),
            2,
            "Incorrect number of strains associated with the project.",
        )

    # Researchers many-to-many
    def test_project_researchers(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(
            project.researchers.count(),
            2,
            "Incorrect number of researchers associated with the project.",
        )

    # Mouse count
    def test_project_mice_count(self):
        project = Project.objects.get(projectname="TestName")
        self.assertEqual(project.mice_count, 0)
        project.mice_count += 1
        self.assertEqual(project.mice_count, 1)


###############
### COMMENT ###
###############


class CommentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        mice = Mouse.objects.create(sex="M", dob=date.today(), genotyped=True)
        Comment.objects.create(comment=mice, comment_text="Mouse has long nails")

    # String method
    def test_comment_str_method(self):
        comment = Comment.objects.first()
        self.assertEqual(str(comment), "1", "Comment .str() method is incorrect")

    # Primary key
    def test_comment_primary_key(self):
        self.assertTrue(
            Comment._meta.get_field("comment").primary_key,
            "Primary key for 'comment' is not set",
        )

    # DB table name
    def test_comment_table_name(self):
        self.assertEqual(
            Comment._meta.db_table, "comment", "Comment table name mismatch"
        )

    # Creation
    def test_comment_creation(self):
        comment = Comment.objects.first()
        self.assertIsInstance(comment, Comment)
        self.assertEqual(
            comment.comment_text, "Mouse has long nails", "Comment creation failed"
        )


# - I think these two lines below make tests run on mouse_stocks.csv instead of mouse test cases here.
# - Useful to know and could be used to split tests into imagined data for simpler tests (does class exist, does it have correct properties)
# - and real data tests (do all mice have either M/F sex? do all have DOB? etc.)

# suite = unittest.TestLoader().loadTestsFromTestCase(MiceModelTest)
# unittest.TextTestRunner(verbosity=2).run(suite)
