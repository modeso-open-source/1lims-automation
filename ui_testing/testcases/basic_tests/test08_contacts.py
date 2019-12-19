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

    def test_003_upadte_contact(self):
        """
        New: Contact: Edit Approach: I can update any contact record 
        I can edit in step one or two & this update should saved successfully 

        LIMS-3564
        """
        
        self.base_selenium.LOGGER.info('Select random table row')
        self.contact_page.get_random_contact()
        self.contact_page.sleep_tiny()

        self.base_selenium.LOGGER.info('updating contact with newrandom data')
        contact_data_before_refresh = self.contact_page.create_update_contact(create=False)

        self.base_selenium.LOGGER.info('Refresh the page to make sure that data updated successfully')
        self.base_selenium.refresh()
        
        contact_data_after_refresh = self.contact_page.get_full_contact_data()

        self.base_selenium.LOGGER.info('Compare Contact before refresh and after refresh')

        self.base_selenium.LOGGER.info('contact no is {}, and it should be {}'.format(contact_data_after_refresh['no'], contact_data_before_refresh['no']) )
        self.assertEqual(contact_data_after_refresh['no'], contact_data_before_refresh['no'])

        self.base_selenium.LOGGER.info('contact name is {}, and it should be {}'.format(contact_data_after_refresh['name'], contact_data_before_refresh['name']) )
        self.assertEqual(contact_data_after_refresh['name'], contact_data_before_refresh['name'])

        self.base_selenium.LOGGER.info('contact address is {}, and it should be {}'.format(contact_data_after_refresh['address'], contact_data_before_refresh['address']) )
        self.assertEqual(contact_data_after_refresh['address'], contact_data_before_refresh['address'])

        self.base_selenium.LOGGER.info('contact postalcode is {}, and it should be {}'.format(contact_data_after_refresh['postalcode'], contact_data_before_refresh['postalcode']) )
        self.assertEqual(contact_data_after_refresh['postalcode'], contact_data_before_refresh['postalcode'])

        self.base_selenium.LOGGER.info('contact location is {}, and it should be {}'.format(contact_data_after_refresh['location'], contact_data_before_refresh['location']) )
        self.assertEqual(contact_data_after_refresh['location'], contact_data_before_refresh['location'])
        
        self.base_selenium.LOGGER.info('contact country is {}, and it should be {}'.format(contact_data_after_refresh['country'], contact_data_before_refresh['country']) )
        self.assertEqual(contact_data_after_refresh['country'], contact_data_before_refresh['country'])

        self.base_selenium.LOGGER.info('contact email is {}, and it should be {}'.format(contact_data_after_refresh['email'], contact_data_before_refresh['email']) )
        self.assertEqual(contact_data_after_refresh['email'], contact_data_before_refresh['email'])

        self.base_selenium.LOGGER.info('contact phone is {}, and it should be {}'.format(contact_data_after_refresh['phone'], contact_data_before_refresh['phone']) )
        self.assertEqual(contact_data_after_refresh['phone'], contact_data_before_refresh['phone'])

        self.base_selenium.LOGGER.info('contact skype is {}, and it should be {}'.format(contact_data_after_refresh['skype'], contact_data_before_refresh['skype']) )
        self.assertEqual(contact_data_after_refresh['skype'], contact_data_before_refresh['skype'])

        self.base_selenium.LOGGER.info('contact website is {}, and it should be {}'.format(contact_data_after_refresh['website'], contact_data_before_refresh['website']) )
        self.assertEqual(contact_data_after_refresh['website'], contact_data_before_refresh['website'])        

        self.base_selenium.LOGGER.info('contact departments is {}, and it should be {}'.format(contact_data_after_refresh['departments'], contact_data_before_refresh['departments']) )
        self.assertEqual(contact_data_after_refresh['departments'], contact_data_before_refresh['departments'])

        self.base_selenium.LOGGER.info('contact contact_type is {}, and it should be {}'.format(contact_data_after_refresh['contact_type'], contact_data_before_refresh['contact_type']) )
        self.assertEqual(contact_data_after_refresh['contact_type'], contact_data_before_refresh['contact_type'])
    
    def test_004_search_by_any_field(self):
        """
        New: Contacts: Search Approach: I can search by any field in the table view 
        I can search by any field in the table view 

        LIMS-3573
        """
        
        row = self.contact_page.get_random_contact_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.article_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])
        