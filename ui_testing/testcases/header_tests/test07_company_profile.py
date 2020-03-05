from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.company_profile_page import CompanyProfile
from parameterized import parameterized


class CompanyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.company_profile_page = CompanyProfile()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.company_profile_page.get_company_profile_page()

    def test001_user_can_search_in_the_country_field(self):
        """
        Company profile: Country Approach: Make sure that you can search in the country field

        LIMS-6295
        """
        search_text = 'Switzerland'
        # get the results
        country_field_results = self.base_selenium.get_drop_down_suggestion_list(
            element='company_profile:country_field', item_text=search_text)
        # check if the country name is in the results
        self.assertIn(search_text, country_field_results)

    @parameterized.expand(['name', 'street_name', 'street_number', 'postal_code', 'location', 'country'])
    def test002_user_can_change_any_field_and_cancel(self, field_name):
        """
        Company profile: Make sure after you edit any data and press on cancel button, nothing occur 

        LIMS-6096
        """
        # set field type depanding on name
        field_type = 'text'
        if field_name == 'country':
            field_type = 'drop_down'

        # get the field value before edit
        field_value_before_edit = self.company_profile_page.get_field_value(
            field_name, field_type)

        # change the value
        self.company_profile_page.set_field_value(field_name, field_type)

        # click on cancel
        self.company_profile_page.cancel(force=True)
        self.company_profile_page.get_company_profile_page()

        # get the field value after edit
        field_value_after_edit = self.company_profile_page.get_field_value(
            field_name, field_type)

        # compare the before value and the after value
        self.assertEqual(field_value_before_edit, field_value_after_edit)

    def test003_user_can_update_company_profile(self):
        """
        Company Profile: Make sure that you can create company profile 
        with all data( name, street name, street number, ....) 

        LIMS-6093
        """
        # update the profile and get the values before saving
        company_profile = self.company_profile_page.update_company_profile()

        # refresh the page
        self.company_profile_page.get_company_profile_page()

        # check that the values before save are matching the values after refresh.
        self.assertEqual(company_profile['name'], self.company_profile_page.get_field_value('name'))
        self.assertEqual(company_profile['street_name'], self.company_profile_page.get_field_value('street_name'))
        self.assertEqual(company_profile['street_number'], self.company_profile_page.get_field_value('street_number'))
        self.assertEqual(company_profile['postal_code'], self.company_profile_page.get_field_value('postal_code'))
        self.assertEqual(company_profile['location'], self.company_profile_page.get_field_value('location'))
        self.assertEqual(company_profile['country'], self.company_profile_page.get_field_value(field_name='country', field_type='drop_down'))

    def test004_company_profile_has_username_and_email(self):
        """
        Company Profile: Make sure that the user name & email displayed in the profile

        LIMS-6098
        """
        username = self.base_selenium.get_text(element='company_profile:username')
        email = self.base_selenium.get_text(element='company_profile:email')
        self.assertTrue(username)
        self.assertTrue(email)

    def test005_company_profile_fields_validation(self):
        """
        Compeny profile: Make sure that when you didn't enter any field then press on save button, 
        red border display on all fields

        LIMS-6506
        """
        self.company_profile_page.set_field_value(field_name='name', empty=True)
        self.company_profile_page.save()
        self.company_profile_page.sleep_small()
        validation_error = self.base_selenium.check_element_is_exist(element='company_profile:validation_error')
        self.assertTrue(validation_error)

    def test006_company_profile_upload_file_then_cancel_should_not_save(self):
        """
        Company profile: Make sure after you edit any data and press on cancel button, nothing occur

        LIMS-6096
        """
        # choose file from assets to be uploaded
        file_name = 'logo.png'

        # upload the file then cancel
        self.company_profile_page.upload_file(
            file_name=file_name, drop_zone_element='company_profile:logo_field', save=False, remove_current_file=True)

        # go back to the company profile
        self.company_profile_page.get_company_profile_page()

        # check that the image is not saved
        is_the_file_exist = self.base_selenium.check_element_is_exist(
            element='general:file_upload_success_flag')
        self.assertFalse(is_the_file_exist)
