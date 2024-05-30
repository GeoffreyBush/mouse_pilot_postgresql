from django.urls import reverse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Configure options for Chrome
def chrome_test_setup():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    return chrome_options


# Login to dashboard
def auto_login(test):
    test.driver.get(test.live_server_url + reverse("login"))
    test.driver.find_element(By.ID, "id_username").send_keys("testuser")
    test.driver.find_element(By.ID, "id_password").send_keys("testpassword")
    test.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    wait = WebDriverWait(test.driver, 10)
    wait.until(EC.url_contains(reverse("mice_repository")))
