import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class MySeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 1000)
        self.browser.implicitly_wait(1000)
        self.addCleanup(self.browser.quit)

    def test_PageTitle(self):
        self.browser.get("http://127.0.0.1:8000/login/")

        self.assertIn("Pur Beurre", self.browser.title)
        self.browser.get("http://127.0.0.1:8000/")
        self.assertIn("Pur Beurre", self.browser.title)

    def test_login(self):
        self.browser.get("http://127.0.0.1:8000/logout/")
        self.browser.get("http://127.0.0.1:8000/login/")
        mail = self.browser.find_element_by_id("id_email")
        password = self.browser.find_element_by_id("id_password")
        submit = self.browser.find_element_by_id("submit_login")
        mail.send_keys("superusermail@gmail.com")
        password.send_keys("superuserpassword")
        submit.click()
        time.sleep(1)
        cur_url = self.browser.current_url
        self.assertEqual(cur_url, "http://127.0.0.1:8000/")
