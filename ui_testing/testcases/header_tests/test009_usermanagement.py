from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.header_page import Header
from ui_testing.pages.login_page import Login
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.roles_api import RolesAPI
from parameterized import parameterized
import re, random
from unittest import skip
from nose.plugins.attrib import attr


class HeaderTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.header_page = Header()
        self.user_api = UsersAPI()
        self.roles_api = RolesAPI()
        self.set_authorization(auth=self.roles_api.AUTHORIZATION_RESPONSE)
        self.header_page.get_users_page()
        self.header_page.set_all_configure_table_columns_to_specific_value()

    def test001_archive_user_management(self):
        """
        User management: Make sure that you can archive any record

        LIMS-6379
        """
        self.info("select random users rows")
        selected_user_management_data, _ = self.header_page.select_multiple_random_users_rows()
        self.info("Archive selected rows")
        self.header_page.archive_entity(menu_element='user_management:right_menu',
                                        archive_element='user_management:archive')
        self.info("Navigate to archived users")
        self.header_page.get_archived_entities(menu_element='user_management:right_menu',
                                               archived_element='user_management:archived')
        for user in selected_user_management_data:
            user_name = user['Name']
            self.info('{} user should be activated.'.format(user_name))
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))

    def test002_restore_user(self):
        """
        User management: Restore Approach: Make sure that you can restore any record successfully

        LIMS-6380
        """
        user_names = []
        self.info("Navigate to archived users")
        self.header_page.get_archived_entities(menu_element='user_management:right_menu',
                                               archived_element='user_management:archived')
        self.info("Select random archived users rows")
        selected_user_data, _ = self.header_page.select_multiple_random_users_rows()
        self.assertTrue(selected_user_data, 'No archived users found')
        for user in selected_user_data:
            user_names.append(user['Name'])

        self.info("Restore selected rows")
        self.header_page.restore_entity(menu_element='user_management:right_menu',
                                        restore_element='user_management:restore')
        self.header_page.get_active_entities(menu_element='user_management:right_menu',
                                             active_element='user_management:active')
        for user_name in user_names:
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))

    #@skip("https://modeso.atlassian.net/browse/LIMSA-199")
    def test003_user_search(self):
        """
        Header:  User management:  Search Approach: Make sure that you can search by
        any field in the active table successfully

        LIMS-6082
        """
        self.info("select random row and search by its data")
        row = self.header_page.get_random_user_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) \
                    or row_data[column] == '' or row_data[column] == '-':
                continue
            self.info('search for {} : {}'.format(column, row_data[column]))
            search_results = self.header_page.search(row_data[column])
            self.assertGreater(len(search_results), 1,
                               " * There is no search results for {}, Report a bug.".format(row_data[column]))
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test004_download_user_sheet(self):
        """
        User management: Make sure you can export all the data in
        the active table & it should display in the same order

        LIMS-6101
        """
        self.header_page.download_xslx_sheet()
        rows_data = list(filter(None, self.header_page.get_table_rows_data()))
        for index in range(len(rows_data)):
            self.info('comparing the user no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.header_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    def test005_delete_user(self):
        """
        User management : Delete Approach: Make sure that you can delete
        any record successfully If this record not used in any other entity

        LIMS-6381
        """
        self.info("create new user")
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        new_user_name = response['user']['username']
        self.header_page.search(value=new_user_name)
        self.header_page.select_all_records()
        self.header_page.archive_entity(menu_element='user_management:right_menu',
                                        archive_element='user_management:archive')
        self.header_page.get_archived_entities(menu_element='user_management:right_menu',
                                               archived_element='user_management:archived')
        self.info('make sure that that the user record navigate to the archive table')
        self.assertTrue(self.header_page.search(value=new_user_name))
        self.header_page.select_all_records()
        self.header_page.delete_entity()
        result = self.header_page.search(value=new_user_name)
        self.assertEqual(result[0].get_attribute("textContent"), 'No data available in table')
        self.info('deleted successfully')

    def test006_create_new_user(self):
        """
        Header: User management Approach:  Make sure that I can create new user successfully

        LIMS-6000
        """
        random_user_name = self.generate_random_string()
        random_user_email = self.header_page.generate_random_email()
        self.header_page.create_new_user(
            user_name=random_user_name, user_email=random_user_email,
            user_password='1', user_confirm_password='1')

        self.header_page.sleep_tiny()
        user_row = self.header_page.search(value=random_user_name)
        table_row = self.header_page.result_table()
        self.assertEqual(table_row, user_row)

    def test007_overview_btn_from_create_mode(self):
        """
        User Management: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table

        LIMS-6396
        """
        # from the create mode it will redirect me to the active table
        self.header_page.click_create_new_user()
        self.header_page.click_on_overview_btn()
        self.info('it will redirect me to the active table')
        self.assertEqual(self.base_selenium.get_url(), '{}users'.format(self.base_selenium.url))

    def test008_overview_btn_from_edit_mode(self):
        """
        User Management: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table

        LIMS-6396
        """
        # from the edit mode it will redirect me to the active table
        self.header_page.get_random_user()
        self.header_page.click_on_overview_btn()
        self.info('it will redirect me to the active table')
        self.assertEqual(self.base_selenium.get_url(), '{}users'.format(self.base_selenium.url))

    @parameterized.expand(['save_btn', 'cancel'])
    def test009_update_user_name_with_save_cancel_btn(self, save):
        """
        User management: User management: I can update user name with save & cancel button

        LIMS-6395
        """
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.info('user_url : {}'.format(user_url))
        self.header_page.sleep_tiny()

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
            self.info(
                'Assert {} (new_name) == {} (user_name)'.format(new_name, user_name))
            self.assertEqual(new_name, user_name)
        else:
            self.info(
                'Assert {} (current_name) == {} (user_name)'.format(current_name, user_name))
            self.assertEqual(current_name, user_name)

    @parameterized.expand(['save_btn', 'cancel'])
    def test010_update_user_role_with_save_cancel_btn(self, save):
        """
        User management: I can update user role with save & cancel button

        LIMS-6398
        """
        # open random user in the edit mode
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.info('user_url : {}'.format(user_url))
        self.header_page.sleep_tiny()
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
            self.info(
                'Assert {} (new_role) == {} (user_role)'.format(new_role, user_role))
            self.assertEqual(new_role, user_role)
        else:
            self.info(
                'Assert {} (current_role) == {} (user_role)'.format(current_role, user_role))
            self.assertEqual(current_role, user_role)

    @parameterized.expand(['save_btn', 'cancel'])
    def test011_update_user_email_with_save_cancel_btn(self, save):
        """
        User management: I can update user email with save & cancel button

        LIMS-6397
        """
        # open random user in the edit mode
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.info('user_url : {}'.format(user_url))
        self.header_page.sleep_tiny()
        current_email = self.header_page.get_user_email()
        new_email = self.header_page.generate_random_email()
        self.header_page.set_user_email(new_email)
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

            self.base_selenium.get(
                url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_email = self.header_page.get_user_email()
        if 'save_btn' == save:
            self.info(
                'Assert {} (new_email) == {} (user_email)'.format(new_email, user_email))
            self.assertEqual(new_email, user_email)
        else:
            self.info(
                'Assert {} (current_email) == {} (user_email)'.format(current_email, user_email))
            self.assertEqual(current_email, user_email)

    def test012_validation_user_name_email_fields(self):
        """
        Header: User management: Make sure when the user update name & email then press on save button,
        red border display and he can't save

        LIMS-6121
        """
        # from the create mode it will redirect me to the active table
        self.header_page.get_random_user()
        self.header_page.clear_user_name()
        self.header_page.clear_user_email()
        self.header_page.save(save_btn='user_management:save_btn')
        self.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert error msg')
        self.assertEqual(validation_result, True)

    @parameterized.expand([('name', 'filter_name', 'Name'),
                           ('email', 'filter_email', 'Email'),
                           ('number', 'filter_number', 'No'),
                           ('created_on', 'filter_created_on', 'Created On')])
    def test013_filter_by_text_field(self, field, filter_elem, header):
        """
        User management Approach: I can filter by name, email, number and created on successfully

        LIMS-6002
        LIMS-6442
        LIMS-6488
        LIMS-6486
        """
        self.header_page.sleep_tiny()
        filter_data = self.header_page.get_data_from_row()[field]
        self.info(" filter by  {}".format(filter_data))
        user_results = self.header_page.filter_user_by(filter_element='user_management:{}'.format(filter_elem),
                                                       filter_text=filter_data)
        for user_result in user_results:
            self.assertEqual(user_result[header].replace("'", ""), filter_data.replace("'", ""))

    def test014_filter_by_role(self):
        """
        User management Approach: I can filter by user role successfully

        LIMS-6443
        """
        self.info('get random role')
        res, _ = self.roles_api.get_all_roles(limit=50)
        random_role = random.choice(res['roles'])
        self.info(f'random role id: {random_role["id"]}')

        self.info('create random user')
        payload = {
            'role': {
                'id': random_role['id'],
                'text': random_role['name']
            },
            'roleId': random_role['id']
        }
        response, payload = self.user_api.create_new_user(**payload)

        user_results = self.header_page.filter_user_by(filter_element='user_management:filter_role',
                                                       filter_text=random_role['name'], field_type='drop_down')
        usernames = []
        for user_result in user_results:
            self.assertEqual(user_result["Role"], random_role['name'])
            usernames.append(user_result['Name'])

        self.assertIn(response['user']['username'], usernames)

    @skip('https://modeso.atlassian.net/browse/LIMS-6624')
    def test015_cant_create_two_users_with_the_same_name(self):
        """
        User management: Can't create two users with the same name

        LIMS-6503
        """
        # create new user with random data
        random_user_name = self.generate_random_string()
        random_user_email = self.header_page.generate_random_email()
        self.header_page.create_new_user(user_name=random_user_name, user_email=random_user_email,
                                         user_role='Admin', user_password='1', user_confirm_password='1')

        self.info('search to make sure that the role created '.format(random_user_name))
        created_user = self.header_page.search(random_user_name)[0]
        user_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_user)
        self.assertTrue(created_user, user_data)

        # create role with the same name
        self.header_page.create_new_user(user_name=random_user_name, user_email=random_user_email,
                                         user_role='Admin', user_password='1', user_confirm_password='1')
        self.info('waiting fo validation message appear when I enter two users with the same name')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert the error message to make sure that validation when '
                  'I enter two users with the same name? {}'.format(validation_result))
        self.assertTrue(validation_result)


