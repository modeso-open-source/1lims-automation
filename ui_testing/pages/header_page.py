from ui_testing.pages.base_pages import BasePages
from random import randint
import time


class Header(BasePages):
    def __init__(self):
        super().__init__()
        # self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.user_url = "{}users".format(self.base_selenium.url)
        self.role_url = "{}roles".format(self.base_selenium.url)

    def get_users_page(self):
        self.info(' + Get users page.')
        self.base_selenium.get(url=self.user_url)
        self.wait_until_page_is_loaded()

    def get_random_user(self):
        row = self.get_random_user_row()
        self.open_edit_page(row=row)
        self.sleep_small()

    def get_random_user_row(self):
        return self.get_random_table_row(table_element='user_management:user_table')

    def click_on_header_button(self):
        self.info('Press on the header button')
        self.base_selenium.click(element='header:header_button')
        self.sleep_small()

    def archive_entity(self, menu_element, archive_element):
        self.base_selenium.scroll()
        self.base_selenium.click(element=menu_element)
        self.base_selenium.click(element=archive_element)
        self.confirm_popup()

    def get_archived_entities(self, menu_element, archived_element):
        self.base_selenium.scroll()
        self.base_selenium.click(element=menu_element)
        self.base_selenium.click(element=archived_element)
        self.sleep_small()

    def is_user_in_table(self, value):
        """
            - get_archived_users then call me to check if the user has been archived.
            - get_active_users then call me to check if the user is active.
        :param value: search value
        :return:
        """
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def restore_entity(self, menu_element, restore_element):

        self.base_selenium.scroll()
        self.base_selenium.click(element=menu_element)
        self.base_selenium.click(element=restore_element)
        self.confirm_popup()

    def get_active_entities(self, menu_element, active_element):
        self.base_selenium.scroll()
        self.base_selenium.click(element=menu_element)
        self.base_selenium.click(element=active_element)
        self.sleep_small()

    def create_new_user(self, user_role='', sleep=True, user_email='', user_password='', user_confirm_password='',
                        user_name='', contact=''):
        self.base_selenium.LOGGER.info(' + Create new user.')
        self.base_selenium.click(element='user_management:create_user_button')
        self.sleep_small()
        user_name = self.set_user_name(user_name)
        user_email = self.set_user_email(user_email)
        user_role = self.set_user_role(user_role)
        user_password = self.set_user_password(user_password)
        user_confirm_password = self.set_user_confirm_password(user_confirm_password)
        user_data = {
            "user_name": user_name,
            "user_email": user_email,
            "user_role": user_role,
            "user_password": user_password,
            "user_confirm_password": user_confirm_password,
        }
        if contact:
            user_contact = self.set_contact(contact)
            user_data.update({"user_contact": user_contact})

        self.save(sleep)
        return user_data

    def set_user_name(self, user_name):
        self.base_selenium.set_text(element='user_management:user_name', value=user_name)

    def get_user_name(self):
        return self.base_selenium.get_text(element='user_management:user_name').split('\n')[0]

    def set_user_number(self, user_number):
        self.base_selenium.set_text(element="user_management:user_number", value=user_number)

    def get_user_number(self):
        return self.base_selenium.get_text(element='user_management:user_number').split('\n')[0]

    def set_user_email(self, user_email=''):
        self.generate_random_email()
        self.base_selenium.set_text(element="user_management:user_email", value=user_email)
        return user_email

    def get_user_email(self):
        return self.base_selenium.get_value(element="user_management:user_email")

    def set_user_password(self, user_password):
        self.base_selenium.set_text(element="user_management:user_password", value=user_password)

    def get_user_password(self):
        return self.base_selenium.get_text(element='user_management:user_password').split('\n')[0]

    def set_user_confirm_password(self, user_confirm_password):
        self.base_selenium.set_text(element="user_management:user_confirm_password", value=user_confirm_password)

    def get_user_confirm_password(self):
        return self.base_selenium.get_text(element='user_management:user_confirm_password').split('\n')[0]

    def get_user_role(self):
        return self.base_selenium.get_text(element='user_management:user_role').split('\n')[0]

    def set_user_role(self, user_role='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='user_management:user_role', avoid_duplicate=True)

        else:
            self.base_selenium.select_item_from_drop_down(element='user_management:user_role', item_text=user_role)
            return self.get_user_role()

    def get_user_edit_page(self, name):
        user = self.search(value=name)[0]
        self.open_edit_page(row=user)

    def filter_user_by(self, filter_element, filter_text, field_type='text'):
        self.open_filter_menu()
        self.info(
            ' + Filter by {} : {}'.format(filter_element.replace('user:filter_', '').replace('_', ' '), filter_text))
        self.filter_by(filter_element=filter_element, filter_text=filter_text, field_type=field_type)
        self.filter_apply()
        self.sleep_tiny()
        return self.get_the_latest_row_data()

    def filter_user_drop_down(self, filter_name, filter_text, field_type='drop_down'):
        self.open_filter_menu()

        self.info(' + Filter by user : {}'.format(filter_text))
        self.filter_by(filter_element=filter_name, filter_text=filter_text)
        self.filter_apply()
        self.sleep_tiny()
        return self.get_table_rows_data()[0]

    def get_data_from_row(self):

        user_row = self.get_random_table_row(table_element='general:table')
        user_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=user_row)
        return {
            'created_on': user_row_data['Created On'].split(',')[0],
            'changed_by': user_row_data['Changed By'],
            'number': user_row_data['No'],
            'role': user_row_data['Role'],
            'email': user_row_data['Email'],
            'name': user_row_data['Name'],
        }

    def get_created_on_filter(self):
        return self.base_selenium.get_value(element='order:test_date')

    def set_created_on_filter(self, date=''):
        if not date:
            date = self.get_random_date()
        self.base_selenium.set_text(element='user_management:user_created_on', value=date)
        return date

    def clear_user_role(self):
        self.info('Clear selected role')
        self.base_selenium.clear_items_in_drop_down(element='user_management:user_role')

    def clear_user_name(self):
        self.info('Clear user name')
        self.base_selenium.clear_text(element='user_management:user_name')

    def clear_user_email(self):
        self.info('Clear user email')
        self.base_selenium.clear_text(element='user_management:user_email')

    def click_on_the_confirm_message(self):
        self.info('Press on ok button')
        self.base_selenium.click(element='general:confirm_pop')
        self.sleep_small()

    def click_on_overview_btn(self):
        self.info('Press on the overview button button')
        self.base_selenium.click(element='user_management:overview_btn')
        self.sleep_small()

    def click_create_new_user(self):
        self.info('Press on the create new user button')
        self.base_selenium.click(element='user_management:create_user_button')
        self.sleep_small()

    def is_role_in_table(self, value):
        """
            - get_archived_roles then call me to check if the role has been archived.
            - get_active_roles then call me to check if the role is active.
        :param value: search value
        :return:
        """
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def get_random_role(self):
        row = self.get_random_user_row()
        self.open_edit_page(row=row)

    def get_random_role_row(self):
        return self.get_random_table_row(table_element='roles_and_permissions:user_table')

    def get_roles_page(self):
        self.info(' + Get roles page.')
        self.base_selenium.get(url=self.role_url)
        self.sleep_small()

    def set_role_name(self, role_name):
        self.base_selenium.set_text(element='roles_and_permissions:role_name', value=role_name)

    def get_role_name(self):
        return self.base_selenium.get_text(element='roles_and_permissions:role_name').split('\n')[0]

    def create_new_role(self, sleep=True, role_name=''):
        self.info(' + Create new role.')
        self.base_selenium.click(element='roles_and_permissions:new_role_btn')
        time.sleep(self.base_selenium.TIME_SMALL)
        role_name = self.set_role_name(role_name)

        role_data = {
            "role_name": role_name,
        }
        self.save(sleep)
        return role_data

    def clear_role_name(self):
        self.info('Clear role name')
        self.base_selenium.clear_text(element='roles_and_permissions:role_name')

    def click_on_roles_permissions_button(self):
        self.info('Press on the roles and permissions button')
        self.base_selenium.click(element='header:roles_and_permissions_button')
        self.sleep_small()

    def click_on_pagination_page(self):
        self.info('click on the pagination page')
        self.base_selenium.click(element='roles_and_permissions:pagination_page')
        self.sleep_small()

    def click_on_master_data_permissions(self):
        self.info('checked master data permissions')
        self.base_selenium.click(element='roles_and_permissions:master_data_view_permissions')
        self.base_selenium.click(element='roles_and_permissions:master_data_edit_permissions')
        self.sleep_small()

    def create_role_with_mater_data_permissions(self, sleep=True, role_name=''):
        self.info(' + Create new role.')
        self.base_selenium.click(element='roles_and_permissions:new_role_btn')
        self.sleep_small()
        role_name = self.set_role_name(role_name)
        self.click_on_master_data_permissions()

        role_data = {
            "role_name": role_name,

        }
        self.save(sleep)
        return role_data

    def click_on_user_management_button(self):
        self.info('Press on the user management button')
        self.base_selenium.click(element='header:user_management_button')
        self.sleep_small()

    def click_on_sample_management_permissions(self):
        self.info('Press on logout button')
        self.base_selenium.click(element='roles_and_permissions:order_view_permissions')
        self.base_selenium.click(element='roles_and_permissions:order_edit_permissions')
        self.base_selenium.click(element='roles_and_permissions:analysis_view_permissions')
        self.base_selenium.click(element='roles_and_permissions:analysis_edit_permissions')
        self.sleep_small()

    def create_role_with_sample_management_permissions(self, sleep=True, role_name=''):
        self.info(' + Create new role.')
        self.base_selenium.click(element='roles_and_permissions:new_role_btn')
        self.sleep_small()
        role_name = self.set_role_name(role_name)
        self.click_on_sample_management_permissions()

        role_data = {
            "role_name": role_name,

        }
        self.save(sleep)
        return role_data

    def set_contact(self, contact=''):
        self.info(
            'Set contact to be "{}", if it is empty, then it will be random'.format(contact))
        if contact:
            self.base_selenium.select_item_from_drop_down(
                element='user_management:contact_field', item_text=contact)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='user_management:contact_field')
        return self.get_contact()

    def get_contact(self):
        self.info('Get user contact')
        return self.base_selenium.get_text(element='user_management:contact_field').split('\n')[0]

    def click_on_reset_btn(self):
        self.info('click on the reset button')
        self.base_selenium.click(element='roles_and_permissions:reset_btn')
        self.sleep_small()

    # this function should be used in case all the fields in the table configuration checked
    def get_role_data_from_fully_checked_headers_random_row(self):

        role_row = self.get_random_table_row(table_element='general:table')
        role_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=role_row)
        random_role_data_to_return = {
            'created_on': role_row_data['Created On'].split(',')[0],
            'changed_by': role_row_data['Changed By'],
            'number': role_row_data['No'],
            'name': role_row_data['Name'],
        }

        return random_role_data_to_return

    def click_on_user_management(self):
        self.info('click on the user management button')
        self.base_selenium.click(element='header:user_management_button')
        self.sleep_small()

    def click_on_table_configuration_button(self):
        self.info('click on the table configuration button')
        self.base_selenium.click(element='roles_and_permissions:configure_table_btn')
        self.sleep_small()

    def get_last_role_row(self):
        rows = self.result_table()
        return rows[0]

    def click_on_user_config_btn(self):
        self.info('click on the table configuration button')
        self.base_selenium.click(element='user_management:config_table')
        self.sleep_small()

    def checked_user_changed_by(self):
        self.info(
            'checked the changed by field from the table configuration to display in the active table ')
        self.base_selenium.click(element='user_management:checked_changed_by')
        self.sleep_small()

    def delete_entity(self):
        self.info(
            ' press on the delete button ')
        self.base_selenium.click(element='user_management:right_menu')
        self.base_selenium.click(element='user_management:delete')
        self.confirm_popup()
        self.sleep_small()

    def get_last_user_row(self):
        rows = self.result_table()
        return rows[0]

    def get_role_edit_page_by_id(self, id):
        url_text = "{}roles/edit/" + str(id)
        self.base_selenium.get(url=url_text.format(self.base_selenium.url))
        self.wait_until_page_is_loaded()

    def filter_role_by_no(self, filter_text):
        self.info('Filter by Role number {}'.format(filter_text))
        self.open_filter_menu()
        self.filter_by(filter_element='roles_and_permissions:filter_no', filter_text=filter_text, field_type='text')
        self.filter_apply()
        self.sleep_tiny()
        return self.get_the_latest_row_data()
