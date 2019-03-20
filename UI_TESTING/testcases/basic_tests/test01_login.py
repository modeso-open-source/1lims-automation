from testcases.base_test import BaseTest
from pages.login_page import Login
import time


class LoginTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()

    def test001_login_correct_data(self):
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        time.sleep(30)
        self.assertIn('dashboard', self.login_page.base_selenium.get_url())



