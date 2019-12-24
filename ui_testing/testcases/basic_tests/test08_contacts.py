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

    def test_001_archive_contact(self, action):
        """
        New: Contact: Restore/Archive Approach: I can archive/restore any contact successfully
        I can archive/restore any contact successfully
        LIMS-3566
        """
        

        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        self.contact_page.archive_selected_contacts()
        self.contact_page.get_archived_contacts()

        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            self.base_selenium.LOGGER.info(' + {} Contact should be archived.'.format(contact_no))
            self.assertTrue(self.contact_page.is_contact_in_table(value=contact_no))

    def test_002_restore_contact(self):
        """
        New: Contact: Restore/Archive Approach: I can archive/restore any contact successfully
        I can archive/restore any contact successfully
        LIMS-3566
        """
            
        self.contact_page.get_archived_contacts()
        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        self.contact_page.restore_selected_contacts()
        self.contact_page.get_active_contacts()

        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            self.base_selenium.LOGGER.info(' + {} Contact should be active.'.format(contact_no))
            self.assertTrue(self.contact_page.is_contact_in_table(value=contact_no))

    def test_003_create_contact(self):
        """
        New: Contact: Creation Approach: I can create new contact successfully
        User can create new conatcts successfully 

        LIMS-3563
        """
        
        self.base_selenium.LOGGER.info('Creating new contact')
        contact_data = self.contact_page.create_update_contact(contact_persons=False)

        self.base_selenium.LOGGER.info('comparing contact\'s data with the first record in contact page')
        self.base_selenium.LOGGER.info('to make sure that when new record is created is set to the be the first record in the page')

        created_contact_record = self.contact_page.search(value=contact_data['Contact No'])[0]
        first_contact_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_contact_record)

        table_headers = self.base_selenium.get_table_head_elements(element="contacts:contact_table")
        headers_text = [header.text for header in table_headers]

        for header in headers_text:
            self.base_selenium.LOGGER.info('contact {} is {}, and it should be {}'.format(header, first_contact_data[header], contact_data[header]) )
            self.assertEqual(first_contact_data[header], contact_data[header])

        
    def test_004_upadte_contact(self):
        """
        New: Contact: Edit Approach: I can update any contact record 
        I can edit in step one or two & this update should saved successfully 

        LIMS-3564
        """
        
        self.base_selenium.LOGGER.info('Select random table row')
        row = self.contact_page.get_random_contact()
        self.contact_page.open_edit_page(row=row)

        self.base_selenium.LOGGER.info('updating contact with newrandom data')
        contact_data_before_refresh = self.contact_page.create_update_contact(create=False, contact_persons=False)

        self.base_selenium.LOGGER.info('Refresh the page to make sure that data updated successfully')
        self.base_selenium.refresh()
        
        contact_data_after_refresh = self.contact_page.get_full_contact_data()

        self.base_selenium.LOGGER.info('Compare Contact before refresh and after refresh')
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh, data_before_save=contact_data_before_refresh))

    
    def test_005_search_by_any_field(self):
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

    def test_006_download_contact_sheet(self):
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

    def test_007_create_contact_with_person(self):
        contact_data = self.contact_page.create_update_contact()

        self.base_selenium.LOGGER.info('filter by contact no.: {} to get the record'.format(contact_data['Contact No']))
        first_contact_record = self.contact_page.search(value=contact_data['Contact No'])[0]

        self.base_selenium.LOGGER.info('open the record in edit to compare the data')
        self.contact_page.open_edit_page(row=first_contact_record)

        contact_data_after_create = self.contact_page.get_full_contact_data()
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_create, data_before_save=contact_data))

        self.contact_page.get_contact_persons_page()

        contact_persons_data_after_create = self.contact_page.get_contact_persons_data()
        
        self.base_selenium.LOGGER.info('compare contact persons data after refresh')
        if self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_data_after_create, data_before_save=contact_data["contact_persons"]):
                self.base_selenium.LOGGER.info('contact persons have been saved successfully')
        else:
            self.base_selenium.LOGGER.info('contact persons was not saved successfully, you should report a BUG')
            self.assertEqual(True, False)

    def test_008_create_contact_person_from_edit_update_old_value(self):
        """
        Contact: Edit Approach: make sure that you can add contact person from the edit mode 
        LIMS-6388
        """

        self.base_selenium.LOGGER.info('open random contact record to add a new contact persons to it')
        random_contact_record = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=random_contact_record)

        self.base_selenium.LOGGER.info('acquire contact data to compare it after updating the persons')
        contact_data = self.contact_page.get_full_contact_data()

        self.base_selenium.LOGGER.info('Open contact persons page')
        self.contact_page.get_contact_persons_page()
        self.base_selenium.LOGGER.info('add new record to contact persons')
        contact_persons_after_update = self.contact_page.create_update_contact_person(save=True)

        self.base_selenium.LOGGER.info('Refresh to compare the data before and after refresh')
        self.base_selenium.refresh()

        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh, data_before_save=contact_data))

        self.contact_page.get_contact_persons_page()
        contact_persons_after_refresh = self.contact_page.get_contact_persons_data()

        self.base_selenium.LOGGER.info('compare contact persons data after refresh')
        self.assertTrue(self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_after_refresh, data_before_save=contact_persons_after_update))
        

    @skip('https://modeso.atlassian.net/browse/LIMS-6394')
    def test_009_delete_contact_person(self):
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
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh, data_before_save=contact_data))

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


    def test_010_delete_contact_used_in_other_data(self):
        """
        New: Contact: Delete Approach: I can't delete any contact if this contact related to some data 
        I can't delete any contact if this contact related to some data 
        """

        order_request = self.orders_api.get_all_orders().json()
        self.assertEqual(order_request['status'], 1)
        orders_records = order_request['orders']
        self.assertNotEqual(len(orders_records), 0)
        random_order_index = self.generate_random_number(lower=0, upper=len(orders_records)-1)
        selected_order_record = orders_records[random_order_index]
        contact_name = selected_order_record['company'][0]
        self.base_selenium.LOGGER.info('filter by contact name: {}'.format(contact_name))
        contact_record = self.contact_page.search(value=contact_name)[0]
        if self.contact_page.check_if_table_is_empty():
            self.base_selenium.LOGGER.info('Contact "{}" doesn\'t exist in active table'.format(contact_name))
        else:
            self.contact_page.click_check_box(source=contact_record)
            self.contact_page.archive_selected_items()
        
        self.base_selenium.LOGGER.info('get the archived contacts')
        self.contact_page.get_archived_contacts()

        contact_archived_records = self.contact_page.search(value=contact_name)[0]

        self.assertFalse(self.contact_page.check_if_table_is_empty)
        
        self.base_selenium.LOGGER.info('delete selected record')
        self.contact_page.click_check_box(source=contact_archived_records)
        self.contact_page.delete_selected_contacts()
        if self.contact_page.check_delete_message():
            self.base_selenium.LOGGER.info('refresh to check that data wasn\'t affected')
            self.base_selenium.refresh()
            self.contact_page.get_archived_contacts()
            archived_record = self.contact_page.search(value=contact_name)

            self.assertFalse(self.contact_page.check_if_table_is_empty)
            
            self.base_selenium.LOGGER.info('Contact record could not be deleted')
            self.base_selenium.LOGGER.info('making sure that the archived contact is the same that is used in data')
            contact_data = self.base_selenium.get_row_cells_dict_related_to_header(row=archived_record[0])
            self.base_selenium.LOGGER.info('Contact name is {}, and it should be {}'.format(contact_data['Contact Name'], contact_name))
            self.assertEqual(contact_data['Contact Name'], contact_name)

    def test_011_user_can_show_hide_any_column(self):
        """
        New:  contacts: Optional fields: User can hide/show any optional field in Edit/Create form 
        In the configuration section, In case I archive any optional field this field should be hidden from Edit/Create from and it should also found in the archive in table configuration.
        LIMS-4129
        """
        
        self.base_selenium.LOGGER.info('hide multiple columns')
        hidden_columns = self.contact_page.hide_columns(always_hidden_columns=['fax'])
        self.contact_page.sleep_small()
        
        self.base_selenium.LOGGER.info('Compare the headers of teh tables to make sure that those columns are hidden')
        table_headers = self.base_selenium.get_table_head_elements(element="contacts:contact_table")
        headers_text = [header.text for header in table_headers]
        
        
        for column in hidden_columns:
            self.assertIn(column, headers_text)

        self.base_selenium.LOGGER.info('All columns are hidden successfully')
        self.base_selenium.LOGGER.info('export the data to make sure that hidden columns are hidden also form export')
        self.contact_page.download_xslx_sheet()
        rows_data = self.contact_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.base_selenium.LOGGER.info(' * Comparing the contact no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.contact_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)
        
        self.base_selenium.LOGGER.info('set all columns to shown again')
        self.contact_page.set_all_configure_table_columns_to_specific_value(value=True, always_hidden_columns=['fax'])
    
    def test_012_update_departments_should_reflect_orders(self):
        """
        New: Contacts: Department Approach: Any edit in the department, will reflect in the table view of orders and analysis sections.
        Any edit in the department, will reflect in the table view of orders and analysis sections.
        LIMS-3571
        """

        self.base_selenium.LOGGER.info('Creating new contact with new department to keep track of the updated departments')
        contact_data = self.contact_page.create_update_contact()

        contact_name = contact_data['name']
        departments = contact_data['departments']

        self.base_selenium.LOGGER.info('create order with the desired contact to keep track of the updated')
        self.order_page.get_orders_page()
        order_data = self.order_page.create_new_order(material_type='Raw Material', departments=departments, contact=contact_name, test_plans=[])

        self.base_selenium.LOGGER.info('get the contacts to update the desired contact department')
        self.contact_page.get_contacts_page()

        contact_record = self.contact_page.search(value=contact_data['no'])[0]
        self.contact_page.open_edit_page(row=contact_record)

        self.base_selenium.LOGGER.info('generating list of new updated departments')
        new_departments_list = []
        counter = 0
        while counter < 1:
            new_departments_list.append(self.contact_page.generate_random_text())
            counter = counter +1

        new_updated_departments = self.contact_page.update_department_list(departments=new_departments_list)
        self.base_selenium.LOGGER.info('refresh to make sure that departments updated correctly')

        self.base_selenium.refresh()
        new_departments_after_refresh = self.contact_page.get_contact_departments()
        self.base_selenium.LOGGER.info('compare departments, departments are {}, and should be {}'.format(new_departments_after_refresh, new_updated_departments))

        self.assertEqual(new_updated_departments, new_departments_after_refresh)

        departments_list = new_updated_departments.split(', ')

        self.base_selenium.LOGGER.info('get orders page and open order no {}, to make sure that departments updated correctly'.format(order_data['orderNo']))
        self.order_page.get_orders_page()

        order_record = self.order_page.search(value=order_data['orderNo'])[0]
        self.order_page.open_edit_page(row=order_record)

        order_data_after_department_updates = self.order_page.get_suborder_data()

        order_departments = order_data_after_department_updates['suborders'][0]['departments']

        self.base_selenium.LOGGER.info('check departments after update')
        for department in order_departments:
            self.assertIn(department, departments_list)