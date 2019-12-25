from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import time


class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.contacts_url = "{}contacts".format(self.base_selenium.url)
        self.contacts_page.get_contacts_page()








