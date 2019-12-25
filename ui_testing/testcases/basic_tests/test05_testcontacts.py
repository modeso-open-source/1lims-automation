from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import time


class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.contacts_url = "{}contacts".format(self.base_selenium.url)
        self.contacts_page.get_contacts_page()

    @parameterized.expand(['ok', 'cancel'])
    def test001_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table
        LIMS-6203
        """
        self.base_selenium.LOGGER.info('create new contact.')
        self.base_selenium.click(element='contacts:new_contact')
        time.sleep(5)
        # click on Overview, this will display an alert to the user
        self.base_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.base_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}contacts'.format(self.base_selenium.url))
            self.base_selenium.LOGGER.info('clicking on Overview confirmed')
        else:
            self.base_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}contacts/add'.format(self.base_selenium.url))
            self.base_selenium.LOGGER.info('clicking on Overview cancelled')

    def test002_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202

        New: Contact: Cancel button: After I edit in any field
        then press on cancel button, a pop up will appear that
        the data will be lost
        LIMS-3585
        """
        self.contacts_page.get_random_contact()
        contact_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info('contact_url : {}'.format(contact_url))
        # click on Overview, it will redirect you to contacts' page
        self.base_selenium.LOGGER.info('click on Overview')
        self.base_page.click_overview()
        self.article_page.sleep_small()
        self.assertEqual(self.base_selenium.get_url(), '{}contacts'.format(self.base_selenium.url))
        self.base_selenium.LOGGER.info('clicking on Overview confirmed')







