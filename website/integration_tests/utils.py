from django.urls import reverse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def options():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--headless")
    return chrome_options

def auto_login(test):
    live_server_url = test.live_server_url
    test.driver.get(live_server_url + reverse("login"))
    username_field = test.driver.find_element(By.ID, "id_username")
    username_field.send_keys(test.user.username)
    password_field = test.driver.find_element(By.ID, "id_password")
    password_field.send_keys("testpassword")
    test.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    wait = WebDriverWait(test.driver, 10)
    wait.until(EC.url_contains(reverse("projects:list_projects")))