from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.contact_page import Contact
from ui_testing.pages.login_page import Login
from ui_testing.pages.base_pages import BasePages
from ui_testing.pages.order_page import Order
from ui_testing.pages.contacts_page import Contacts
from ui_testing.pages.my_profile_page import MyProfile
from ui_testing.pages.header_page import Header
from api_testing.apis.orders_api import OrdersAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.users_api import UsersAPI
from parameterized import parameterized
from nose.plugins.attrib import attr
from unittest import skip
import re, random


class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.contact_page = Contact()
        self.contacts_page = Contacts()
        self.contacts_api = ContactsAPI()
        self.base_page = BasePages()

        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.contacts_api.set_configuration()
        self.contact_page.get_contacts_page()
        table_fields = self.contacts_api.get_table_fields(component_id=3)[0]['fields']
        if self.contact_page.check_for_hidden_table_fields(fields=table_fields):
            self.contact_page.set_all_configure_table_columns_to_specific_value(value=True,
                                                                                always_hidden_columns=['fax'])
        self.contact_page.sleep_tiny()

    def test001_archive_contact(self):
        """
        New: Contact: Restore/Archive Approach: I can archive any contact successfully

        LIMS-3566
        """
        self.info("select random contacts row to archive")
        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        self.contact_page.archive_selected_contacts()
        self.contact_page.get_archived_contacts()
        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            self.info('{} Contact sucessfully archived.'.format(contact_no))
            self.assertTrue(self.contact_page.is_contact_in_table(value=contact_no))

    def test002_restore_contact(self):
        """
        New: Contact: Restore/Archive Approach: I can restore any contact successfully

        LIMS-3566
        """
        self.info("Navigate to archived contacts' table")
        self.contact_page.get_archived_contacts()
        self.info("select random contacts rows to restore")
        selected_contacts_data, _ = self.contact_page.select_random_multiple_table_rows()
        self.contact_page.restore_selected_contacts()
        self.contact_page.get_active_contacts()
        for contact in selected_contacts_data:
            contact_no = contact['Contact No']
            self.info('{} Contact sucessfully restored.'.format(contact_no))
            self.assertTrue(self.contact_page.is_contact_in_table(value=contact_no))

    def test003_create_contact(self):
        """
        New: Contact: Creation Approach: I can create new contact successfully

        LIMS-3563
        """
        self.info('Creating new contact')
        contact_data = self.contact_page.create_update_contact(contact_persons=False)

        self.info('comparing contact\'s data with the first record in contact page')
        self.contact_page.search(value=contact_data['Contact No'])
        found_contact_data = self.contacts_page.get_the_latest_row_data()
        self.info("assert that contact created successfully with data {}".format(contact_data))
        for key in contact_data.keys():
            if key in found_contact_data.keys():
                self.assertEqual(found_contact_data[key].replace("'", ""), contact_data[key])

    def test004_upadte_contact(self):
        """
        New: Contact: Edit Approach: I can update any contact record 
        I can edit in step one or two & this update should saved successfully 

        LIMS-3564
        """
        self.info('Select random table row')
        row = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=row)
        self.info('updating contact with new random data')
        contact_data_before_refresh = self.contact_page.create_update_contact(create=False, contact_persons=False)
        self.info('Refresh the page to make sure that data updated successfully')
        self.base_selenium.refresh()
        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        self.info('Compare Contact before refresh and after refresh')
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh,
                                                                    data_before_save=contact_data_before_refresh))
    def test005_search_by_any_field(self):
        """
        New: Contacts: Search Approach: I can search by any field in the table view 
        I can search by any field in the table view 

        LIMS-3573
        """
        row = self.contact_page.get_random_contact_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] in ['', '-']:
                continue
            self.info('search for {} : {}'.format(column, row_data[column]))
            if column == 'Contact Type':
                search_results = self.contacts_page.search(row_data[column].lower())
            else:
                search_results = self.contacts_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, "There is no search results for it, Report a bug.")

            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column].replace("'", '') == row_data[column].replace("'", ''):
                    break
            self.assertIn(search_data[column].replace("'", ''), row_data[column].replace("'", ''))

    def test006_download_contact_sheet(self):
        """
        New: Contact: XSLX File: I can download all the data in the table view in the excel sheet

        LIMS-3568
        """
        self.info(' * Download XSLX sheet')
        self.contact_page.download_xslx_sheet()
        rows_data = list(filter(None, self.contact_page.get_table_rows_data()))
        for index in range(len(rows_data)-1):
            self.info(' * Comparing the contact no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.contact_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    def test007_create_contact_with_person(self):
        """
        New: Contact: Creation Approach: I can create new contact successfully with contact person

        LIMS-6386
        """
        self.info("create contact with contact person")
        contact_data = self.contact_page.create_update_contact()
        self.info('filter by contact no.: {} to get the record'.format(contact_data['Contact No']))
        self.contacts_page.apply_filter_scenario(
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

    def test008_create_contact_person_from_edit_update_old_value(self):
        """
        Contact: Edit Approach: make sure that you can add contact person from the edit mode 

        LIMS-6388
        """
        self.info('open random contact record to add a new contact persons to it')
        random_contact_record = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=random_contact_record)
        self.contact_page.sleep_small()
        self.info('acquire contact data to compare it after updating the persons')
        contact_data = self.contact_page.get_full_contact_data()

        self.info('Open contact persons page')
        self.contact_page.get_contact_persons_page()
        self.contact_page.sleep_small()
        self.info('add new record to contact persons')
        contact_persons_after_update = self.contact_page.create_update_contact_person(save=True)

        self.info('Refresh to compare the data before and after refresh')
        self.base_selenium.refresh()
        self.contact_page.sleep_small()
        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        self.assertTrue(self.contact_page.compare_contact_main_data(data_after_save=contact_data_after_refresh,
                                                                    data_before_save=contact_data))

        self.contact_page.get_contact_persons_page()
        contact_persons_after_refresh = self.contact_page.get_contact_persons_data()

        self.info('compare contact persons data after refresh')
        self.assertTrue(self.contact_page.compare_contact_persons_data(data_after_save=contact_persons_after_refresh,
                                                                       data_before_save=contact_persons_after_update))
    #@skip('https://modeso.atlassian.net/browse/LIMS-6394')
    def test009_delete_contact_person(self):
        """
        Contact: Edit Approach: Make sure that you can delete any contact person from the edit mode 

        LIMS-6387
        """
        self.info('create contact with persons using API')
        response, payload = self.contacts_api.create_contact_with_person()
        self.assertEqual(response['status'], 1, 'can not create contact with {}'.format(payload))
        self.info('open contact edit page')
        self.contacts_page.get_contact_edit_page_by_id(response['company']['companyId'])
        self.info("navigate to contact persons page")
        self.contact_page.get_contact_persons_page()
        contact_person_data_before_delete = self.contact_page.get_contact_persons_data()
        self.info('contact_persons data before delete {}'.format(contact_person_data_before_delete))
        self.assertTrue(contact_person_data_before_delete)
        self.contact_page.delete_contact_persons()
        self.info('refresh to make sure that data are saved correctly')
        self.base_selenium.refresh()
        self.info('compare contact person data before refresh and after refresh')
        contact_person_data_after_save = self.contact_page.get_contact_persons_data()
        self.assertFalse(contact_person_data_after_save)

    @skip('https://modeso.atlassian.net/browse/LIMSA-388')
    def test010_delete_contact_used_in_other_data(self):
        """
        New: Contact: Delete Approach: I can't delete any contact if this contact related to some data 

        LIMS-3565
        """
        self.info("get random order data")
        response, payload = OrdersAPI().create_new_order()
        contact_No = payload[0]['contact'][0]['No']
        self.info('filter by contact No: {}'.format(contact_No))
        self.contact_page.filter_by_contact_no(contact_No)
        contact_record = self.contacts_page.result_table()[0]
        if self.contact_page.check_if_table_is_empty():
            self.info('contact "{}" doesn\'t exist in active table'.format(contact_No))
        else:
            self.contact_page.click_check_box(source=contact_record)
            self.contact_page.archive_selected_items()
            self.contacts_page.close_filter_menu()

        self.info('get the archived contacts')
        self.contact_page.get_archived_contacts()
        self.contact_page.filter_by_contact_no(contact_No)
        contact_archived_records = self.contacts_page.result_table()[0]
        self.assertFalse(self.contact_page.check_if_table_is_empty())
        self.info('delete selected record')
        self.contact_page.click_check_box(source=contact_archived_records)
        self.assertFalse(self.contact_page.delete_selected_contacts())

    def test011_user_can_show_hide_any_column(self):
        """
        New:  contacts: Optional fields: User can hide/show any optional field in Edit/Create form
        In the configuration section, In case I archive any optional field this field should be hidden
        from Edit/Create from and it should also found in the archive in table configuration.

        LIMS-4129
        """
        self.info('hide multiple columns')
        hidden_columns = self.contact_page.hide_columns(always_hidden_columns=['fax'])
        self.contact_page.sleep_small()
        self.info('Compare the headers of teh tables to make sure that those columns are hidden')
        table_headers = self.base_selenium.get_table_head_elements(element="contacts:contact_table")
        headers_text = [header.text for header in table_headers]

        for column in hidden_columns:
            self.assertNotIn(column, headers_text)

        self.info('All columns are hidden successfully')
        self.info('export the data to make sure that hidden columns are hidden also form export')
        self.contact_page.download_xslx_sheet()
        rows_data = self.contact_page.get_table_rows_data()
        for index in range(len(rows_data)-1):
            self.info(' * Comparing the contact no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.contact_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    def test012_update_departments_should_reflect_orders(self):
        """
        New: Contacts: Department Approach: Any edit in the department,
        will reflect in the table view of orders and analysis sections.

        LIMS-3571
        """
        self.order_page = Order()
        self.info("create new contact with department to make sure that contact and order has only one department")
        contact_response, payload = self.contacts_api.create_contact()
        self.assertEqual(contact_response['status'], 1, payload)
        self.info("create new order with department")
        order_response, payload = OrdersAPI().create_order_with_department_by_contact_id(
            contact_response['company']['companyId'])
        self.assertEqual(order_response['status'], 1, payload)
        self.info('order created with contact {} and department {}'.format(payload[0]['contact'][0]['text'],
                                                                           payload[0]['departments'][0]['text']))

        self.info("Navigate to contact edit page")
        self.contacts_page.get_contact_edit_page_by_id(contact_response['company']['companyId'])
        self.info('update department')
        new_updated_departments = self.contact_page.update_department_list(
            departments=[self.contact_page.generate_random_text()]).split(", ")
        self.info("Department updated to {}".format(new_updated_departments))
        self.info('Navigate to order edit page and get department')
        self.order_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        table_suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        department = self.base_selenium.get_row_cells_id_dict_related_to_header(
            row=table_suborders[0], table_element='order:suborder_table')['departments'].split(",")
        self.assertCountEqual(department, new_updated_departments)

    @parameterized.expand(['ok', 'cancel'])
    def test013_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table

        LIMS-6203
        """
        self.info('press on create new contact button')
        self.base_selenium.click(element='contacts:new_contact')
        self.contact_page.sleep_medium()
        self.info('click on Overview, this will display an alert to the user')
        self.base_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.base_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}contacts'.format(self.base_selenium.url))
            self.info('clicking on Overview confirmed')
        else:
            self.base_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}contacts/add'.format(self.base_selenium.url))
            self.info('clicking on Overview cancelled')

    @parameterized.expand(['edit_overview', 'edit_cancel', 'overview'])
    def test014_edit_approach_overview_button(self, case):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202

        New: Contact: Cancel button: After I edit in any field
        then press on cancel button, a pop up will appear that
        the data will be lost
        LIMS-3585

        Contacts: No popup should appear when clicking on overview without changing anything
        LIMS-6816

        Contacts: Popup should appear when clicking on overview without saving <All data will be lost>
        LIMS-6808
        """
        self.info("open edit page random contact")
        self.contacts_page.get_random_contact()
        contact_url = self.base_selenium.get_url()
        self.contacts_page.info('contact_url : {}'.format(contact_url))
        if case in ['edit_overview', 'edit_cancel']:
            new_name = self.generate_random_string()
            self.contact_page.set_contact_name(new_name)

        if case == 'edit_cancel':
            self.base_selenium.click(element='general:cancel')
        else:
            self.contacts_page.info('click on Overview ')
            self.base_page.click_overview()

        if case in ['edit_overview', 'edit_cancel']:
            self.info('Clicked overview after editing without saving - Asserting popup appears')
            self.assertTrue(self.contacts_page.confirm_popup(check_only=True))
            self.base_selenium.click(element='general:confirm_pop')
        self.contacts_page.sleep_tiny()
        self.assertEqual(self.base_selenium.get_url(), '{}contacts'.format(self.base_selenium.url))
        self.contacts_page.info('clicking on Overview confirmed')

    def test015_contacts_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page

        LIMS-6201
        """
        self.info('select random Contact')
        contacts_response, _ = self.contacts_api.get_all_contacts(limit=10)
        self.assertEqual(contacts_response['status'], 1)
        random_contact_data = random.choice(contacts_response['contacts'])
        contact_name = random_contact_data['name']
        search_results = self.contact_page.search(contact_name)
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        self.info('navigate to Orders page')
        Order().get_orders_page()
        self.assertEqual(self.base_selenium.get_url(), '{}sample/orders'.format(self.base_selenium.url))

    def test016_create_user_with_role_contact(self):
        """
        New: Contact: User management: All the contacts created should be
        found when I create new user with role contact

        LIMS-3569
        """
        self.header_page = Header()
        contact_request, _ = self.contacts_api.get_all_contacts()
        self.assertEqual(contact_request['status'], 1)
        self.assertNotEqual(contact_request['count'], 0)
        contacts_records = contact_request['contacts']
        contact_name = contacts_records[0]['name']
        self.info("Navigate to users page")
        self.header_page.get_users_page()
        user_name = self.header_page.generate_random_text()
        self.info('random username generate is {}'.format(user_name))
        user_pw = self.header_page.generate_random_text()
        self.info('random user password generate is {}'.format(user_pw))
        user_mail = self.header_page.generate_random_email()
        self.info('random user email generate is {}'.format(user_mail))
        self.info('contact that user will be created with is {}'.format(contact_name))
        self.info('create new user with the randomly generated data')
        self.header_page.create_new_user(user_role='Contact', user_password=user_pw,
                                         user_confirm_password=user_pw, contact=contact_name,
                                         user_email=user_mail, user_name=user_name)
        self.info('search with the user name to make sure that it was created with the correct data')
        user_record = self.header_page.search(user_name)[0]
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=user_record)

        self.info('compare the user data with the randomly generated data')
        self.assertEqual(user_name, row_data['Name'])
        self.assertEqual(contact_name, row_data['Contact'])

    def test017_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        self.assertFalse(self.contacts_page.deselect_all_configurations())

    @parameterized.expand([('name', 'name', 'Contact Name'),
                           ('skype', 'skype', 'Skype'),
                           ('companyNo', 'contact_no_filter', 'Contact No'),
                           ('email', 'email_filter', 'Email'),
                           ('postalCode', 'postalcode_filter', 'Postal Code'),
                           ('website', 'website', 'Website'),
                           ('createdAt', 'created_on_field', 'Created On'),
                           ('phone', 'phone', 'Phone'),
                           ('location', 'location', 'Location')])
    def test018_filter_by_contact_text(self, attribute, filter_element, key):
        """
        Contacts: Filter Approach: Make sure you can filter by Name, skype, Number, Email, Postal Code,
        Website, Created On, Phone and Location

        LIMS-6408, LIMS-6418, LIMS-6409, LIMS-6414, LIMS-6419,
        LIMS-6415, LIMS-6420, LIMS-6412 and LIMS-6417
        """
        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute=attribute)
        self.assertNotEqual(data_to_filter_with, False)
        if attribute == 'createdAt':
            data_to_filter_with = self.contact_page.convert_to_dot_date_format(date=data_to_filter_with)
        self.info('filter with {} {}'.format(attribute, data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:{}'.format(filter_element),
                                                filter_text=data_to_filter_with,
                                                field_type='text')
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            self.assertEqual(row_data[key].replace("'", ""), data_to_filter_with.replace("'", ""))
            counter = counter + 1

    @parameterized.expand([('departments', 'departments', 'Departments'),
                           ('country', 'country_filter', 'Country')])
    def test019_filter_by_contact_drop_down_feild(self, attribute, filter_element, key):
        """
        Contacts: Filter Approach: Make sure you can filter by departments and Country

        LIMS-6413
        LIMS-6411
        """
        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute=attribute)
        self.assertNotEqual(data_to_filter_with, False)
        if attribute == 'departments':
            data_to_filter_with = data_to_filter_with.split(',')[0]
        self.info('filter with {} {}'.format(attribute, data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:{}'.format(filter_element),
                                                filter_text=data_to_filter_with)
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            if attribute == 'country':
                self.assertEqual(row_data[key], data_to_filter_with)
            else:
                self.assertIn(data_to_filter_with, row_data[key].split(', '))
            counter = counter + 1

    @attr(series=True)        
    def test020_filter_by_contact_changed_by(self):
        """
        Contacts: Filter Approach: Make sure you can filter by changed by

        LIMS-6410
        """
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.info("Navigate to contact page and create new contact")
        self.contacts_page.get_contacts_page()
        contact_data = self.contact_page.create_update_contact(contact_persons=False)
        self.contacts_page.set_all_configure_table_columns_to_specific_value(value=True)

        self.info('New contact is created successfully with name: {}'.format(contact_data["Contact Name"]))
        self.info('filter with last modified user {}'.format(payload['username']))
        self.contact_page.apply_filter_scenario(filter_element='contact:last_modified_user_field',
                                                filter_text=payload['username'])
        row_data = self.contact_page.get_the_latest_row_data()
        self.assertEqual(row_data['Changed By'], payload['username'])
        self.assertEqual(row_data['Contact Name'], contact_data['Contact Name'])
        self.assertEqual(row_data['Contact No'], contact_data['Contact No'])

    def test021_filter_by_contact_type(self):
        """
        Contacts: Filter Approach: Make sure you can filter by type

        LIMS-6421
        """
        data_to_filter_with = self.contacts_api.get_first_record_with_data_in_attribute(attribute='type')
        self.assertTrue(data_to_filter_with)
        data_to_filter_with = self.contact_page.get_mapped_contact_type(contact_type=data_to_filter_with[0])

        self.info('filter with {}'.format(data_to_filter_with))
        self.contact_page.apply_filter_scenario(filter_element='contact:type_filter', filter_text=data_to_filter_with)
        table_records = self.contact_page.result_table()
        counter = 0
        while counter < (len(table_records) - 1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=table_records[counter])
            contact_type = row_data['Contact Type'].split(', ')
            self.assertIn(data_to_filter_with, contact_type)
            counter = counter + 1

    def test022_add_contact_title(self):
        """
        Contacts: Contact person will have a title field to choose (Mr. or Ms)

        LIMS-6491
        """
        self.info("create contact")
        contact_data = self.contact_page.create_update_contact(save=False, contact_persons=False)
        self.info('Open contact persons page')
        self.contacts_page.sleep_tiny()
        self.contact_page.get_contact_persons_page()
        self.info('Create contact person with Mr.')
        contact_person_data = self.contact_page.create_update_contact_person(title='Mr.', save=False)
        self.info('Asserting the title set to  Mr.')
        self.assertEqual(contact_person_data[0]['title'], 'Mr.')
        self.info("update Title to be Ms")
        self.contacts_page.sleep_tiny()
        self.contact_page.create_update_contact_person(create=False, title='Ms', save=True, indexToEdit=0)
        self.contact_page.sleep_small()
        self.contacts_page.search_find_row_open_edit_page(contact_data['Contact No'])
        new_contact_person_data = self.contact_page.get_contact_persons_data()
        self.info('Asserting the title was changed successfully to Ms')
        self.assertEqual(new_contact_person_data[0]['title'], 'Ms')

    @attr(series=True)
    def test023_contact_title_translation(self):
        """
        Contacts: Title translation approach:
        Mr. >> Herr
        Ms >> Frau
        LIMS-6492
        """
        self.my_profile_page = MyProfile()
        contact_with_mr, payload = self.contacts_api.create_contact_with_person()
        self.assertEqual(contact_with_mr['status'], 1, 'cannot create contact')
        contact_with_ms, payload = self.contacts_api.create_contact_with_person(gender='Ms')
        self.assertEqual(contact_with_ms['status'], 1, 'cannot create contact')
        self.info('Navigating to My profile to change the language to German')
        self.my_profile_page.get_my_profile_page()
        self.my_profile_page.chang_lang('DE')
        self.info("Navigate to the contacts page to assert that the first contact's person is saved with title 'Herr'")
        self.contact_page.get_contact_edit_page_by_id(contact_with_mr['company']['companyId'])
        contact_person_data_first_contact = self.contact_page.navigate_to_contact_person_tab_get_data()
        self.info('Asserting the title of the first contact person in the '
                  'first contact: {} was translated successfully to Herr'.
                  format(contact_with_ms['company']['name']))
        self.assertEqual(contact_person_data_first_contact['title'], 'Herr')
        self.info("Navigate to the contacts page to assert that the second contact's person is saved with title 'Frau'")
        self.contact_page.get_contact_edit_page_by_id(contact_with_ms['company']['companyId'])
        contact_person_data_second_contact = self.contact_page.navigate_to_contact_person_tab_get_data()
        self.info('Asserting the title of the first contact person in the '
                  'second contact: {} was translated successfully to Frau'.
                  format(contact_with_ms['company']['name']))
        self.assertEqual(contact_person_data_second_contact['title'], 'Frau')

        # set the language back to english
        self.info('Navigating to My Profile to change the language back to English')
        self.my_profile_page.get_my_profile_page()
        self.my_profile_page.chang_lang('EN')
