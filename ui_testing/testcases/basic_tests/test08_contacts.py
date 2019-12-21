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
        

    # @skip('https://modeso.atlassian.net/browse/LIMS-6394')
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