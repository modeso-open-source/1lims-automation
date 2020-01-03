from ui_testing.pages.base_pages import BasePages
from random import randint
import time

class Header(BasePages):
    def __init__(self):
            super().__init__()
            self.base_selenium.wait_until_page_url_has(text='dashboard')
            self.user_url = "{}users".format(self.base_selenium.url)

    def get_users_page(self):
            self.base_selenium.LOGGER.info(' + Get users page.')
            self.base_selenium.get(url=self.user_url)
            self.sleep_small()

    def get_random_user(self):
            row = self.get_random_user_row()
            self.open_edit_page(row=row)

    def get_random_user_row(self):
            return self.get_random_table_row(table_element='user_management:user_table')


    def click_on_header_button(self):
            self.base_selenium.LOGGER.info('Press on the header button')
            self.base_selenium.click(element='header:header_button')
            self.sleep_small()

    def click_on_user_management_button(self):
            self.base_selenium.LOGGER.info('Press on the user management button')
            self.base_selenium.click(element='header:user_management_button')
            self.sleep_small()

    def archive_selected_users(self):
            self.base_selenium.scroll()
            self.base_selenium.click(element='user_management:right_menu')
            self.base_selenium.click(element='user_management:archive')
            self.confirm_popup()

    def get_archived_users(self):
            self.base_selenium.scroll()
            self.base_selenium.click(element='user_management:right_menu')
            self.base_selenium.click(element='user_management:archived')
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

    def restore_selected_user(self):
            self.base_selenium.scroll()
            self.base_selenium.click(element='user_management:right_menu')
            self.base_selenium.click(element='user_management:restore')
            self.confirm_popup()

    def get_active_users(self):
            self.base_selenium.scroll()
            self.base_selenium.click(element='user_management:right_menu')
            self.base_selenium.click(element='user_management:active')
            self.sleep_small()


    def create_new_user(self, user_role='', sleep=True, user_email='', user_password='', user_confirm_password='', user_name='', user_contact=''):
        self.base_selenium.LOGGER.info(' + Create new user.')
        self.base_selenium.click(element='user_management:create_user_button')
        time.sleep(self.base_selenium.TIME_SMALL)
        self.set_user_name(user_name)
        self.set_user_email(user_email)
        self.set_user_role(user_role)
        self.set_user_password(user_password)
        self.set_user_confirm_password(user_confirm_password)
        created_user_contact=''
        if user_role == 'Contact':
            created_user_contact=self.set_contact(contact=user_contact)

        user_data = {
            "user_name":self.get_user_name(),
            "user_email":self.set_user_email,
            "user_role": self.get_user_role(),
            "user_password": self.get_user_password(),
            "user_confirm_password": self.get_user_confirm_password(),
            "user_contact": created_user_contact
        }
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
                return self.get_user_role()
            else:
                self.base_selenium.select_item_from_drop_down(element='user_management:user_role', item_text=user_role)

    def click_on_filter_view(self):
            self.base_selenium.LOGGER.info('Press on the filter view button')
            self.base_selenium.click(element='general:menu_filter_view')
            self.sleep_small()

    def click_on_filter_user_name(self):
            self.base_selenium.LOGGER.info('Enter user name in the filter field')
            self.base_selenium.click(element='user_management:filter_')
            self.sleep_small()

    def get_user_edit_page(self, name):
            user = self.search(value=name)[0]
            self.open_edit_page(row=user)

    def filter_user_by(self, filter_element, filter_text, field_type='text'):
        self.base_selenium.LOGGER.info(
            ' + Filter by {} : {}'.format(filter_element.replace('user:filter_', '').replace('_', ' '), filter_text))
        self.filter_by(filter_element=filter_element, filter_text=filter_text, field_type=field_type)
        self.filter_apply()



    def get_created_on_filter(self):
        return self.base_selenium.get_value(element='order:test_date')

    def set_created_on_filter(self, date=''):
        if not date:
            date = self.get_random_date()
        self.base_selenium.set_text(element='user_management:user_created_on', value=date)
        return date

    def filter_reset_btn(self):
            self.base_selenium.LOGGER.info('Press on the filter reset button button')
            self.base_selenium.click(element='user_management:filter_reset_btn')
            self.sleep_small()

    def filter_by(self, filter_element, filter_text, field_type='drop_down'):
        if field_type == 'drop_down':
            self.base_selenium.select_item_from_drop_down(element=filter_element, item_text=filter_text)
        else:
            self.base_selenium.set_text(element=filter_element, value=filter_text)

    def click_create_new_user(self):
            self.base_selenium.LOGGER.info('Press on the create new user button')
            self.base_selenium.click(element='user_management:create_user_button')
            self.sleep_small()

    def clear_user_role(self):
        self.base_selenium.LOGGER.info('Clear selected role')
        self.base_selenium.clear_items_in_drop_down(element='user_management:user_role')

    def clear_user_name(self):
        self.base_selenium.LOGGER.info('Clear user name')
        self.base_selenium.clear_text(element='user_management:user_name')

    def clear_user_email(self):
        self.base_selenium.LOGGER.info('Clear user email')
        self.base_selenium.clear_text(element='user_management:user_email')

    def click_on_the_confirm_message(self):
        self.base_selenium.LOGGER.info('Press on ok button')
        self.base_selenium.click(element='general:confirm_pop')
        self.sleep_small()

    def click_on_delete_button(self):
        self.base_selenium.LOGGER.info('Press on the delete button')
        self.base_selenium.click(element='user_management:delete')
        self.sleep_small()

    def click_on_user_right_menu(self):
        self.base_selenium.LOGGER.info('Press on the right menu')
        self.base_selenium.click(element='user_management:right_menu')
        self.sleep_small()

    def click_on_overview_btn(self):
        self.base_selenium.LOGGER.info('Press on the overview button button')
        self.base_selenium.click(element='user_management:overview_btn')
        self.sleep_small()

    def click_on_clear_all(self):
        self.base_selenium.LOGGER.info('Press on the overview button')
        self.base_selenium.click(element='user_management:clear_all')
        self.sleep_small()

    def set_contact(self, contact=''):
        self.base_selenium.LOGGER.info(
            'Set contact to be "{}", if it is empty, then it will be random'.format(contact))
        if contact:
            self.base_selenium.select_item_from_drop_down(
                element='user_management:contact_field', item_text=contact)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='user_management:contact_field')
        return self.get_contact()

    def get_contact(self):
        self.base_selenium.LOGGER.info('Get user contact')
        return self.base_selenium.get_text(element='user_management:contact_field').split('\n')[0]










