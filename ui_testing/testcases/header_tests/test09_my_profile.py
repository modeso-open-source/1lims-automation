from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip

class MyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.my_profile_page.get_my_profile_page()

    def test001_user_can_change_password_and_press_on_cancel(self):
        """
        My Profile: Make sure after you change the password and press on cancel button, 
        the password shouldn't change

        LIMS-6091
        """
        new_password = self.my_profile_page.generate_random_text()
        # change the password value
        self.base_selenium.set_text('my_profile:new_password_field', new_password)
        self.base_selenium.set_text('my_profile:confirm_password_field', new_password)
        
        # cancel
        self.my_profile_page.cancel(force=True)

        # get field values after edit