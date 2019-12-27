from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized

class companyProfileTestCases(BaseTest):
    def setUp(self):
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.company_profile_page.get_company_profile_page()

    def test001(self):
        pass