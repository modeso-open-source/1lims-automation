from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip
import time

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

        self.base_selenium.click(element='header:roles_and_permissions_button')
        self.header_page.sleep_small()
        selected_roles_and_permissions_data, _ = self.header_page.select_random_multiple_table_rows()
        self.header_page.archive_entity(menu_element='roles_and_permissions:right_menu',
                                        archive_element='roles_and_permissions:archive')
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
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
        self.base_selenium.click(element='header:roles_and_permissions_button')
        role_names = []
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        selected_role_data, _ = self.header_page.select_random_multiple_table_rows()
        for role in selected_role_data:
            role_names.append(role['Name'])
        self.header_page.restore_entity(menu_element='roles_and_permissions:right_menu',
                                        restore_element='roles_and_permissions:restore')
        self.header_page.get_active_entities(menu_element='roles_and_permissions:right_menu',
                                            active_element='roles_and_permissions:active')
        for role_name in role_names:
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    def test003_search_roles_and_permissions(self):
        """
        Header: Roles & Permissions: Search Approach: Make sure that you can search by any field in the active table successfully
        LIMS-6083
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
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
        self.base_selenium.click(element='header:roles_and_permissions_button')
        self.base_selenium.LOGGER.info('Press on create new role button')
        self.base_selenium.click(element='roles_and_permissions:new_role_btn')
        self.base_selenium.LOGGER.info('Press on the overview  button')
        self.base_selenium.click(element='roles_and_permissions:roles_overview_btn')
        self.header_page.confirm_popup()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_roles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}roles'.format(self.base_selenium.url))

        # from the edit mode it will redirect me to the active table
        self.header_page.get_random_role()
        self.base_selenium.LOGGER.info('Press on the overview  button')
        self.base_selenium.click(element='roles_and_permissions:roles_overview_btn')
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
        self.base_selenium.click(element='header:roles_and_permissions_button')
        # open random user in the edit mode
        self.header_page.get_random_role()
        role_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + role_url : {}'.format(role_url))
        self.order_page.sleep_tiny()
        current_name = self.header_page.get_role_name()
        random_name = self.generate_random_string()
        self.header_page.set_role_name(role_name=random_name)
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

    def test006_delete_role_not_used_in_other_entity(self):
        """
        Roles & Permissions: Make sure that you can delete any role record,
        If this record not used in other entity
        LIMS-6401
        :return:
            """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        random_role_name = self.generate_random_string()
        self.header_page.create_new_role(role_name =random_role_name)

        self.base_selenium.LOGGER.info('make sure that that the user record created in the active table')
        created_role = self.header_page.search(random_role_name)[0]
        role_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_role)
        self.assertTrue(created_role, role_data)

        self.header_page.select_all_records()
        self.header_page.archive_entity(menu_element='roles_and_permissions:right_menu',
                                        archive_element='roles_and_permissions:archive')
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')

        self.base_selenium.LOGGER.info('make sure that that the user record navigate to the archive table')
        created_role = self.header_page.search(random_role_name)[0]
        role_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_role)
        self.assertTrue(created_role, role_data)

        self.header_page.select_all_records()
        self.base_selenium.LOGGER.info('Press on the right menu')
        self.base_selenium.click(element='roles_and_permissions:right_menu')
        self.base_selenium.LOGGER.info('Press on the delete button')
        self.base_selenium.click(element='roles_and_permissions:delete')
        self.header_page.confirm_popup()

        result = self.header_page.search(value=random_role_name)
        self.base_selenium.LOGGER.info('deleted successfully')
        self.assertTrue(result, 'No records found')

    def test007_validation_role_name_field(self):
        """
        Roles & Permissions: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table
        LIMS-6404
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
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
        self.base_selenium.click(element='header:roles_and_permissions_button')
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

    def test010_delete_role_used_in_other_entity(self):
        """
        Roles & Permissions: Make sure that you can't delete any role record If this record used in other entity
        LIMS-6437
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        # create new role with random data
        role_random_name = self.generate_random_string()
        self.header_page.create_new_role(role_name = role_random_name)
        self.base_selenium.LOGGER.info(
            'search to make sure that the role created '.format(role_random_name))
        created_role = self.header_page.search(role_random_name)[0]
        role_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_role)

        self.header_page.click_on_header_button()
        self.base_selenium.click(element='header:user_management_button')

        # use this role in any other entity so update the user role field with it
        self.header_page.get_random_user()
        self.header_page.set_user_role(user_role=role_random_name)
        self.header_page.save(save_btn='roles_and_permissions:save_btn')

        # navigate to the role page to delete it
        self.header_page.get_roles_page()
        self.header_page.search(value =role_random_name)

        self.header_page.select_all_records()
        # navigate to the archived table to delete it
        self.header_page.archive_entity(menu_element='roles_and_permissions:right_menu',
                                        archive_element='roles_and_permissions:archive')
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        self.header_page.select_all_records()
        self.base_selenium.LOGGER.info('Press on the right menu')
        self.base_selenium.click(element='roles_and_permissions:right_menu')

        # make sure when you press on the delete button. message appear to confirm that I want to delete
        self.base_selenium.LOGGER.info('Press on the delete button')
        self.base_selenium.click(element='roles_and_permissions:delete')
        self.header_page.confirm_popup()
        self.base_selenium.LOGGER.info(
            'message will appear this user related to some data & cant delete it')
        self.header_page.confirm_popup()

        self.base_selenium.LOGGER.info(
            'search to make sure this user found in the active table '.format(role_random_name))
        result = self.header_page.search(value=role_random_name)
        self.assertTrue(result, role_data)

    def test011_archived_role_not_displayed_in_the_user_role_drop_down(self):
        """
        Roles& Permissions: Archived roles shouldn't display in the user role drop down.l
        LIMS-6438
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        # create new user with random data
        role_random_name = self.generate_random_string()
        self.header_page.create_new_role(role_name = role_random_name)

        self.base_selenium.LOGGER.info(
            'search to make sure that the role created '.format(role_random_name))
        created_role = self.header_page.search(role_random_name)[0]
        role_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_role)
        self.assertTrue(created_role, role_data)

        # archive the role that you created
        self.header_page.select_all_records()
        self.header_page.archive_entity(menu_element='roles_and_permissions:right_menu',
                                        archive_element='roles_and_permissions:archive')
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        # go to the user entity to search by it in the user drop down list
        self.header_page.click_on_header_button()
        self.base_selenium.click(element='header:user_management_button')

        self.header_page.get_random_user()
        result = self.header_page.set_user_role(user_role=role_random_name)
        self.assertFalse(result, 'no results found ')

    def test012_cant_create_two_roles_with_the_same_name(self):
        """
        Roles & Permissions: you can't create two roles with the same name
        LIMS-6439
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        # create new user with random data
        role_random_name = self.generate_random_string()
        self.header_page.create_new_role(role_name = role_random_name)

        self.base_selenium.LOGGER.info(
            'search to make sure that the role created '.format(role_random_name))
        created_role = self.header_page.search(role_random_name)[0]
        role_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_role)
        self.assertTrue(created_role, role_data)

        # create role with the same name
        created_role = self.header_page.create_new_role(role_name=role_random_name)
        self.base_selenium.LOGGER.info(
            'red border will display that the name already exit'.format(role_random_name))
        self.assertTrue(created_role, 'Name already exit')

    def test013_create_role_with_master_data_permissions_then_create_user_by_it(self):
        """
        Roles & Permissions: when I create user with master data permissions then create user wit it
        when I login with this user the master data only should appear in the menu
        LIMS-6440
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        # create role with random name with master data permissions
        random_role_name = self.generate_random_string()
        self.header_page.create_role_with_mater_data_permissions(role_name = random_role_name)

        # go to the user section to create user with this role
        self.header_page.click_on_header_button()
        self.base_selenium.click(element='header:user_management_button')

        # go to the user section to create user with this role
        random_user_name = self.generate_random_string()
        random_user_email = self.base_page.generate_random_email()
        self.header_page.create_new_user(user_name=random_user_name,
                                         user_email=random_user_email,
                                         user_role=random_role_name, user_password='1',
                                         user_confirm_password='1')

        self.header_page.click_on_header_button()
        self.base_selenium.LOGGER.info('Press on logout button')
        self.base_selenium.click(element='header:logout')

        # login with role & user that you created to make sure from the permissions
        self.login_page.login(username=random_user_name, password='1')
        time.sleep(15)

        # make sure that all the master data pages appear(articles & test units & test plans & contacts)
        self.base_selenium.LOGGER.info('get the test unit url')
        self.assertTrue('Test Units', self.test_unit_page.get_test_units_page())
        self.base_selenium.LOGGER.info('get the articles url')
        self.assertTrue('Articles', self.article_page.get_articles_page())
        self.base_selenium.LOGGER.info('get the test plan url')
        self.assertTrue('Test Plans', self.test_plan.get_test_plans_page())
        self.base_selenium.LOGGER.info('get the contacts url')
        self.assertTrue('Contacts', self.contacts_page.get_contacts_page())

    def test014_create_role_with_sample_management_permissions_then_create_user_by_it(self):
        """

        LIMS-6441
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        # create role with random name with sample management permissions
        random_role_name = self.generate_random_string()
        self.header_page.create_role_with_sample_management_permissions(role_name = random_role_name)

        # go to the user section to create user with this role
        self.header_page.click_on_header_button()
        self.base_selenium.click(element='header:user_management_button')

        # go to the user section to create user with this role
        random_user_name = self.generate_random_string()
        random_user_email = self.base_page.generate_random_email()
        self.header_page.create_new_user(user_name=random_user_name,
                                         user_email=random_user_email,
                                         user_role=random_role_name, user_password='1',
                                         user_confirm_password='1')

        self.header_page.click_on_header_button()
        self.base_selenium.LOGGER.info('Press on logout button')
        self.base_selenium.click(element='header:logout')

        # login with role & user that you created to make sure from the permissions
        self.login_page.login(username=random_user_name, password='1')
        time.sleep(15)

        # make sure that all the master data pages appear(articles & test units & test plans & contacts)
        self.base_selenium.LOGGER.info('get the order url')
        self.assertTrue('Sample Management', self.order_page.get_orders_page())
        self.base_selenium.LOGGER.info( 'get the analysis url')
        self.assertTrue('Sample Management', self.single_analysis_page.get_analysis_page())

    def test015_filter_by_role_name(self):
        """
        Roles & Permissions: Make sure that the user can filter by role name
        LIMS-6120
        :return:
        """
        self.header_page.get_roles_page()
        role_data = self.header_page.get_role_data_from_fully_checked_headers_random_row()

        self.base_selenium.click(element='general:menu_filter_view')
        self.header_page.filter_user_by(filter_element='roles_and_permissions:role_name',
                                        filter_text=role_data['name'])

        roles_result = self.header_page.result_table()
        self.assertIn(str(role_data['name']), (roles_result[0].text).replace("'", ""))

        self.base_selenium.LOGGER.info('filter results displayed with random role name')
        self.base_selenium.click(element='roles_and_permissions:reset_btn')

    def test016_filter_by_no(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role number
        LIMS-6003
        :return:
        """
        self.header_page.get_roles_page()
        role_data = self.header_page.get_role_data_from_fully_checked_headers_random_row()

        self.base_selenium.click(element='general:menu_filter_view')
        self.header_page.filter_user_by(filter_element='roles_and_permissions:filter_no',
                                        filter_text=role_data['number'])

        roles_result = self.header_page.result_table()
        self.assertIn(str(role_data['number']), (roles_result[0].text).replace("'", ""))

        self.base_selenium.LOGGER.info('filter results displayed with the role no')
        self.base_selenium.click(element='roles_and_permissions:reset_btn')

    def test017_filter_created_on(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role created on
        LIMS-6508
        :return:
        """
        self.header_page.get_roles_page()
        role_data = self.header_page.get_role_data_from_fully_checked_headers_random_row()

        self.base_selenium.click(element='general:menu_filter_view')
        self.header_page.filter_user_by(filter_element='roles_and_permissions:filter_created_on',
                                        filter_text=role_data['created_on'])

        roles_result = self.header_page.result_table()
        self.assertIn(str(role_data['created_on']), (roles_result[0].text).replace("'", ""))

        self.base_selenium.LOGGER.info('filter results displayed with the role created_on')
        self.base_selenium.click(element='roles_and_permissions:reset_btn')

class LoginRandomUser(BaseTest):

    def setUp(self):
        super().setUp()
        self.random_user_name = self.generate_random_string()
        random_user_email = self.base_page.generate_random_email()
        random_user_password = self.generate_random_string()
        self.users_api.create_new_user(self.random_user_name, random_user_email, random_user_password)
        self.login_page.login(username=self.random_user_name, password=random_user_password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.header_page.click_on_header_button()

    def test018_filter_by_changed_by(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role changed by
        LIMS-6507
        :return:
        """
        self.base_selenium.click(element='header:roles_and_permissions_button')
        random_role_name= self.generate_random_string()
        self.header_page.create_new_role(role_name=random_role_name)

        self.header_page.click_on_table_configuration_button()
        self.base_selenium.click(element='roles_and_permissions:checked_role_changed_by')
        self.base_selenium.click(element='roles_and_permissions:apply_btn')


        self.base_selenium.click(element='general:menu_filter_view')
        self.header_page.filter_user_drop_down(filter_name='roles_and_permissions:filter_changed_by',
                                               filter_text=self.random_user_name)

        roles_result = self.header_page.get_table_rows_data()
        self.assertIn(self.random_user_name, roles_result[0])




