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

    
    def test_002_create_contact(self):
        """
        New: Contact: Creation Approach: I can create new contact successfully
        User can create new conatcts successfully 

        LIMS-3563
        """
        
        self.base_selenium.LOGGER.info('Creating new contact')
        contact_data = self.contact_page.create_update_contact()

        self.base_selenium.LOGGER.info('comparing contact\'s data with the first record in contact page')
        self.base_selenium.LOGGER.info('to make sure that when new record is created is set to the be the first record in the page')

        created_contact_record = self.contact_page.result_table()[0]
        first_contact_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_contact_record)

        self.base_selenium.LOGGER.info('contact no is {}, and it should be {}'.format(first_contact_data['Contact No'], contact_data['no']) )
        self.assertEqual(first_contact_data['Contact No'], contact_data['no'])

        self.base_selenium.LOGGER.info('contact name is {}, and it should be {}'.format(first_contact_data['Contact Name'], contact_data['name']) )
        self.assertEqual(first_contact_data['Contact Name'], contact_data['name'])

        self.base_selenium.LOGGER.info('contact address is {}, and it should be {}'.format(first_contact_data['Address'], contact_data['address']) )
        self.assertEqual(first_contact_data['Address'], contact_data['address'])

        self.base_selenium.LOGGER.info('contact address is {}, and it should be {}'.format(first_contact_data['Address'], contact_data['address']) )
        self.assertEqual(first_contact_data['Address'], contact_data['address'])

        self.base_selenium.LOGGER.info('contact postalcode is {}, and it should be {}'.format(first_contact_data['Postal Code'], contact_data['postalcode']) )
        self.assertEqual(first_contact_data['Postal Code'], contact_data['postalcode'])


        self.base_selenium.LOGGER.info('contact location is {}, and it should be {}'.format(first_contact_data['Location'], contact_data['location']) )
        self.assertEqual(first_contact_data['Location'], contact_data['location'])

        self.base_selenium.LOGGER.info('contact location is {}, and it should be {}'.format(first_contact_data['Location'], contact_data['location']) )
        self.assertEqual(first_contact_data['Location'], contact_data['location'])

        
        self.base_selenium.LOGGER.info('contact country is {}, and it should be {}'.format(first_contact_data['Country'], contact_data['country']) )
        self.assertEqual(first_contact_data['Country'], contact_data['country'])

        self.base_selenium.LOGGER.info('contact email is {}, and it should be {}'.format(first_contact_data['Email'], contact_data['email']) )
        self.assertEqual(first_contact_data['Email'], contact_data['email'])

        self.base_selenium.LOGGER.info('contact phone is {}, and it should be {}'.format(first_contact_data['Phone'], contact_data['phone']) )
        self.assertEqual(first_contact_data['Phone'], contact_data['phone'])

        self.base_selenium.LOGGER.info('contact skype is {}, and it should be {}'.format(first_contact_data['Skype'], contact_data['skype']) )
        self.assertEqual(first_contact_data['Skype'], contact_data['skype'])

        self.base_selenium.LOGGER.info('contact website is {}, and it should be {}'.format(first_contact_data['Website'], contact_data['website']) )
        self.assertEqual(first_contact_data['Website'], contact_data['website'])        

        self.base_selenium.LOGGER.info('contact departments is {}, and it should be {}'.format(first_contact_data['Departments'], contact_data['departments']) )
        self.assertEqual(first_contact_data['Departments'], contact_data['departments'])

        self.base_selenium.LOGGER.info('contact contact_type is {}, and it should be {}'.format(first_contact_data['Type'], contact_data['contact_type']) )
        self.assertEqual(first_contact_data['Type'], contact_data['contact_type'])
        