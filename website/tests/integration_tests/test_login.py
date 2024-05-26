

"""
class LoginTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=chrome_test_setup())
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

    def tearDown(self):
        self.driver.quit()

    def test_successful_login(self):
        self.driver.get(self.live_server_url + reverse("login"))

        # Fill in the login form
        self.driver.find_element(By.ID, "id_username").send_keys("testuser")
        self.driver.find_element(By.ID, "id_password").send_keys("testpassword")
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Wait for the redirect and assert the user is logged in
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains(reverse("mice_repository")))
        self.assertIn("Research Home Page", self.driver.page_source)


# Integration tests should closely mirror client requirements
"""
