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

        self.base_selenium.LOGGER.info('contact postalcode is {}, and it should be {}'.format(first_contact_data['Postal Code'], contact_data['postalcode']) )
        self.assertEqual(first_contact_data['Postal Code'], contact_data['postalcode'])

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
        if self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh, data_before_save=contact_data_before_refresh):
            self.base_selenium.LOGGER.info('contact data have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact data was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)

    
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

    def test05_download_contact_sheet(self):
        """
        New: Contact: XSLX File: I can download all the data in the table view in the excel sheet
        I can download all the data in the table view in the excel sheet 

        LIMS:3568
        """
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.contact_page.download_xslx_sheet()
        rows_data = self.contact_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.base_selenium.LOGGER.info(' * Comparing the contact no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.contact_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    def test_06_create_contact_with_person(self):
        contact_data = self.contact_page.create_update_contact()

        self.base_selenium.LOGGER.info('filter by contact no.: {} to get the record'.format(contact_data['no']))
        first_contact_record = self.contact_page.search(value=contact_data['no'])[0]

        self.base_selenium.LOGGER.info('open the record in edit to compare the data')
        self.contact_page.open_edit_page(row=first_contact_record, xpath='//span[@class="mr-auto ng-star-inserted"]/a')

        contact_data_after_create = self.contact_page.get_full_contact_data()
        if self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_create, data_before_save=contact_data):
            self.base_selenium.LOGGER.info('contact data have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact data was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)

        self.contact_page.get_contact_persons_page()

        contact_persons_data_after_create = self.contact_page.get_contact_persons_data()
        
        self.base_selenium.LOGGER.info('compare contact persons data after refresh')
        if self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_data_after_create, data_before_save=contact_data["contact_persons"]):
                self.base_selenium.LOGGER.info('contact persons have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact persons was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)

    def test_07_create_contact_person_from_edit_update_old_value(self):
        """
        Contact: Edit Approach: make sure that you can add contact person from the edit mode 
        LIMS-6388
        """

        self.base_selenium.LOGGER.info('open random contact record to add a new contact persons to it')
        first_contact_record = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=first_contact_record)

        self.base_selenium.LOGGER.info('acquire contact data to compare it after updating the persons')
        contact_data = self.contact_page.get_full_contact_data()

        self.base_selenium.LOGGER.info('Open contact persons page')
        self.contact_page.get_contact_persons_page()
        self.base_selenium.LOGGER.info('add new record to contact persons')
        contact_persons_after_update = self.contact_page.create_update_contact_person(save=True)

        self.base_selenium.LOGGER.info('Refresh to compare the data before and after refresh')
        self.base_selenium.refresh()

        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        if self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh, data_before_save=contact_data):
            self.base_selenium.LOGGER.info('contact data have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact data was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)

        self.contact_page.get_contact_persons_page()
        contact_persons_after_refresh = self.contact_page.get_contact_persons_data()

        self.base_selenium.LOGGER.info('compare contact persons data after refresh')
        if self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_after_refresh, data_before_save=contact_persons_after_update):
                self.base_selenium.LOGGER.info('contact persons have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact persons was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)
        

    @skip('https://modeso.atlassian.net/browse/LIMS-6394')
    def test_08_delete_contact_person(self):
        """
        Contact: Edit Approach: Make sure that you can delete any contact person from the edit mode 
        LIMS-6387
        """

        self.base_selenium.LOGGER.info('in this case, we will delete contact person that exist in the first record in the table')
        self.base_selenium.LOGGER.info('because in the sequence of test cases, first record will contain for sure a contact person')

        self.base_selenium.LOGGER.info('select the first contact record')
        first_contact_record = self.contact_page.result_table()[0]

        self.base_selenium.LOGGER.info('open the record in edit form')
        self.contact_page.open_edit_page(row=first_contact_record)

        self.base_selenium.LOGGER.info('acquire the data from the form to compare it with the data after saving to make sure it is saved correctly')
        contact_data = self.contact_page.get_full_contact_data()

        self.contact_page.get_contact_persons_page()
        count_of_contact_person_before_delete = self.contact_page.get_contact_persons_count()
        self.contact_page.delete_contact_person()
        count_of_contact_person_after_delete = self.contact_page.get_contact_persons_count()

        if count_of_contact_person_after_delete == count_of_contact_person_before_delete:
            is_successfully_deleted = self.contact_page.check_contact_persons_table_is_empty()
            if is_successfully_deleted:
                self.base_selenium.LOGGER.info('Contact person removed successfully')
            else:
                self.base_selenium.LOGGER.info('Contact person was not removed successfully, a bug should be created')
                self.assertEqual(True, is_successfully_deleted)
        else:
            self.base_selenium.LOGGER.info('Contact person removed successfully')
        
        self.base_selenium.LOGGER.info('getting contact person data after remove the record to check that it was not corrupted after being saved')
        contact_persons_after_remove = self.contact_page.get_contact_persons_data()

        self.contact_page.save(save_btn='contact:save')
        
        self.base_selenium.LOGGER.info('Refreshing to make sure that data are saved without being corrupted')
        self.base_selenium.refresh()

        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        if self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh, data_before_save=contact_data):
            self.base_selenium.LOGGER.info('contact data have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact data was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)

        self.contact_page.get_contact_persons_page()
        self.base_selenium.LOGGER.info('get contact person data after refresh to make sure it was saved correctly')
        
        contact_persons_after_refresh = self.contact_page.get_contact_persons_data()
        if count_of_contact_person_before_delete == 1:
            if self.contact_page.check_contact_persons_table_is_empty():
                self.base_selenium.LOGGER.info('contact person deleted successfully')
            else:
                self.base_selenium.LOGGER.info('contact person was not deleted successfully, report a bug')
                self.assertEqual(True, False)

        if len(contact_persons_after_refresh) == len(contact_persons_after_remove):
            if self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_after_refresh, data_before_save=contact_persons_after_remove):
                self.base_selenium.LOGGER.info('contact persons have been saved successfully')
            else:
                self.base_selenium.LOGGER.info('contact persons was not saved successfully, you should report a BUG')
                self.assertEqual(True, False)
        else:
            self.base_selenium.LOGGER.info('Data were not correctly saved, report a bug')
            self.assertEqual(True, False)