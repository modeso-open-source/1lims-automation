from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
from api_testing.apis.base_api import BaseAPI
import re
from unittest import skip


class MyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.my_profile_page.get_my_profile_page()
        self.current_password = self.base_selenium.password
        self.new_password = None
        self.reset_original_password = False

    def tearDown(self):
        # reset the original password
        if self.reset_original_password:
            self.login_page.login(username=self.base_selenium.username, password=self.new_password)
            self.my_profile_page.get_my_profile_page()
            self.my_profile_page.change_password(self.new_password, self.current_password, True)
        return super().tearDown()


    def test001_user_can_change_password_and_press_on_cancel(self):
        """
        My Profile: Make sure after you change the password and press on cancel button, 
        the password shouldn't change

        LIMS-6091
        """
        # new password value
        self.new_password = self.my_profile_page.generate_random_text()
        # flag to insure that the user failed to login
        failed_to_login = False

        # change the password value
        self.my_profile_page.change_password(self.current_password, self.new_password)

        # logout
        self.header_page.logout()

        # try to authorize with the new password
        try:
            baseAPI = BaseAPI()
            baseAPI._get_authorized_session(username=self.base_selenium.username, password=self.new_password, reset_token=True)
        except:
            failed_to_login = True
        finally:
            self.assertTrue(failed_to_login)

    def test002_my_profile_should_show_username_and_email(self):
        """
        My Profile: Make sure that the user name & email displayed above the language

        LIMS-6090
        """
        username = self.base_selenium.get_text(element='my_profile:username')
        email = self.base_selenium.get_text(element='my_profile:email')
        self.assertTrue(username)
        self.assertTrue(email) 

    def test003_user_can_change_password_and_login_successfully(self):
        """
        My Profile: Make sure that you can change the password 
        and login with the new one successfully 

        LIMS-6084
        """
        # new password value
        self.new_password = self.my_profile_page.generate_random_text()

        # change password
        self.my_profile_page.change_password(self.current_password, self.new_password, True)

        # reset the original password flag
        self.reset_original_password = True
        
        # logout
        self.header_page.logout()

        # Authorize
        baseAPI = BaseAPI()
        auth_token = baseAPI._get_authorized_session(username=self.base_selenium.username, password=self.new_password)
        
        # check if the auth token has value
        self.assertTrue(auth_token)

    @parameterized.expand(['EN', 'DE'])
    def test004_user_can_change_the_language(self, lang):
        """
        My Profile: Language Approach: Make sure that you can change language

        LIMS-6089 ( https://modeso.atlassian.net/browse/LIMS-6089 )
        """
        # change the language
        self.base_selenium.select_item_from_drop_down(element='my_profile:language_field', item_text=lang)

        # wait till the page reloads
        self.my_profile_page.sleep_large()
        
        # get page name
        page_name = self.base_selenium.get_text('my_profile:page_name')

        if lang == 'EN':
            self.assertEqual(page_name, 'My Profile') 
        else:
            self.assertEqual(page_name, 'Mein profil')
