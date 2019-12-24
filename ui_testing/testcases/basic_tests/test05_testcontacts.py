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
        self.base_selenium.get(url=self.contacts_url)

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






