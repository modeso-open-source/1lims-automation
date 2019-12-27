from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized

class companyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.company_profile_page.get_company_profile_page()

    def test001_user_can_search_in_the_country_field(self):
        """
        Company profile: Country Approach: Make sure that you can search in the country field

        LIMS-6295
        """
        search_text = 'Egy'    
        # get the results
        country_field_results = self.base_selenium.get_drop_down_suggestion_list(element='company_profile:country_field', item_text=search_text)
        # check if the country name is in the results
        self.assertIn(search_text, country_field_results)

    def test002_user_can_change_any_field_and_cancel(self):
        """
        Company profile: Make sure after you edit any data and press on cancel button, nothing occur 

        LIMS-6096
        """
        pass