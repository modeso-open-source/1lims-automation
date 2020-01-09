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
        self.username = self.base_selenium.username
        self.current_password = self.base_selenium.password
        self.email = None
        self.new_password = None
        self.reset_original_password = False
        self.reset_language = False

    def tearDown(self):
        # reset the original password
        if self.reset_original_password:
            self.login_page.login(username=self.base_selenium.username, password=self.new_password)
            self.base_selenium.wait_until_page_url_has(text='dashboard')
            self.my_profile_page.get_my_profile_page()
            self.my_profile_page.change_password(self.new_password, self.current_password, True)
            self.reset_original_password = False

        # reset the english language
        if self.reset_language:
            self.my_profile_page.chang_lang('EN')
            self.reset_language = False
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
        self.login_page.logout()

        # try to authorize with the new password
        try:
            baseAPI = BaseAPI()
            baseAPI._get_authorized_session(username=self.base_selenium.username, password=self.new_password, reset_token=True)
        except:
            failed_to_login = True
        else:
            raise Exception('The user was able to authorize with an unsaved password')
        finally:
            self.assertTrue(failed_to_login)

    def test002_my_profile_should_show_username_and_email(self):
        """
        My Profile: Make sure that the user name & email displayed above the language

        LIMS-6090
        """
        username = self.base_selenium.get_text(element='my_profile:username')
        email = self.base_selenium.get_text(element='my_profile:email')
        self.assertEqual(username.lower(), self.username.lower())
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
        self.login_page.logout()

        # Authorize
        baseAPI = BaseAPI()
        auth_token = baseAPI._get_authorized_session(username=self.base_selenium.username, password=self.new_password)
        
        # check if the auth token has value
        self.assertTrue(auth_token)

    @parameterized.expand(['EN', 'DE'])
    def test004_user_can_change_the_language(self, lang):
        """
        My Profile: Language Approach: Make sure that you can change language

        LIMS-6089
        """
        # change language
        self.my_profile_page.chang_lang(lang)

        # to restore the language
        if lang == 'DE':
            self.reset_language = True
        
        # get page name
        page_name = self.base_selenium.get_text('my_profile:page_name')

        if lang == 'EN':
            self.assertEqual(page_name, 'My Profile') 
        else:
            self.assertEqual(page_name, 'Mein Profil')

    def test005_company_profile_upload_file_then_cancel_should_not_save(self):
        """
        My Profile: Signature Approach: Make sure after you upload the signature 
        & press on cancel button, this signature didn't submit
        
        LIMS-6086
        """
        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')

        # choose file from assets to be uploaded
        file_name = 'logo.png'

        # upload the file then cancel
        self.my_profile_page.upload_file(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=False, remove_current_file=True)

        # go back to the company profile
        self.my_profile_page.get_my_profile_page()

        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')

        # check that the image is not saved
        is_the_file_exist = self.base_selenium.check_element_is_exist(
            element='general:file_upload_success_flag')
        self.assertFalse(is_the_file_exist)