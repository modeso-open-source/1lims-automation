from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.my_profile_page import MyProfile
from ui_testing.pages.header_page import Header
from api_testing.apis.users_api import UsersAPI
from parameterized import parameterized
from api_testing.apis.base_api import BaseAPI


class MyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.my_profile_page = MyProfile()
        self.users_api = UsersAPI()
        self.info("create new user")
        response, payload = self.users_api.create_new_user()
        self.assertEqual(response['status'], 1, "failed to create new user")
        self.current_password = payload["password"]
        self.username = payload["username"]
        self.email = payload["email"]
        self.info('user {}:{}'.format(self.username, self.current_password))
        self.users_api._get_authorized_session(username=self.username, password=self.current_password, reset_token=True)
        self.set_authorization(auth=self.users_api.AUTHORIZATION_RESPONSE)
        self.my_profile_page.get_my_profile_page()

    def tearDown(self):
        # Blocked by https: // modeso.atlassian.net / browse / LIMS - 6425
        # self.users_api.delete_active_user(id=self.userId)
        return super().tearDown()

    def test001_user_can_change_password_and_press_on_cancel(self):
        """
        My Profile: Make sure after you change the password and press on cancel button,
        the password shouldn't change

        LIMS-6091
        """
        self.new_password = self.my_profile_page.generate_random_text()
        self.my_profile_page.change_password(self.current_password, self.new_password)
        response = self.users_api.post_auth(username=self.username, password=self.new_password)
        self.assertEqual("username_or_password_is_incorrect", response.json()["message"])

    def test002_my_profile_should_show_username_and_email(self):
        """
        My Profile: Make sure that the user name & email displayed above the language

        LIMS-6090
        """
        username = self.base_selenium.get_text(element='my_profile:username')
        self.info('Check the username is {}'.format(self.username))
        self.assertEqual(username.lower(), self.username.lower())

        email = self.base_selenium.get_text(element='my_profile:email')
        self.info('Check the email is {}'.format(self.email))
        self.assertTrue(email.lower(), self.email.lower())

    def test003_user_can_change_password_and_login_successfully(self):
        """
        My Profile: Make sure that you can change the password
        and login with the new one successfully

        LIMS-6084
        """
        # new password value
        new_password = self.my_profile_page.generate_random_text()

        # change password
        self.my_profile_page.change_password(self.current_password, new_password, True)

        # Authorize
        baseAPI = BaseAPI()
        auth_token = baseAPI._get_authorized_session(username=self.base_selenium.username, password=new_password)

        # check if the auth token has value
        self.assertTrue(auth_token)

    @parameterized.expand(['EN', 'DE'])
    def test004_user_can_change_the_language(self, lang):
        """
        My Profile: Language Approach: Make sure that you can change language

        LIMS-6089
        """
        self.my_profile_page.chang_lang('DE')
        self.my_profile_page.sleep_tiny()

        if lang == 'EN':
            self.my_profile_page.chang_lang('EN')
            self.my_profile_page.sleep_tiny()

        self.base_selenium.scroll()
        self.my_profile_page.sleep_tiny()
        page_name = self.base_selenium.get_text('my_profile:page_name')
        if lang == 'EN':
            self.assertEqual(page_name, 'My Profile')
        else:
            self.assertEqual(page_name, 'Mein Profil')

    def test005_company_profile_upload_logo_then_cancel_should_not_save(self):
        """
        My Profile: Signature Approach: Make sure after you upload the signature
        & press on cancel button, this signature didn't submit

        LIMS-6086
        """
        self.info('open signature tab')
        self.base_selenium.click('my_profile:signature_tab')
        # choose file from assets to be uploaded
        file_name = 'logo.png'
        self.info('upload the file then cancel')
        self.my_profile_page.upload_logo(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=False)

        self.info("Navigate to my profile page")
        self.my_profile_page.get_my_profile_page()
        self.info('open signature tab')
        self.base_selenium.click('my_profile:signature_tab')
        self.info('check that the image is not saved')
        is_the_file_not_exist = self.base_selenium.check_element_is_not_exist(
            element='general:file_upload_success_flag')
        self.assertTrue(is_the_file_not_exist)

    def test006_my_profile_user_can_upload_logo(self):
        """
        My Profile: Signature Approach: Make sure that you can upload the signature successfully

        LIMS-6085
        """
        self.info('open signature tab')
        self.base_selenium.click('my_profile:signature_tab')
        file_name = 'logo.png'
        uploaded_file_name = self.my_profile_page.upload_logo(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=True)
        self.assertEqual(uploaded_file_name, file_name)

    def test007_my_profile_user_can_update_logo(self):
        """
        My Profile: Signature Approach: Make sure that you can remove any signature

        LIMS-6095
        """
        self.info('open signature tab')
        self.base_selenium.click('my_profile:signature_tab')

        self.info('choose file from assets to be uploaded')
        file_name = 'logo.png'
        self.my_profile_page.upload_logo(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=True)

        self.info('remove the uploaded logo')
        self.base_selenium.scroll()
        self.base_selenium.click('general:remove_file')
        self.my_profile_page.save(save_btn="my_profile:save_button")

        self.info("check that the image is not saved")
        is_the_file_not_exist = self.base_selenium.check_element_is_not_exist(
            element='general:file_upload_success_flag')
        self.assertTrue(is_the_file_not_exist)

    def test008_you_cant_upload_more_than_one_signature(self):
        """
        My Profile: Signature Approach: Make sure you can't download more than one signature

        LIMS-6087
        """
        self.info('open signature tab')
        self.base_selenium.click('my_profile:signature_tab')
        self.info('choose file from assets to be uploaded')
        file_name = 'logo.png'
        other_file_name = 'logo2.png'
        self.info("upload the first file")
        self.my_profile_page.upload_logo(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=True)
        self.base_selenium.scroll()
        self.info("upload other file beside the current one")
        self.my_profile_page.upload_logo(
            file_name=other_file_name, drop_zone_element='my_profile:signature_field', save=True)
        self.base_selenium.scroll()
        self.assertTrue(self.base_selenium.find_element('general:oh_snap_msg'))
        self.info('wait to see if the file upload')
        self.my_profile_page.sleep_medium()
        self.info('get array of all uploaded files')
        files_uploaded_flags = self.base_selenium.find_elements('general:files_upload_success_flags')
        self.info('assert that only 1 file should be uploaded')
        self.assertEqual(len(files_uploaded_flags), 1)
