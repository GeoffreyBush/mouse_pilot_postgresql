from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from website.models import CustomUser, Mouse, Project
from website.tests.integration_tests.helpers import auto_login, chrome_test_setup


class ResearcherShowProjectTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=chrome_test_setup())
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.project = Project.objects.create(projectname="TestProject")
        self.mouse1 = Mouse.objects.create(
            sex="M",
            dob=date.today(),
            genotyped=True,
            project=self.project,
        )
        self.mouse2 = Mouse.objects.create(
            sex="F",
            dob=date.today(),
            genotyped=False,
            project=self.project,
        )

        auto_login(self)

    def tearDown(self):
        self.driver.quit()

    def test_show_project_page(self):

        self.driver.get(
            self.live_server_url
            + reverse("show_project", args=[self.project.projectname])
        )

        # Wait for the page to load and assert the project name
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.url_contains(reverse("show_project", args=[self.project.projectname]))
        )
        self.assertIn(self.project.projectname, self.driver.page_source)

        # Assert the mice table is displayed
        self.assertIn("Mouse ID", self.driver.page_source)
        self.assertIn("Genotyped", self.driver.page_source)
        self.assertIn("Date of Birth", self.driver.page_source)
        self.assertIn("Sex", self.driver.page_source)
        self.assertIn("Earmark", self.driver.page_source)

        # Assert the mouse details are displayed
        self.assertIn(str(self.mouse1.genotyped), self.driver.page_source)
        self.assertIn(
            str(self.mouse1.dob.strftime("%B %d, %Y")), self.driver.page_source
        )
        self.assertIn(self.mouse1.sex, self.driver.page_source)
        self.assertIn(self.mouse1.earmark, self.driver.page_source)

        self.assertIn(str(self.mouse2.genotyped), self.driver.page_source)
        self.assertIn(
            str(self.mouse2.dob.strftime("%B %d, %Y")), self.driver.page_source
        )
        self.assertIn(self.mouse2.sex, self.driver.page_source)
        self.assertIn(self.mouse2.earmark, self.driver.page_source)

    def test_add_request(self):

        self.driver.get(
            self.live_server_url
            + reverse("show_project", args=[self.project.projectname])
        )

        # Select the first mouse
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="mice"]').click()

        # Click the "Add Request" button
        self.driver.find_element(
            By.CSS_SELECTOR, 'button[id="add-request-button"]'
        ).click()

        # Wait for the redirect and assert the request was created
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.url_contains(reverse("add_request", args=[self.project.projectname]))
        )
        self.assertIn("Add Request", self.driver.page_source)
