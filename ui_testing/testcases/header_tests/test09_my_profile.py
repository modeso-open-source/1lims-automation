from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
from api_testing.apis.base_api import BaseAPI
import re
from unittest import skip


class MyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.my_profile_page.info(self.base_selenium.password)
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.my_profile_page.get_my_profile_page()

    def test001_user_can_change_password_and_press_on_cancel(self):
        """
        My Profile: Make sure after you change the password and press on cancel button, 
        the password shouldn't change

        LIMS-6091
        """
        # new password value
        new_password = self.my_profile_page.generate_random_text()
        # flag to insure that the user failed to login
        failed_to_login = False

        # change the password value
        self.base_selenium.set_text(
            'my_profile:current_password_field', self.base_selenium.password)
        self.base_selenium.set_text(
            'my_profile:new_password_field', new_password)
        self.base_selenium.set_text(
            'my_profile:confirm_password_field', new_password)

        # cancel
        self.my_profile_page.cancel(force=True)

        # logout
        self.header_page.click_on_header_button()
        self.base_selenium.click(element='header:logout_button')
        self.header_page.sleep_medium()

        # try to authorize with the new password
        try:
            baseAPI = BaseAPI()
            baseAPI._get_authorized_session(username=self.base_selenium.username, password=new_password, reset_token=True)
        except:
            failed_to_login = True
        finally:
            self.assertTrue(failed_to_login)
