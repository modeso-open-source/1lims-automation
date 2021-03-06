from ui_testing.pages.base_pages import BasePages
from random import randint


class Contacts(BasePages):
    def __init__(self):
        super().__init__()
        self.contacts_url = "{}contacts".format(self.base_selenium.url)

    def get_contacts_page(self):
        self.base_selenium.get(url=self.contacts_url)
        self.wait_until_page_is_loaded()

    def archive_contact(self, name='', random=False, force=True):
        if not random:
            contact = self.search(value=name)[0]
            if contact is not None:
                contact_archive_button = self.base_selenium.find_element_in_element(source=contact,
                                                                                    destination_element='articles:article_archive_button')
                contact_archive_button.click()
                self.base_selenium.click(element='articles:article_archive_dropdown')
                if force:
                    self.base_selenium.click(element='articles:confirm_archive')
                else:
                    self.base_selenium.click(element='articles:cancel_archive')
                self.sleep_medium()

    def get_random_contact(self):
        row = self.get_random_contact_row()
        self.open_edit_page(row=row)

    def get_random_contact_row(self):
        return self.get_random_table_row(table_element='contacts:contact_table')
        
    def archive_selected_contacts(self):
        self.info("Archive selected contacts")
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archive')
        self.confirm_popup()
        self.sleep_tiny()

    def restore_selected_contacts(self):
        self.info("Restore selected contacts")
        self.base_selenium.scroll()
        self.base_selenium.click(element='articles:right_menu')
        self.base_selenium.click(element='articles:restore')
        self.confirm_popup()
        self.sleep_tiny()

    def is_contact_in_table(self, value):
        """
            - get_archived_contacts then call me to check if the contact has been archived.
            - get_active_contacts then call me to check if the contact is active.
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

    def get_archived_contacts(self):
        self.info("Navigate to archived contacts table")
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archived')
        self.sleep_small()

    def get_active_contacts(self):
        self.info("Navigate to active contacts table")
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:active')
        self.sleep_small()

    def delete_selected_contacts(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:delete')
        self.confirm_popup()

        if self.base_selenium.check_element_is_exist(element='general:cant_delete_message'):
            self.base_selenium.click(element='general:confirm_pop')
            return False
        return True

    def check_if_table_is_empty(self):
        row = self.base_selenium.get_table_rows(element='contacts:contact_table')[0]
        if row.text != '':
            return False
        return True

    def check_delete_message(self):
        msg = self.base_selenium.find_element(element='contacts:delete_contact_msg')
        if msg.text != "You can't Delete this item as it's related to some other data":
            return False
        confirmation_button = self.base_selenium.find_element(element='contacts:confirmation_button')
        if confirmation_button:
            confirmation_button.click()
            return True

    def check_for_hidden_table_fields(self, fields, hidden_fields=['fax', 'id']):
        self.base_selenium.LOGGER.info('check that all fields are shown')
        for field in fields:
            if field['isShownInTable'] == False and field['fieldData']['name'] not in hidden_fields:
                return True

        return False

    def get_mapped_contact_type(self, contact_type):
        types = {'supplier': 'Contact',
                 'client': 'Client',
                 'laboratory': 'Laboratory'}
        return types[contact_type]

    def get_contact_edit_page_by_id(self, id):
        url_text = "{}/contacts/edit/" + str(id)
        self.base_selenium.get(url=url_text.format(self.base_selenium.url))
        self.wait_until_page_is_loaded()

    def filter_by_contact_no(self, contact_no):
        self.open_filter_menu()
        self.info('Filter by contact no. : {}'.format(contact_no))
        self.filter_by(filter_element='contact:contact_no_filter', filter_text=contact_no, field_type='text')
        self.filter_apply()

    def search_find_row_open_edit_page(self, search_text):
        rows = self.search(search_text)
        self.open_edit_page_by_css_selector(row=rows[0])

    def open_contact_configurations_options(self):
        self.base_selenium.click(element='configurations_page:display_options_menu')
        self.sleep_tiny()
        self.base_selenium.click(element='configurations_page:field_options')
        self.sleep_tiny()

    def clear_all_selected_view_and_search_options(self):
        self.info('clear selected view and search options of contact name')
        self.base_selenium.click(element='configurations_page:clear_all')
        self.sleep_tiny()

    def select_option_to_view_search_with(self, view_search_options):
        self.info('change view search options')
        self.clear_all_selected_view_and_search_options()
        for view_search_option in view_search_options:
            if view_search_option != '':
                self.base_selenium.select_item_from_drop_down(element='configurations_page:view_search_ddl',
                                                              item_text=view_search_option.replace('×',''))
        self.base_selenium.click(element='configurations_page:popup_save_button')
        self.sleep_small()
        self.base_selenium.click(element='configurations_page:save_button')
        self.sleep_small()
