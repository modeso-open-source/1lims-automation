from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip

class HeaderTestCases(BaseTest):
        def setUp(self):
            super().setUp()
            self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
            self.base_selenium.wait_until_page_url_has(text='dashboard')
            self.header_page.click_on_header_button()




        def test008_validate_all_user_fields(self):
            """
            New: orders Test plan /test unit validation in edit mode
            LIMS-4826
            """
            self.base_selenium.LOGGER.info(
                ' Running test case to check on the validation of all fields')

            # validate in edit mode, go to to user active table
            self.header_page.click_on_user_management_button()
            self.header_page.get_random_user()
            user_url = self.base_selenium.get_url()
            self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))

            self.base_selenium.LOGGER.info(
                ' Remove all selected fields name & email & role')
            # delete all fields
            self.header_page.get_user_name()
            self.header_page.clear_user_name()
            self.header_page.clear_user_email()
            self.header_page.sleep_small()
            self.header_page.clear_user_role()
            self.header_page.sleep_small()
            self.header_page.save(save_btn='user_management:save_btn', logger_msg='Save new user, should fail')

            # check name & email & role fields have error
            user_name_class_name = self.base_selenium.get_attribute(element="user_management:user_name", attribute='class')
            user_email_class_name = self.base_selenium.get_attribute(element="user_management:user_email", attribute='class')
            user_role_class_name = self.base_selenium.get_attribute(element="user_management:user_role", attribute='class')
            self.assertIn('has-error', user_name_class_name)
            self.assertIn('has-error', user_email_class_name)
            self.assertIn('has-error', user_role_class_name)






