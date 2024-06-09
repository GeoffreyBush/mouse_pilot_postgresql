"""
class ResearcherShowProjectTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=chrome_test_setup())
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.project = Project.objects.create(project_name="TestProject")
        self.mouse1 = Mouse.objects.create(
            sex="M",
            dob=date.today(),
            project=self.project,
        )
        self.mouse2 = Mouse.objects.create(
            sex="F",
            dob=date.today(),
            project=self.project,
        )

        auto_login(self)

    def tearDown(self):
        self.driver.quit()

    def test_show_project_page(self):

        self.driver.get(
            self.live_server_url
            + reverse("show_project", args=[self.project.project_name])
        )

        # Wait for the page to load and assert the project name
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.url_contains(reverse("show_project", args=[self.project.project_name]))
        )
        self.assertIn(self.project.project_name, self.driver.page_source)

        # Assert the mice table is displayed
        self.assertIn("Mouse ID", self.driver.page_source)
        self.assertIn("Date of Birth", self.driver.page_source)
        self.assertIn("Sex", self.driver.page_source)
        self.assertIn("Earmark", self.driver.page_source)

        # Assert the mouse details are displayed
        self.assertIn(
            str(self.mouse1.dob.strftime("%B %d, %Y")), self.driver.page_source
        )
        self.assertIn(self.mouse1.sex, self.driver.page_source)
        self.assertIn(self.mouse1.earmark, self.driver.page_source)

        self.assertIn(
            str(self.mouse2.dob.strftime("%B %d, %Y")), self.driver.page_source
        )
        self.assertIn(self.mouse2.sex, self.driver.page_source)
        self.assertIn(self.mouse2.earmark, self.driver.page_source)

    def test_add_request(self):

        self.driver.get(
            self.live_server_url
            + reverse("show_project", args=[self.project.project_name])
        )

        # Select the first mouse
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="mice"]').click()

        # Click the "Add Request" button
        self.driver.find_element(
            By.CSS_SELECTOR, 'button[id="add-request-button"]'
        ).click()

        # Assert the user is redirected to the add request page
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.url_contains(reverse("add_request", args=[self.project.project_name]))
        )
        self.assertIn("Add Request", self.driver.page_source)
        # click the submit button

        # Assert that the request was created
"""

# Need to test MouseSelectionForm carried over to the add_request view.
# Could do a complete sequence from MouseSelect to AddRequest to confirm request