class LoginRandomUser(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.header_page = Header()
        self.roles_api = RolesAPI()
        self.login_page.base_selenium.refresh()
        self.login_page.logout()
        response, payload = UsersAPI().create_new_user()

        self.user_name = response['user']['username']
        self.info("login with new user {} and pw {}".format(self.user_name, payload['password']))

        self.login_page.login(username=self.user_name, password=payload['password'])
        self.header_page.wait_until_page_is_loaded()
        self.header_page.get_users_page()

    def tearDown(self):
        self.set_authorization(auth=self.roles_api.AUTHORIZATION_RESPONSE)
        super().tearDown()

    @attr(series=True)
    def test016_delete_user_used_in_other_entity(self):
        """
        User management: Make sure that you can't delete any user record If this record used in other entity

        LIMS-6407
        """
        last_row = self.header_page.get_last_user_row()
        self.header_page.click_check_box(source=last_row)
        self.header_page.archive_entity(menu_element='user_management:right_menu',
                                        archive_element='user_management:archive')
        self.header_page.get_archived_entities(menu_element='user_management:right_menu',
                                               archived_element='user_management:archived')

        last_row = self.header_page.get_last_user_row()
        self.header_page.click_check_box(source=last_row)
        self.header_page.delete_entity()
        self.assertTrue(self.base_selenium.element_is_displayed(element='general:confirmation_pop_up'))

    @attr(series=True)
    def test017_filter_by_changed_by(self):
        """
        Header: Roles & Permissions Approach: Make sure that you can filter by role changed by

        LIMS-6507
        """
        new_user = self.generate_random_string()
        new_email = self.header_page.generate_random_email()
        self.header_page.create_new_user(user_name=new_user, user_email=new_email,
                                         user_role='Admin', user_password='1', user_confirm_password='1')

        self.header_page.click_on_user_config_btn()
        self.base_selenium.click(element='user_management:checked_changed_by')
        self.base_selenium.click(element='user_management:apply_btn')

        self.header_page.sleep_tiny()
        user_results = self.header_page.filter_user_by(filter_element='user_management:filter_changed_by',
                                                       filter_text=self.user_name, field_type='drop_down')

        self.assertEqual(self.user_name, user_results[0]['Changed By'])