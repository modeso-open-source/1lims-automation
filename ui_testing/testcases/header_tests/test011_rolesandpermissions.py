from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.contacts_page import Contacts
from ui_testing.pages.header_page import Header
from ui_testing.pages.analysis_page import SingleAnalysisPage
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.roles_api import RolesAPI
from parameterized import parameterized
from nose.plugins.attrib import attr
import re, random
from unittest import skip


class HeaderTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.header_page = Header()
        self.users_api = UsersAPI()
        self.roles_api = RolesAPI()
        self.set_authorization(auth=self.users_api.AUTHORIZATION_RESPONSE)
        self.header_page.get_roles_page()

    def test001_archive_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure that you can archive any role record
        
        LIMS-6400
        """
        self.info("select random rows to archive")
        selected_roles_and_permissions_data, _ = self.header_page.select_random_multiple_users_table_rows()
        self.info("Archive selected rows")
        self.header_page.archive_entity(menu_element='roles_and_permissions:right_menu',
                                        archive_element='roles_and_permissions:archive')
        self.info("Navigate to archived roles table")
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        for role in selected_roles_and_permissions_data:
            role_name = role['Name']
            self.info(' + {} role should be activated.'.format(role_name))
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    def test002_restore_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure that you can restore any role record
        
        LIMS-6104
        """
        role_names = []
        self.info("Navigate to archived roles table")
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        self.info("select random rows to restore")
        selected_role_data, _ = self.header_page.select_random_multiple_users_table_rows()
        for role in selected_role_data:
            role_names.append(role['Name'])
        self.info("Restore selected roles")
        self.header_page.restore_entity(menu_element='roles_and_permissions:right_menu',
                                        restore_element='roles_and_permissions:restore')
        self.info("Navigate to active roles table")
        self.header_page.get_active_entities(menu_element='roles_and_permissions:right_menu',
                                             active_element='roles_and_permissions:active')
        for role_name in role_names:
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    def test003_search_roles_and_permissions(self):
        """
        Header: Roles & Permissions: Search Approach: Make sure that you can search
        by any field in the active table successfully

        LIMS-6083
        """
        row = self.header_page.get_random_role_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.header_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test004_overview_btn_from_create_mode(self):
        """
        Roles & Permissions: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table

        LIMS-6404- create approach
        """
        # from the create mode it will redirect me to the active table
        self.info('Press on create new role button')
        self.base_selenium.click(element='roles_and_permissions:new_role_btn')
        self.info('Press on the overview  button')
        self.base_selenium.click(element='roles_and_permissions:roles_overview_btn')
        self.header_page.confirm_popup()
        self.info('it will redirect me to the active table')
        self.header_page.get_roles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}roles'.format(self.base_selenium.url))

    def test005_overview_btn_from_edit_mode(self):
        """
        Roles & Permissions: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table

        LIMS-6404- edit approach
        """
        self.info("get random role edit page")
        response, payload = self.roles_api.get_all_roles()
        self.assertEqual(response['status'], 1, response)
        random_role_id = random.choice(response['roles'])['id']
        self.header_page.get_role_edit_page_by_id(random_role_id)
        self.info('Press on the overview  button')
        self.base_selenium.click(element='roles_and_permissions:roles_overview_btn')
        self.info('it will redirect me to the active table')
        self.header_page.get_roles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}roles'.format(self.base_selenium.url))

    @parameterized.expand(['save_btn', 'cancel'])
    def test006_update_role_name_with_save_cancel_btn(self, save):
        """
        Roles & Permissions: Make sure that you can update role name with save & cancel button

        LIMS-6108
        """
        self.info("get random role edit page")
        random_role = random.choice(self.roles_api.get_random_role())
        self.header_page.get_role_edit_page_by_id(random_role['id'])
        new_name = self.generate_random_string()
        self.header_page.set_role_name(role_name=new_name)
        if 'save_btn' == save:
            self.header_page.save(save_btn='roles_and_permissions:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.header_page.get_roles_page()
        found_role = self.header_page.filter_role_by_no(random_role['id'])['Name']
        if 'save_btn' == save:
            self.assertEqual(found_role, new_name)
        else:
            self.assertEqual(found_role, random_role['name'])

    def test007_delete_role_not_used_in_other_entity(self):
        """
        Roles & Permissions: Make sure that you can delete any role record,
        If this record not used in other entity

        LIMS-6401
        """
        role_name = self.generate_random_string()
        response, payload = self.roles_api.create_role(role_name=role_name)
        self.assertEqual(response['status'], 1)
        row = self.header_page.search(role_name)
        self.header_page.sleep_tiny()
        self.header_page.click_check_box(row[0])
        self.header_page.archive_selected_items()
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        self.info('make sure that that the user record navigate to the archive table')
        archived_row = self.header_page.search(role_name)
        self.header_page.click_check_box(archived_row[0])
        self.info('Press on the right menu')
        self.base_selenium.click(element='roles_and_permissions:right_menu')
        self.info('Press on the delete button')
        self.base_selenium.click(element='roles_and_permissions:delete')
        self.header_page.confirm_popup()
        result = self.header_page.search(value=role_name)
        self.info('deleted successfully')
        self.assertTrue(result, 'No records found')

    def test008_validation_role_name_field(self):
        """
        Roles & Permissions: Make sure from the validation of all fields

        LIMS-6122
        """
        self.info("get random role edit page")
        random_role = random.choice(self.roles_api.get_random_role())
        self.header_page.get_role_edit_page_by_id(random_role['id'])
        self.header_page.clear_role_name()
        self.header_page.sleep_medium()
        self.header_page.save(save_btn='roles_and_permissions:save_btn')
        self.header_page.sleep_small()
        self.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert error msg')
        self.assertEqual(validation_result, True)

    @skip('https://modeso.atlassian.net/browse/LIMSA-220')
    def test009_download_role_sheet(self):
        """
        Roles & Permissions: Make sure you can export all the data in the active table
        & it should display in the same order

        LIMS-6107
        """
        self.info(' * Download XSLX sheet')
        self.header_page.download_xslx_sheet()
        rows_data = self.header_page.get_table_rows_data()
        for index in range(len(rows_data)-1):
            self.info(' * Comparing the role no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.header_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(str(item).lower, fixed_sheet_row_data)

    @parameterized.expand(['10', '20', '25', '50', '100'])
    @attr(series=True)
    def test010_testing_table_pagination(self, pagination_limit):
        """
        Header: Active table: Pagination Approach; Make sure that I can set the pagination
        to display 10/20/25/50/100 records in each page

        LIMS-6103 
        """
        self.header_page.set_page_limit(limit=pagination_limit)
        table_info = self.header_page.get_table_info_data()

        self.info('get current table records count')
        table_records_count = str(len(self.header_page.result_table()) - 1)

        self.info('table records count is {}, and it should be {}'.
                  format(table_records_count, table_info['page_limit']))
        self.assertEqual(table_records_count, table_info['page_limit'])

        self.info('current page limit is {}, and it should be {}'.
                  format(table_info['pagination_limit'], pagination_limit))
        self.assertEqual(table_info['pagination_limit'], pagination_limit)

        if int(table_info['pagination_limit']) <= int(table_info['count']):
            self.assertEqual(table_info['pagination_limit'], table_records_count)

    def test011_delete_role_used_in_other_entity(self):
        """
        Roles & Permissions: Make sure that you can't delete any role record If this record used in other entity

        LIMS-6437
        """
        self.info('create new role with random data')
        role_random_name = self.generate_random_string()
        response, payload = self.roles_api.create_role(role_name=role_random_name)
        self.assertEqual(response['status'], 1, response)
        self.info("Navigate to users page")
        self.header_page.get_users_page()
        self.info("get random user edit page and set role to {}".format(role_random_name))
        self.header_page.get_random_user()
        self.header_page.sleep_tiny()
        self.header_page.set_user_role(user_role=role_random_name)
        self.header_page.save(save_btn='roles_and_permissions:save_btn')
        self.info("navigate to the role page to delete it")
        self.header_page.get_roles_page()
        row = self.header_page.search(role_random_name)
        self.header_page.sleep_tiny()
        self.header_page.click_check_box(row[0])
        self.header_page.archive_selected_items()
        self.header_page.get_archived_entities(menu_element='roles_and_permissions:right_menu',
                                               archived_element='roles_and_permissions:archived')
        self.info('make sure that that the user record navigate to the archive table')
        archived_row = self.header_page.search(role_random_name)
        self.header_page.click_check_box(archived_row[0])
        self.info('Press on the right menu')
        self.base_selenium.click(element='roles_and_permissions:right_menu')
        self.info('Press on the delete button')
        self.base_selenium.click(element='roles_and_permissions:delete')
        self.header_page.confirm_popup()
        self.info('message will appear this user related to some data & cant delete it')
        self.header_page.confirm_popup()
        self.info('search to make sure this user found in the active table '.format(role_random_name))
        result = self.header_page.search(value=role_random_name)
        self.assertIn(role_random_name, result[0].text)

    def test012_archived_role_not_displayed_in_the_user_role_drop_down(self):
        """
        Roles& Permissions: Archived roles shouldn't display in the user role drop down

        LIMS-6438
        """
        self.info('select random archived role')
        response, payload = self.roles_api.get_all_roles(deleted=1)
        self.assertEqual(response['status'], 1, response)
        role_random_name = random.choice(response['roles'])['name']
        self.info("archived role name {}".format(role_random_name))
        # go to the user entity to search by it in the user drop down list
        self.header_page.get_users_page()
        self.header_page.get_random_user()
        result = self.header_page.set_user_role(user_role=role_random_name)
        self.assertEqual(result, '')

    def test013_cant_create_two_roles_with_the_same_name(self):
        """
        Roles & Permissions: you can't create two roles with the same name

        LIMS-6439
        """
        self.info('create new role with random data')
        role_random_name = self.generate_random_string()
        response, payload = self.roles_api.create_role(role_name=role_random_name)
        self.assertEqual(response['status'], 1, response)
        self.info('create role with the same name')
        created_role = self.header_page.create_new_role(role_name=role_random_name)
        self.info('red border will display that the name already exit'.format(role_random_name))
        self.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert error msg')
        self.assertEqual(validation_result, True)
        self.assertEqual(created_role['role_name'], None)

    @attr(series=True)
    def test014_create_role_with_master_data_permissions_then_create_user_by_it(self):
        """
        Roles & Permissions: when I create user with master data permissions then create user wit it
        when I login with this user the master data only should appear in the menu

        LIMS-6440
        """
        self.login_page = Login()
        self.info('create role with random name with master data permissions')
        random_role_name = self.generate_random_string()
        self.header_page.create_role_with_mater_data_permissions(role_name=random_role_name)

        self.info('go to the user section to create user with this role')
        self.header_page.get_users_page()
        random_user_name = self.generate_random_string()
        random_user_email = self.header_page.generate_random_email()
        random_user_password = self.generate_random_string()
        self.header_page.create_new_user(user_name=random_user_name,
                                         user_email=random_user_email,
                                         user_role=random_role_name,
                                         user_password=random_user_password,
                                         user_confirm_password=random_user_password)

        self.login_page.logout()

        self.info('login with role & user {}:{}'.format(random_user_name, random_user_password))
        self.login_page.login(username=random_user_name, password=random_user_password)
        self.header_page.sleep_medium()
        # make sure that all the master data pages appear(articles & test units & test plans & contacts)
        self.info('get the test unit url')
        self.assertTrue('Test Units', TstUnit().get_test_units_page())
        self.info('get the articles url')
        self.assertTrue('Articles', Article().get_articles_page())
        self.info('get the test plan url')
        self.assertTrue('Test Plans', TstPlan().get_test_plans_page())
        self.info('get the contacts url')
        self.assertTrue('Contacts', Contacts().get_contacts_page())

    @attr(series=True)
    def test015_create_role_with_sample_management_permissions_then_create_user_by_it(self):
        """
        Roles & Permissions: when I create user with sample management permissions then create
        user wit it when I login with this user the master data only should appear in the menu

        LIMS-6441
        """
        self.login_page = Login()
        self.info("create role with random name with sample management permissions")
        random_role_name = self.generate_random_string()
        self.header_page.create_role_with_sample_management_permissions(role_name=random_role_name)

        self.info('go to the user section to create user with this role')
        self.header_page.get_users_page()
        random_user_name = self.generate_random_string()
        random_user_email = self.header_page.generate_random_email()
        random_user_password = self.generate_random_string()
        self.header_page.create_new_user(user_name=random_user_name,
                                         user_email=random_user_email,
                                         user_role=random_role_name,
                                         user_password=random_user_password,
                                         user_confirm_password=random_user_password)

        self.login_page.logout()

        self.info('login with role & user {}:{}'.format(random_user_name, random_user_password))
        self.login_page.login(username=random_user_name, password=random_user_password)
        self.header_page.sleep_medium()
        self.info('get the order url')
        self.assertTrue('Sample Management', Order().get_orders_page())
        self.info('get the analysis url')
        Orders().navigate_to_analysis_active_table()
        self.assertIn('sample/analysis', self.base_selenium.get_url())

    def test016_filter_by_role_name(self):
        """
        Roles & Permissions: Make sure that the user can filter by role name

        LIMS-6120
        """
        self.info("get random role name")
        random_role = random.choice(self.roles_api.get_random_role())
        roles_results = self.header_page.filter_user_by(
            filter_element='roles_and_permissions:role_name',
            filter_text=random_role['name'])
        for roles_result in roles_results:
            self.assertEqual(random_role['name'], roles_result['Name'])

    def test017_filter_by_no(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role number

        LIMS-6003
        """
        self.info("get random role name")
        random_role = random.choice(self.roles_api.get_random_role())
        roles_result = self.header_page.filter_role_by_no(random_role['id'])
        self.assertEqual(str(random_role['id']), roles_result['No'])

    def test018_filter_created_on(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role created on

        LIMS-6508
        """
        self.header_page.set_all_configure_table_columns_to_specific_value()
        role_data = self.header_page.get_role_data_from_fully_checked_headers_random_row()
        roles_results = self.header_page.filter_user_by(
            filter_element='roles_and_permissions:filter_created_on',
            filter_text=role_data['created_on'])
        for roles_result in roles_results:
            self.assertEqual(role_data['created_on'], roles_result['Created On'])

    @attr(series=True)
    def test019_filter_by_changed_by(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role changed by

        LIMS-6507
        """
        self.login_page = Login()
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, response)
        self.login_page.logout()
        self.header_page.sleep_tiny()
        self.info('login with role & user {}:{}'.format(payload['username'], payload['password']))
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.header_page.wait_until_page_is_loaded()
        self.header_page.sleep_medium()
        self.header_page.get_roles_page()
        self.header_page.sleep_small()
        random_role_name = self.generate_random_string()
        self.header_page.create_new_role(role_name=random_role_name)
        self.header_page.click_on_table_configuration_button()
        self.base_selenium.click(element='roles_and_permissions:checked_role_changed_by')
        self.base_selenium.click(element='roles_and_permissions:apply_btn')
        self.header_page.sleep_tiny()
        roles_results = self.header_page.filter_user_by(
            filter_element='roles_and_permissions:filter_changed_by',
            filter_text=payload['username'], field_type='drop_down')
        for roles_result in roles_results:
            self.assertIn(payload['username'], roles_result['Changed By'])
