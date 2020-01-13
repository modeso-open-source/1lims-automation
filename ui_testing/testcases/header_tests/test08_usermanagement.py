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

    def test001_archive_user_management(self):
        """
        User management: Make sure that you can archive any record
        LIMS-6379
        :return:
        """
        self.header_page.click_on_user_management_button()
        selected_user_management_data, _ = self.header_page.select_random_multiple_table_rows()
        self.header_page.archive_selected_users()
        self.header_page.get_archived_users()
        for user in selected_user_management_data:
            user_name = user['Name']
            self.base_selenium.LOGGER.info(' + {} user should be activated.'.format(user_name))
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))

    def test002_restore_user(self):
        """
        User management: Restore Approach: Make sure that you can restore any record successfully
        LIMS-6380
        :return:
            """
        self.header_page.click_on_user_management_button()
        user_names = []
        self.header_page.get_archived_users()
        selected_user_data, _ = self.header_page.select_random_multiple_table_rows()
        for user in selected_user_data:
            user_names.append(user['Name'])

        self.header_page.restore_selected_user()
        self.header_page.get_active_users()
        for user_name in user_names:
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))

    @skip('https://modeso.atlassian.net/browse/LIMS-6384')
    def test003_user_search(self):
        """
        Header:  User management:  Search Approach: Make sure that you can search by any field in the active table successfully
        LIMS-6082
        :return:
        """
        self.header_page.click_on_user_management_button()
        row = self.header_page.get_random_user_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.header_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test004_download_user_sheet(self):
        """
        User management: Make sure you can export all the data in the active table & it should display in the same order
        LIMS-6101
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.header_page.download_xslx_sheet()
        rows_data = self.header_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.base_selenium.LOGGER.info(' * Comparing the user no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.header_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    def test005_delete_user(self):
        """
        User management : Delete Approach: Make sure that you an delete any record successfully
        if this user not used in other entities
        LIMS-6381
        :return:
            """
        self.header_page.click_on_user_management_button()
        # create new user
        self.header_page.create_new_user(user_email=(self.header_page.generate_random_email()), user_role='',
                                         user_password='1', user_confirm_password='1')
        self.base_selenium.LOGGER.info('make sure that that the user record created in the active table')
        active_user = self.header_page.search(value=self.header_page.user_name)[0].text
        self.assertIn(self.header_page.user_name, active_user)
        self.header_page.select_all_records()
        self.header_page.archive_selected_users()
        self.header_page.get_archived_users()
        self.base_selenium.LOGGER.info('make sure that that the user record navigate to the archive table')
        archive_user = self.header_page.search(value=self.header_page.user_name)[0].text
        self.assertIn(self.header_page.user_name, archive_user)
        self.header_page.select_all_records()
        self.header_page.click_on_user_right_menu()
        self.header_page.click_on_delete_button()
        self.header_page.confirm_popup()
        result = self.header_page.search(value=self.header_page.user_name)[0].text
        self.base_selenium.LOGGER.info('deleted successfully')
        self.assertFalse(result, 'deleted successfully')

    def test006_create_new_user(self):
        """
        Header: User management Approach:  Make sure that I can create new user successfully
        LIMS-6000
        :return:
        """
        self.header_page.click_on_user_management_button()
        #create new user
        self.header_page.create_new_user(user_email=(self.header_page.generate_random_email()), user_role='',
                                         user_password='1', user_confirm_password='1')

        #make sure when you search you will find it
        user_text = self.header_page.search(value=self.header_page.user_name)[0].text
        self.assertIn(self.header_page.user_name, user_text)


    def test007_user_filter(self):
        """
        Header: User management Approach: Make sure that you can filter by any field in the active table
        LIMS-6002
        :return:
        """
        self.header_page.click_on_user_management_button()
        # create new user to get it's data
        user = self.header_page.create_new_user(user_email=(self.header_page.generate_random_email()), user_role='',
                                                user_password='1', user_confirm_password='1')
        # the filter view will open
        self.header_page.click_on_filter_view()

        # filter by user name
        self.header_page.filter_user_by(filter_element='user_management:filter_name',
                                        filter_text=user['user_name'])
        result_user = self.header_page.result_table()[0]
        self.assertIn(user['user_name'], result_user.text)
        self.header_page.filter_reset_btn()

    def test008_overview_btn_from_create_edit_mode(self):
        """
        User Management: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table
        LIMS-6396
        :return:
        """
        # from the create mode it will redirect me to the active table
        self.header_page.click_on_user_management_button()
        self.header_page.click_create_new_user()
        self.header_page.click_on_overview_btn()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_users_page()
        self.assertEqual(self.base_selenium.get_url(), '{}users'.format(self.base_selenium.url))

        # from the edit mode it will redirect me to the active table
        self.header_page.get_random_user()
        self.header_page.click_on_overview_btn()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_users_page()
        self.assertEqual(self.base_selenium.get_url(), '{}users'.format(self.base_selenium.url))

    @parameterized.expand(['save_btn', 'cancel'])
    def test009_update_user_name_with_save_cancel_btn(self, save):
        """
        User managemen: User management: I can update user name with save & cancel button
        LIMS-6395
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))
        self.order_page.sleep_tiny()
        #
        current_name = self.header_page.get_user_name()
        self.header_page.set_user_name(self.generate_random_string())
        new_name = self.header_page.get_user_name()
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.base_selenium.get(
            url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_name = self.header_page.get_user_name()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_name) == {} (user_name)'.format(new_name, user_name))
            self.assertEqual(new_name, user_name)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_name) == {} (user_name)'.format(current_name, user_name))
            self.assertEqual(current_name, user_name)

    @parameterized.expand(['save_btn', 'cancel'])
    def test010_update_user_role_with_save_cancel_btn(self, save):
        """
        User management: I can update user role with save & cancel button
        LIMS-6398
        :return:
        """
        self.header_page.click_on_user_management_button()
        # open random user in the edit mode
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))
        self.order_page.sleep_tiny()
        current_role = self.header_page.get_user_role()
        self.header_page.set_user_role()
        new_role = self.header_page.get_user_role()
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.base_selenium.get(
            url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_role = self.header_page.get_user_role()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_role) == {} (user_role)'.format(new_role, user_role))
            self.assertEqual(new_role, user_role)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_role) == {} (user_role)'.format(current_role, user_role))
            self.assertEqual(current_role, user_role)


