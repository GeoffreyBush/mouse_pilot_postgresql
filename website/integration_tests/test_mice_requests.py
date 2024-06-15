import chromedriver_autoinstaller
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mouse_pilot_postgresql.model_factories import UserFactory
from website.integration_tests.utils import options

chromedriver_autoinstaller.install()


class MiceRequestIntegrationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=options())
        self.user = UserFactory()

    def tearDown(self):
        connections.close_all()
        self.driver.quit()

    def test_create_request(self):

        self.driver.get(self.live_server_url + reverse("login"))
        username_field = self.driver.find_element(By.ID, "id_username")
        username_field.send_keys(self.user.username)
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("testpassword")
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains(reverse("projects:list_projects")))
        assert "Projects List" == self.driver.title
