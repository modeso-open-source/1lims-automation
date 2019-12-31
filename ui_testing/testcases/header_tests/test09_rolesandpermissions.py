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

    def test001_archive_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure that you can archive any role record
        LIMS-6400
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        selected_roles_and_permissions_data, _ = self.header_page.select_random_multiple_table_rows()
        self.header_page.archive_selected_roles_and_permissions()
        self.header_page.get_archived_roles_and_permissions()
        for role in selected_roles_and_permissions_data:
            role_name = role['Name']
            self.base_selenium.LOGGER.info(' + {} role should be activated.'.format(role_name))
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    def test002_restore_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure that you can restore any role record
        LIMS-6104
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        role_names = []
        self.header_page.get_archived_roles_and_permissions()
        selected_role_data, _ = self.header_page.select_random_multiple_table_rows()
        for role in selected_role_data:
            role_names.append(role['Name'])

        self.header_page.restore_selected_roles()
        self.header_page.get_active_roles()
        for role_name in role_names:
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    def test003_search_roles_and_permissions(self):
        """
        Header: Roles & Permissions: Search Approach: Make sure that you can search by any field in the active table successfully
        LIMS-6083
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        row = self.header_page.get_random_role_row()
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

    def test004_overview_btn_from_create_edit_mode(self):
        """
        Roles & Permissions: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table
        LIMS-6404
        :return:
        """
        # from the create mode it will redirect me to the active table
        self.header_page.click_on_roles_permissions_button()
        self.header_page.click_create_new_role()
        self.header_page.click_on_role_overview_btn()
        self.header_page.confirm_popup()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_roles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}roles'.format(self.base_selenium.url))

        # from the edit mode it will redirect me to the active table
        self.header_page.get_random_role()
        self.header_page.click_on_role_overview_btn()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_roles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}roles'.format(self.base_selenium.url))

    @parameterized.expand(['save_btn', 'cancel'])
    def test005_update_role_name_with_save_cancel_btn(self, save):
        """
        Roles & Permissions: Make sure that you can update role name with save & cancel button
        LIMS-6108
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        # open random user in the edit mode
        self.header_page.get_random_role()
        role_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + role_url : {}'.format(role_url))
        self.order_page.sleep_tiny()
        current_name = self.header_page.get_role_name()
        self.header_page.set_role_name(role_name='text')
        new_name = self.header_page.get_role_name()
        if 'save_btn' == save:
            self.header_page.save(save_btn='roles_and_permissions:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.base_selenium.get(
            url=role_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_name = self.header_page.get_role_name()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_role) == {} (user_role)'.format(new_name, user_name))
            self.assertEqual(new_name, user_name)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_role) == {} (user_role)'.format(current_name, user_name))
            self.assertEqual(current_name, user_name)

    def test006_delete_role(self):
        """
        Roles & Permissions: Make sure that you can delete any role record,
        If this record not used in other entity
        LIMS-6401
        :return:
            """
        self.header_page.click_on_roles_permissions_button()
        # create new role record
        self.header_page.create_new_role(role_name = self.header_page.generate_random_text())
        self.base_selenium.LOGGER.info('make sure that that the user record created in the active table')
        active_role = self.header_page.search(value=self.header_page.role_name)[0].text
        self.assertIn(self.header_page.role_name, active_role)
        self.header_page.select_all_records()
        self.header_page.archive_selected_roles()
        self.header_page.get_archived_roles()
        self.base_selenium.LOGGER.info('make sure that that the user record navigate to the archive table')
        archive_role = self.header_page.search(value=self.header_page.role_name)[0].text
        self.assertIn(self.header_page.role_name, archive_role)
        self.header_page.select_all_records()
        self.header_page.click_on_role_right_menu()
        self.header_page.click_on_role_delete_btn()
        self.header_page.confirm_popup()
        result = self.header_page.search(value=self.header_page.role_name)[0].text
        self.base_selenium.LOGGER.info('deleted successfully')
        self.assertFalse(result, 'deleted successfully')


    def test007_validation_role_name_field(self):
        """
        Roles & Permissions: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table
        LIMS-6404
        :return:
        """
        # from the create mode it will redirect me to the active table
        self.header_page.click_on_roles_permissions_button()
        self.header_page.get_random_role()
        self.header_page.clear_role_name()
        self.header_page.sleep_medium()
        self.header_page.save(save_btn='roles_and_permissions:save_btn')
        self.header_page.sleep_small()
        self.base_selenium.LOGGER.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.base_selenium.LOGGER.info('Assert error msg')
        self.assertEqual(validation_result, True)

    def test008_download_role_sheet(self):
        """
        Roles & Permissions: Make sure you can export all the data in the active table
        & it should display in the same order

        LIMS-6107
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.header_page.download_xslx_sheet()
        rows_data = self.header_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.base_selenium.LOGGER.info(' * Comparing the role no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.header_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)
    
    @parameterized.expand(['10', '20', '25', '50', '100'])
    def test009_testing_table_pagination(self, pagination_limit):
        """
        Header: Active table: Pagination Approach; Make sure that I can set the pagination to display 10/20/25/50/100 records in each page 
        """
        
        self.header_page.click_on_roles_permissions_button()
        
        self.header_page.set_page_limit(limit=pagination_limit)
        table_info = self.header_page.get_table_info_data()

        self.base_selenium.LOGGER.info('get current table records count')
        table_records_count = str(len(self.header_page.result_table()) -1)

        self.base_selenium.LOGGER.info('table records count is {}, and it should be {}'.format(table_records_count, table_info['page_limit']))
        self.assertEqual(table_records_count, table_info['page_limit'])

        self.base_selenium.LOGGER.info('current page limit is {}, and it should be {}'.format(table_info['pagination_limit'], pagination_limit))
        self.assertEqual(table_info['pagination_limit'], pagination_limit)

        if int(table_info['pagination_limit']) <= int(table_info['count']):
            self.assertEqual(table_info['pagination_limit'], table_records_count)


