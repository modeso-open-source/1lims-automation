from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.article_page import Article
from ui_testing.pages.contact_page import Contact
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.base_pages import BasePages
from ui_testing.pages.order_page import Order
from ui_testing.pages.contacts_page import Contacts
from ui_testing.pages.header_page import Header
from api_testing.apis.orders_api import OrdersAPI
from api_testing.apis.contacts_api import ContactsAPI
from parameterized import parameterized
import re
import random
from unittest import skip


class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.contact_page = Contact()
        self.contacts_page = Contacts()
        self.contacts_api = ContactsAPI()
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.test_unit_page = TstUnit()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.header_page = Header()
        self.base_page = BasePages()

        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.contact_page.get_contacts_page()
        table_fields = self.contacts_api.get_table_fields(component_id=3)[0]['fields']

        if self.contact_page.check_for_hidden_table_fields(fields=table_fields):
            self.contact_page.set_all_configure_table_columns_to_specific_value(value=True,
                                                                                always_hidden_columns=['fax'])
        self.contact_page.sleep_tiny()

    def test_001_archive_contact(self):
        """
        New: Contact: Restore/Archive Approach: I can archive any contact successfully

        LIMS-3566
        """
        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        self.contact_page.archive_selected_contacts()
        self.contact_page.get_archived_contacts()
        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            self.info(' + {} Contact sucessfully archived.'.format(contact_no))
            self.assertTrue(self.contact_page.is_contact_in_table(value=contact_no))

    def test_002_restore_contact(self):
        """
        New: Contact: Restore/Archive Approach: I can restore any contact successfully

        LIMS-3566
        """
        self.contact_page.get_archived_contacts()
        self.contacts_page.sleep_tiny()
        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        self.contact_page.restore_selected_contacts()
        self.contact_page.get_active_contacts()
        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            self.info(' + {} Contact sucessfully restored.'.format(contact_no))
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
        created_contact_record = self.contact_page.search(value=contact_data['Contact No'])[0]
        first_contact_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_contact_record)

        table_headers = self.base_selenium.get_table_head_elements(element="contacts:contact_table")
        headers_text = [header.text for header in table_headers]

        self.base_selenium.LOGGER.info(headers_text)
        for header, value in contact_data.items():
            if header != 'contact_persons':
                self.base_selenium.LOGGER.info(
                    'contact {} is {}, and it should be {}'.format(header, first_contact_data[header],
                                                                   contact_data[header]))
                self.assertEqual(first_contact_data[header], contact_data[header])

    def test_004_upadte_contact(self):
        """
        New: Contact: Edit Approach: I can update any contact record 
        I can edit in step one or two & this update should saved successfully 

        LIMS-3564
        """

        self.base_selenium.LOGGER.info('Select random table row')
        row = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=row)

        self.base_selenium.LOGGER.info('updating contact with newrandom data')
        contact_data_before_refresh = self.contact_page.create_update_contact(create=False, contact_persons=False)

        self.base_selenium.LOGGER.info('Refresh the page to make sure that data updated successfully')
        self.base_selenium.refresh()

        contact_data_after_refresh = self.contact_page.get_full_contact_data()

        self.base_selenium.LOGGER.info('Compare Contact before refresh and after refresh')
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh,
                                                                    data_before_save=contact_data_before_refresh))

    def test_005_search_by_any_field(self):
        """
        New: Contacts: Search Approach: I can search by any field in the table view 
        I can search by any field in the table view 

        LIMS-3573
        """

        row = self.contact_page.get_random_contact_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '' or row_data[
                column] == '-':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.article_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    @skip('https://modeso.atlassian.net/browse/LIMS-6402')
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
        """
        New: Contact: Creation Approach: I can create new contact
        successfully with contact person

        LIMS-6386
        """
        contact_data = self.contact_page.create_update_contact()

        self.info('filter by contact no.: {} to get the record'.format(contact_data['Contact No']))
        self.order_page.apply_filter_scenario(
            filter_element='contact:contact_no_filter', filter_text=contact_data['Contact No'], field_type='text')
        self.contact_page.sleep_small()
        contact_record = self.contact_page.result_table()[0]

        self.info('open the record in edit to compare the data')
        self.contact_page.open_edit_page_by_css_selector(row=contact_record)
        contact_data_after_create = self.contact_page.get_full_contact_data()
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_create,
                                                                    data_before_save=contact_data))

        self.contact_page.get_contact_persons_page()
        contact_persons_data_after_create = self.contact_page.get_contact_persons_data()
        self.info('compare contact persons data after refresh')
        self.assertTrue(self.contact_page.compare_contact_persons_data(
            data_after_save=contact_persons_data_after_create, data_before_save=contact_data["contact_persons"]))
        self.info('contact persons have been saved successfully')

    def test_008_create_contact_person_from_edit_update_old_value(self):
        """
        Contact: Edit Approach: make sure that you can add contact person from the edit mode 

        LIMS-6388
        """
        self.info('open random contact record to add a new contact persons to it')
        random_contact_record = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=random_contact_record)

        self.info('acquire contact data to compare it after updating the persons')
        contact_data = self.contact_page.get_full_contact_data()

        self.info('Open contact persons page')
        self.contact_page.get_contact_persons_page()
        self.info('add new record to contact persons')
        contact_persons_after_update = self.contact_page.create_update_contact_person(save=True)

        self.info('Refresh to compare the data before and after refresh')
        self.base_selenium.refresh()
        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh,
                                                                    data_before_save=contact_data))

        self.contact_page.get_contact_persons_page()
        contact_persons_after_refresh = self.contact_page.get_contact_persons_data()

        self.info('compare contact persons data after refresh')
        self.assertTrue(self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_after_refresh,
                                                                       data_before_save=contact_persons_after_update))

    @skip('https://modeso.atlassian.net/browse/LIMS-6394')
    def test_009_delete_contact_person(self):
        """
        Contact: Edit Approach: Make sure that you can delete any contact person from the edit mode 
        LIMS-6387
        """

        self.base_selenium.LOGGER.info('select random contact record')
        random_contact_record = self.contact_page.get_random_contact_row()

        self.base_selenium.LOGGER.info('open the record in edit form')
        self.contact_page.open_edit_page(row=random_contact_record)

        self.base_selenium.LOGGER.info(
            'acquire the data from the form to compare it with the data after saving to make sure it is saved correctly')
        contact_data = self.contact_page.get_full_contact_data()

        self.contact_page.get_contact_persons_page()
        self.base_selenium.LOGGER.info('check if there is no contact person, create new one and then refresh the page')

        if self.contact_page.check_contact_persons_table_is_empty():
            self.contact_page.create_update_contact_person()
            self.contact_page.save(save_btn='contact:save')
            self.base_selenium.refresh()
            self.contact_page.get_contact_persons_page()

        self.base_selenium.LOGGER.info('get the data of the contact_persons before delete')
        contact_persons_data_before_delete = self.contact_page.get_contact_persons_data()
        random_index_to_delete = self.generate_random_number(lower=0, upper=len(contact_persons_data_before_delete) - 1)
        self.contact_page.delete_contact_person(index=random_index_to_delete)
        deleted_person_name = contact_persons_data_before_delete[random_index_to_delete]['name']
        contact_persons_data_after_delete = self.contact_page.get_contact_persons_data()

        self.assertNotEqual(len(contact_persons_data_before_delete), len(contact_persons_data_after_delete))

        for person in contact_persons_data_after_delete:
            self.assertNotEqual(deleted_person_name, person['name'])

        self.contact_page.save(save_btn='contact:save')
        self.base_selenium.LOGGER.info('refresh to make sure that data are saved correctly')
        self.base_selenium.refresh()

        self.base_selenium.LOGGER.info('compare contact data before refresh and after refresh')
        contact_data_after_refresh = self.contact_page.get_full_contact_data()

        self.assertTrue(self.contact_page.compare_contact_main_data(data_before_save=contact_data,
                                                                    data_after_save=contact_data_after_refresh))

        self.contact_page.get_contact_persons_page()
        self.base_selenium.LOGGER.info('compare contact person data before refresh and after refresh')
        contact_person_data_after_save = self.contact_page.get_contact_persons_data()
        self.assertTrue(
            self.contact_page.compare_contact_persons_data(data_before_save=contact_persons_data_after_delete,
                                                           data_after_save=contact_person_data_after_save))

    def test_010_delete_contact_used_in_other_data(self):
        """
        New: Contact: Delete Approach: I can't delete any contact if this contact related to some data 
        I can't delete any contact if this contact related to some data

        LIMS-3565
        """
        order_request = self.orders_api.get_all_orders()
        self.assertEqual(order_request['status'], 1)
        orders_records = order_request['orders']
        self.assertNotEqual(len(orders_records), 0)
        random_order_index = self.generate_random_number(lower=0, upper=len(orders_records) - 1)
        selected_order_record = orders_records[random_order_index]
        contact_name = selected_order_record['company'][0]
        self.info('filter by contact name: {}'.format(contact_name))
        contact_record = self.contact_page.search(value=contact_name)[0]
        if self.contact_page.check_if_table_is_empty():
            self.info('Contact "{}" doesn\'t exist in active table'.format(contact_name))
        else:
            self.contact_page.click_check_box(source=contact_record)
            self.contact_page.archive_selected_items()

        self.info('get the archived contacts')
        self.contact_page.get_archived_contacts()
        contact_archived_records = self.contact_page.search(value=contact_name)[0]

        self.assertFalse(self.contact_page.check_if_table_is_empty())
        self.info('delete selected record')
        self.contact_page.click_check_box(source=contact_archived_records)
        self.contact_page.delete_selected_contacts()
        self.contact_page.sleep_tiny()
        self.info('refresh to check that data wasn\'t affected')
        self.base_selenium.refresh()
        self.contact_page.get_archived_contacts()
        archived_record = self.contact_page.search(value=contact_name)

        self.assertFalse(self.contact_page.check_if_table_is_empty())
        self.info('Contact record could not be deleted')
        self.info('making sure that the archived contact is the same that is used in data')

        found = False
        for row in archived_record:
            contact_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)

            if len(contact_data) > 1 and contact_data['Contact Name'] == contact_name:
                found = True
        self.assertTrue(found)

    @skip('https://modeso.atlassian.net/browse/LIMS-6402')
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
            self.assertNotIn(column, headers_text)

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

    def test012_update_departments_should_reflect_orders(self):
        """
        New: Contacts: Department Approach: Any edit in the department, will reflect in the table view of orders and analysis sections.
        Any edit in the department, will reflect in the table view of orders and analysis sections.
        LIMS-3571
        """

        self.base_selenium.LOGGER.info(
            'Creating new contact with new department to keep track of the updated departments')
        contact_data = self.contact_page.create_update_contact()

        contact_name = contact_data['Contact Name']
        departments = contact_data['Departments']

        self.base_selenium.LOGGER.info('create order with the desired contact to keep track of the updated')
        self.order_page.get_orders_page()
        self.order_page.create_new_order(material_type='Raw Material', departments=departments,
                                         contact=contact_name, test_plans=[])
        order_id = self.order_page.get_order_id()
        self.base_selenium.LOGGER.info('get the contacts to update the desired contact department')
        self.contact_page.get_contacts_page()

        contact_record = self.contact_page.search(value=contact_data['Contact No'])[0]
        self.contact_page.open_edit_page(row=contact_record)

        self.base_selenium.LOGGER.info('generating list of new updated departments')
        new_departments_list = []
        counter = 0
        while counter < 1:
            new_departments_list.append(self.contact_page.generate_random_text())
            counter = counter + 1

        new_updated_departments = self.contact_page.update_department_list(departments=new_departments_list)
        self.base_selenium.LOGGER.info('refresh to make sure that departments updated correctly')

        self.base_selenium.refresh()
        new_departments_after_refresh = self.contact_page.get_contact_departments()
        self.base_selenium.LOGGER.info(
            'compare departments, departments are {}, and should be {}'.format(new_departments_after_refresh,
                                                                               new_updated_departments))

        self.assertEqual(new_updated_departments, new_departments_after_refresh)

        departments_list = new_updated_departments.split(', ')

        self.base_selenium.LOGGER.info('get order data of order with id {}'.format(order_id))
        order_request = self.orders_api.get_order_by_id(id=order_id)
        self.assertEqual(order_request['status'], 1)
        order_data = order_request['orders']
        self.assertNotEqual(len(order_data), 0)

        orders_departments = []
        for suborder in order_data:
            temp_departments = list(map(lambda s: s['name'], suborder['departments']))
            orders_departments = orders_departments + temp_departments

        self.base_selenium.LOGGER.info(
            'making sure that the updated departments does exist in the order departments list')
        for dep in departments_list:
            self.assertIn(dep, orders_departments)

    @parameterized.expand(['ok', 'cancel'])
    def test013_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table
        LIMS-6203
        """
        self.base_selenium.LOGGER.info('create new contact.')
        self.base_selenium.click(element='contacts:new_contact')
        self.contact_page.sleep_small()
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

    def test014_edit_approach_overview_button(self):
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
        self.contacts_page.info('contact_url : {}'.format(contact_url))
        # click on Overview, it will redirect you to contacts' page
        self.contacts_page.info('click on Overview and confirm pop-up')
        self.base_page.click_overview()
        self.contacts_page.confirm_overview_pop_up()
        self.contacts_page.sleep_tiny()
        self.assertEqual(self.base_selenium.get_url(), '{}contacts'.format(self.base_selenium.url))
        self.contacts_page.info('clicking on Overview confirmed')

    def test015_contacts_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page
        LIMS-6201

        """

        contacts_response, _ = self.contacts_api.get_all_contacts()
        contacts = contacts_response['contacts']
        contact_name = random.choice(contacts)['name']
        search_results = self.contact_page.search(contact_name)
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
            if search_data['Contact Name'] == contact_name:
                break
        else:
            self.assertTrue(False, " * There is no search results for it, Report a bug.")
        self.assertEqual(contact_name, search_data['Contact Name'])
        # Navigate to test plan page
        self.base_selenium.LOGGER.info('navigate to test plans page')
        self.test_plan.get_test_plans_page()
        self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))

    def test016_create_user_with_role_contact(self):
        """
        New: Contact: User management: All the contacts created should be found when I create new user with role contact 
        All the contacts created should be found when I create new user with role contact 
        
        LIMS-3569
        """

        contact_request, _ = self.contacts_api.get_all_contacts()
        self.assertEqual(contact_request['status'], 1)
        self.assertNotEqual(contact_request['count'], 0)
        contacts_records = contact_request['contacts']

        contact_name = contacts_records[0]['name']

        self.header_page.get_users_page()

        user_name = self.header_page.generate_random_text()
        self.base_selenium.LOGGER.info('random username generate is {}'.format(user_name))

        user_pw = self.header_page.generate_random_text()
        self.base_selenium.LOGGER.info('random user password generate is {}'.format(user_pw))

        user_mail = self.header_page.generate_random_email()
        self.base_selenium.LOGGER.info('random user email generate is {}'.format(user_mail))

        self.base_selenium.LOGGER.info('contact that user will be created with is {}'.format(contact_name))

        self.base_selenium.LOGGER.info('create new user with the randomly generated data')
        self.header_page.create_new_user(user_role='Contact', user_password=user_pw, user_confirm_password=user_pw,
                                         user_email=user_mail, user_name=user_name, user_contact=contact_name)

        self.base_selenium.LOGGER.info(
            'search with the user name to make sure that it was created with the correct data')
        user_record = self.header_page.search(user_name)[0]
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=user_record)

        self.base_selenium.LOGGER.info('compare the user data with the randomly generated data')
        self.assertEqual(user_name, row_data['Name'])
        self.assertEqual(contact_name, row_data['Contact'])

    def test017_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        assert (self.test_unit_page.deselect_all_configurations(), False)

    def test018_filter_by_contact_name(self):
        """
        Contacts: Filter Approach: Make sure you can filter by Name
        LIMS-6408
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='name')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:name', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Contact Name'], data_to_filter_with)
            counter = counter + 1

    def test019_filter_by_contact_departments(self):
        """
        Contacts: Filter Approach: Make sure you can filter by departments
        LIMS-6413
        """

        data_to_filter_with = \
            self.contacts_api.get_first_record_with_data_in_attribute(attribute='departments').split(',')[0]
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:departments', filter_text=data_to_filter_with)
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            contact_departments = row_data['Departments'].split(', ')
            self.assertIn(data_to_filter_with, contact_departments)
            counter = counter + 1

    def test020_filter_by_contact_skype(self):
        """
        Contacts: Filter Approach: Make sure you can filter by skype
        LIMS-6418
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='skype')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:skype', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Skype'], data_to_filter_with)
            counter = counter + 1

    def test021_filter_by_contact_number(self):
        """
        Contacts: Filter Approach: Make sure you can filter by number
        LIMS-6409
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='companyNo')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:no', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Contact No'].replace("'", ""), data_to_filter_with.replace("'", ""))
            counter = counter + 1

    def test022_filter_by_contact_email(self):
        """
        Contacts: Filter Approach: Make sure you can filter by email
        LIMS-6414
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='email')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:email', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Email'], data_to_filter_with)
            counter = counter + 1

    def test023_filter_by_contact_postalcode(self):
        """
        Contacts: Filter Approach: Make sure you can filter by postal code
        LIMS-6419
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='postalCode')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:postalcode_filter',
                                                filter_text=data_to_filter_with, field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Postal Code'], data_to_filter_with)
            counter = counter + 1

    def test024_filter_by_contact_changed_by(self):
        """
        Contacts: Filter Approach: Make sure you can filter by changed by
        LIMS-6410
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='lastModifiedUser')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:last_modified_user_field',
                                                filter_text=data_to_filter_with)
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Changed By'], data_to_filter_with)
            counter = counter + 1

    def test025_filter_by_contact_website(self):
        """
        Contacts: Filter Approach: Make sure you can filter by website
        LIMS-6415
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='website')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:website', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Website'], data_to_filter_with)
            counter = counter + 1

    def test026_filter_by_contact_created_on(self):
        """
        Contacts: Filter Approach: Make sure you can filter by created on 
        LIMS-6420
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='createdAt')
        data_to_filter_with = self.contact_page.convert_to_dot_date_format(date=data_to_filter_with)
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:created_on_field',
                                                filter_text=data_to_filter_with, field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Created On'], data_to_filter_with)
            counter = counter + 1

    def test027_filter_by_contact_address(self):
        """
        Contacts: Filter Approach: Make sure you can filter by address
        LIMS-6411
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='country')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:country_filter',
                                                filter_text=data_to_filter_with)
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Country'], data_to_filter_with)
            counter = counter + 1

    def test028_filter_by_contact_type(self):
        """
        Contacts: Filter Approach: Make sure you can filter by type
        LIMS-6421
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='type')
        self.assertNotEqual(data_to_filter_with, False)
        data_to_filter_with = self.contact_page.get_mapped_contact_type(contact_type=data_to_filter_with[0])

        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:type_filter', filter_text=data_to_filter_with)
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            contact_type = row_data['Type'].split(', ')
            self.assertIn(data_to_filter_with, contact_type)
            counter = counter + 1

    def test029_filter_by_contact_phone(self):
        """
        Contacts: Filter Approach: Make sure you can filter by phone
        LIMS-6412
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='phone')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:phone', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Phone'], data_to_filter_with)
            counter = counter + 1

    def test030_filter_by_contact_location(self):
        """
        Contacts: Filter Approach: Make sure you can filter by location
        LIMS-6417
        """

        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='location')
        self.assertNotEqual(data_to_filter_with, False)
        self.base_selenium.LOGGER.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:location', filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data['Location'], data_to_filter_with)
            counter = counter + 1
