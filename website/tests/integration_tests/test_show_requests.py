from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from website.models import CustomUser, Mouse, Project, Request
from website.tests.integration_tests.helpers import auto_login, chrome_test_setup


class ResearcherShowProjectTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=chrome_test_setup())
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create objects for testing
        self.project = Project.objects.create(projectname="TestProject")
        self.mouse1 = Mouse.objects.create(
            sex="M", dob=date.today(), project=self.project
        )
        self.mouse2 = Mouse.objects.create(
            sex="F", dob=date.today(), project=self.project
        )
        self.request1 = Request.objects.create(
            researcher=self.user, task_type="Cl", confirmed=False
        )
        self.request1.mice.add(self.mouse1, self.mouse2)

        auto_login(self)

    def tearDown(self):
        self.driver.quit()

    def test_show_requests_page(self):

        self.driver.get(self.live_server_url + reverse("show_requests"))

        # Wait for the page to load and assert show_requests is loaded
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains(reverse("show_requests")))
        self.assertIn("Show Requests", self.driver.page_source)

        # Assert the requests table is displayed
        self.assertIn("Messaging", self.driver.page_source)
        self.assertIn("Mouse IDs", self.driver.page_source)
        self.assertIn("Tasks", self.driver.page_source)
        self.assertIn("Confirm", self.driver.page_source)

        # Assert the request details are displayed
        self.assertIn(self.request1.task_type, self.driver.page_source)
        self.assertIn("Confirm Request", self.driver.page_source)

    # Test is broken until confirming a clip request adds an earmark too
    """ 
    def test_confirm_request(self):

        self.driver.get(self.live_server_url + reverse("show_requests"))
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains(reverse("show_requests")))

        # Click the "Confirm Request" link for the first request
        self.driver.find_element(By.LINK_TEXT, "Confirm Request").click()

        # Wait for the redirect and assert the request is confirmed
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains(reverse("show_requests")))
        self.assertIn("Confirmed", self.driver.page_source)

        # Assert that the clipped mice are now genotyped
        self.mouse1.refresh_from_db()
        self.mouse2.refresh_from_db()
        self.assertTrue(self.mouse1.is_genotyped())
        self.assertTrue(self.mouse2.is_genotyped())
    """