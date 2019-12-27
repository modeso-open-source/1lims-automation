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
        country_name = 'Egypt'
        # open the country field 
        self.base_selenium.click(element='company_profile:country_field')
        # search for the country name
        self.base_selenium.set_text(element='company_profile:country_field', value=country_name)
        # get the results
        country_field_results = self.base_selenium.find_element('company_profile:country_field_results').text
        # check if the country name is in the results
        self.assertIn(country_name, country_field_results)