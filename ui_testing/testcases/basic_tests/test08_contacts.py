from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip


class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.contact_page.get_contacts_page()

    @parameterized.expand(['archive', 'restore'])
    def test_001_archive_restore_contact(self, action):
        """
        New: Contact: Restore/Archive Approach: I can archive/restore any contact successfully
        I can archive/restore any contact successfully
        LIMS-3566
        """
        
        if action == 'restore':
            self.contact_page.get_archived_contacts()

        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        if action == 'archive':
            self.contact_page.archive_selected_contacts()
        elif action == 'restore':
            self.contact_page.restore_selected_contacts()
        if action == 'archive':
            self.contact_page.get_archived_contacts()
        elif action == 'restore':
            self.contact_page.get_active_contacts()

        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            if action == 'archive':
                self.base_selenium.LOGGER.info(' + {} Contact should be archived.'.format(contact_no))
            elif action == 'restore':
                self.base_selenium.LOGGER.info(' + {} Contact should be active.'.format(contact_no))
            self.assertTrue(self.contact_page.is_contact_in_table(value=contact_no))


        
