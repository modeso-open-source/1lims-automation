import re
from unittest import skip
from parameterized import parameterized
from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from ui_testing.pages.analysis_page import SingleAnalysisPage
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from ui_testing.pages.contacts_page import Contacts
from random import randint
import random


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.article_api = ArticleAPI()
        self.test_unit_api = TestUnitAPI()
        self.single_analysis_page = SingleAnalysisPage()
        self.test_plan_api = TestPlanAPI()
        self.contacts_api = ContactsAPI()
        self.general_utilities_api = GeneralUtilitiesAPI()
        self.contacts_page = Contacts()
        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.order_page.get_orders_page()

    # will continue with us
    @parameterized.expand(['save_btn', 'cancel'])
    @skip('https://modeso.atlassian.net/browse//LIMS-4768')
    def test001_cancel_button_edit_no(self, save):
        """
        New: Orders: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be
        LIMS-5241
        :return:
        """
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        current_no = self.order_page.get_no()
        new_no = self.generate_random_string()
        self.order_page.set_no(new_no)
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(
            url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        order_no = self.order_page.get_no()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_no) == {} (order_no)'.format(new_no, order_no))
            self.assertEqual(new_no, order_no)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_no) == {} (order_no)'.format(current_no, order_no))
            self.assertEqual(current_no, order_no)

    @parameterized.expand(['save_btn', 'cancel'])
    def test002_update_contact_with_save_cancel_btn(self, save):
        """
        Orders: In case I update the contact then press on cancel button, a pop up should display with ( ok & cancel )
        buttons and when I press on cancel button, this update shouldn't submit
        LIMS-4764
        LIMS-4764
        :return:
        """
        orders, payload = self.orders_api.get_all_orders(limit=40)
        random_order = random.choice(orders['orders'])

        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        order_url = self.base_selenium.get_url()
        self.info(' + order_url : {}'.format(order_url))
        current_contact = self.order_page.get_contact_field()
        self.order_page.set_contact()
        new_contact = self.order_page.get_contact_field()
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        order_contact = self.order_page.get_contact_field()
        if 'save_btn' == save:
            self.info(
                ' + Assert {} (new_contact) == {} (order_contact)'.format(new_contact, order_contact))
            self.assertEqual(new_contact, order_contact)
        else:
            self.info(
                ' + Assert {} (current_contact) == {} (order_contact)'.format(current_contact, order_contact))
            self.assertEqual(current_contact, order_contact)

    # will continue with us
    @parameterized.expand(['save_btn', 'cancel'])
    def test003_cancel_button_edit_departments(self, save):
        """
        Orders: department Approach: In case I update the department then press on save button ( the department updated successfully) &
        when I press on cancel button ( this department not updated )
        LIMS-4765
        LIMS-4765
        :return:
        """
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        self.order_page.sleep_tiny()
        current_departments = self.order_page.get_department()
        self.order_page.set_departments()
        new_departments = self.order_page.get_department()
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        order_departments = self.order_page.get_department()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_departments) == {} (order_departments)'.format(new_departments, order_departments))
            self.assertEqual(new_departments, order_departments)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_departments) == {} (order_departments)'.format(current_departments,
                                                                                      order_departments))
            self.assertEqual(current_departments, order_departments)

    def test004_archive_main_order(self):
        '''
        LIMS-6516
        User can archive a main order
        '''
        orders, payload = self.orders_api.get_all_orders(limit=20)
        order = random.choice(orders['orders'])
        order_no = order['orderNo']
        self.order_page.apply_filter_scenario(filter_element='orders:filter_order_no', filter_text=order_no,
                                              field_type='text')
        row = self.order_page.get_last_order_row()
        self.order_page.click_check_box(source=row)
        self.orders_page.archive_selected_items()

        self.orders_page.get_archived_items()
        self.orders_page.search(order_no)
        results = self.order_page.result_table()[0].text
        self.assertIn(order_no.replace("'", ""), results.replace("'", ""))

    def test004_archive_order(self):
        """
            New: Orders: Archive
            The user cannot archive an order unless all corresponding analysis are archived
            LIMS-3425
            New: Archive order has active analysis
            The user cannot archive an order unless all corresponding analysis are archived
            LIMS-4329
        :return:
        """
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        analysis_numbers_list = order_data['Analysis No.'].split(',')
        self.base_selenium.LOGGER.info(
            ' + Try to archive order with number : {}'.format(order_data['Order No.']))
        order_deleted = self.order_page.archive_selected_orders(
            check_pop_up=True)
        self.base_selenium.LOGGER.info(' + {} '.format(order_deleted))

        if order_deleted:
            self.base_selenium.LOGGER.info(
                ' + Order number : {} deleted successfully'.format(order_data['Order No.']))
            self.analyses_page.get_analyses_page()
            self.base_selenium.LOGGER.info(
                ' + Assert analysis numbers : {} is not active'.format(analysis_numbers_list))
            has_active_analysis = self.analyses_page.search_if_analysis_exist(
                analysis_numbers_list)
            self.base_selenium.LOGGER.info(
                ' + Has activated analysis? : {}.'.format(has_active_analysis))
            self.assertFalse(has_active_analysis)
        else:
            self.analyses_page.get_analyses_page()
            self.base_selenium.LOGGER.info(
                ' + Archive Analysis with numbers : {}'.format(analysis_numbers_list))
            self.analyses_page.search_by_number_and_archive(
                analysis_numbers_list)
            self.order_page.get_orders_page()
            rows = self.order_page.search(analysis_numbers_list[0])
            self.order_page.click_check_box(source=rows[0])
            self.base_selenium.LOGGER.info(
                ' + archive order has analysis number =  {}'.format(analysis_numbers_list[0]))
            self.order_page.archive_selected_orders()
            rows = self.order_page.result_table()
            self.assertEqual(len(rows), 1)

    def test005_restore_archived_orders(self):
        """
        Restore Order
        I can restore any order successfully
        LIMS-4374
        """
        self.orders_page.get_archived_items()
        orders, payload = self.orders_api.get_all_orders(deleted=1, limit=20)
        order = random.choice(orders['orders'])

        order_no = order['orderNo']
        self.info('order no: {}'.format(order_no))
        self.order_page.apply_filter_scenario(filter_element='orders:filter_order_no', filter_text=order_no,
                                              field_type='text')
        suborders_data = self.order_page.get_child_table_data(index=0)
        self.order_page.restore_table_suborder(index=0)
        self.info('make sure that suborder is restored successfully')
        if len(suborders_data) > 1:
            suborder_data_after_restore = self.order_page.get_table_data()
            self.assertNotEqual(suborder_data_after_restore[0], suborders_data[0])
        else:
            table_records_count = len(self.order_page.result_table()) - 1
            self.assertEqual(table_records_count, 0)

        self.orders_page.get_orders_page()
        analysis_no = self.order_page.search(suborders_data[0]['Analysis No.'])
        self.single_analysis_page.open_child_table(source=analysis_no[0])
        results = self.order_page.result_table(element='general:table_child')[0].text
        self.assertIn(suborders_data[0]['Analysis No.'].replace("'", ""), results.replace("'", ""))

    # will continue with us
    def test006_delete_main_order(self):
        """
        New: Order without/with article: Deleting of orders
        The user can hard delete any archived order
        LIMS-3257
        """
        orders, payload = self.orders_api.get_all_orders(limit=40, deleted=1)
        random_order = random.choice(orders['orders'])
        self.orders_page.get_archived_items()
        order_row =self.orders_page.search(random_order['orderNo'])[0]

        self.order_page.click_check_box(source=order_row)

        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        order_number = order_data['Order No.'].split(',')

        self.info(
            ' + Delete order has number = {}'.format(order_data['Order No.']))
        self.order_page.delete_selected_item()
        self.assertFalse(self.order_page.confirm_popup())
        deleted_order = self.orders_page.search(order_number)[0]
        self.assertTrue(deleted_order.get_attribute("textContent"), 'No records found')
        self.order_page.navigate_to_analysis_tab()
        deleted_order = self.orders_page.search(order_number)[0]
        self.assertTrue(deleted_order.get_attribute("textContent"), 'No records found')

    # will continue with us
    @parameterized.expand(['True', 'False'])
    def test007_order_search(self, small_letters):
        """
        New: Orders: Search Approach: User can search by any field & each field should display with yellow color
        LIMS-3492
        LIMS-3061
        :return:
        """
        orders = self.orders_api.get_all_orders(limit=1).json()['orders'][0]
        rows = self.order_page.search(orders['orderNo'])
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=rows[0])
        for column in row_data:
            search_by = row_data[column].split(',')[0]
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[
                column] == '' or column == 'Time Difference' or row_data[column] == '-':
                continue
            elif column == 'Analysis Results':
                search_by = row_data[column].split(' (')[0]

            row_data[column] = row_data[column].split(',')[0]
            self.base_selenium.LOGGER.info(
                ' + search for {} : {}'.format(column, row_data[column]))
            if small_letters == 'True':
                search_results = self.order_page.search(search_by)
            else:
                search_results = self.order_page.search(search_by.upper())

            self.assertGreater(
                len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(
                    search_result)
                if search_data[column].replace("'", '').split(',')[0] == row_data[column].replace("'", '').split(',')[
                    0]:
                    break
            self.assertEqual(row_data[column].replace("'", '').split(',')[0],
                             search_data[column].replace("'", '').split(',')[0])

    def test008_duplicate_main_order(self):
        """
        New: Orders with test units: Duplicate an order with test unit 1 copy
        LIMS-3270
        :return:
        """
        # get the random main order data
        main_order = self.order_page.get_random_main_order_with_sub_orders_data()
        # select the order
        self.order_page.click_check_box(main_order['row_element'])
        # duplicate the main order
        self.order_page.duplicate_main_order_from_table_overview()
        # get the new order data
        after_duplicate_order = self.order_page.get_suborder_data()

        # ignore contact no since the table view doesn't have contact No.
        for contact in after_duplicate_order['contacts']:
            contact['no'] = None

        for index in range(len(main_order['suborders'])):
            # ignore analysis no. since it won't be created in the form until saving
            main_order['suborders'][index]['analysis_no'] = ''
            # ignore testunit numbers since the table view only got the name
            for testunit in after_duplicate_order['suborders'][index]['testunits']:
                testunit['no'] = None

        # make sure that its the duplication page
        self.assertTrue('duplicateMainOrder' in self.base_selenium.get_url())
        # make sure that the new order has different order No
        self.assertNotEqual(main_order['orderNo'], after_duplicate_order['orderNo'])
        # compare the contacts
        self.assertCountEqual(main_order['contacts'], after_duplicate_order['contacts'])
        # compare the data of suborders data in both orders
        self.assertCountEqual(main_order['suborders'], after_duplicate_order['suborders'])

        # save the duplicated order
        self.order_page.save(save_btn='orders:save_order')
        # go back to the table view
        self.order_page.get_orders_page()
        # search for the created order no
        self.order_page.search(after_duplicate_order['orderNo'])
        # get the search result text
        results = self.order_page.result_table()[0].text
        # check that it exists
        self.assertIn(after_duplicate_order['orderNo'], results)

    # will continue with us
    def test009_export_order_sheet(self):
        """
        New: Orders: XSLX Approach: user can download all data in table view with the same order with table view
        LIMS-3274
        :return:
        """
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.order_page.select_all_records()
        self.order_page.download_xslx_sheet()
        rows_data = self.order_page.get_table_rows_data()
        for index in range(len(rows_data) - 1):
            self.base_selenium.LOGGER.info(
                ' * Comparing the order no. {} '.format(index + 1))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.order_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    # will continue with us
    def test010_user_can_add_suborder(self):
        """
        New: Orders: Table view: Suborder Approach: User can add suborder from the main order
        LIMS-3817
        LIMS-4279
        Only "Apply this from add new item in the order table view"
        :return:
        """
        test_plan_dict = self.get_active_article_with_tst_plan(
            test_plan_status='complete')

        self.order_page.get_orders_page()
        order_row = self.order_page.get_random_order_row()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        orders_duplicate_data_before, orders = self.order_page.get_orders_duplicate_data(
            order_no=order_data['Order No.'])
        orders_records_before = self.order_page.get_table_records()

        self.base_selenium.LOGGER.info(
            ' + Select random order with {} no.'.format(order_data['Order No.']))

        self.order_page.get_random_x(orders[0])

        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + Order url : {}'.format(order_url))

        self.order_page.create_new_suborder(material_type=test_plan_dict['Material Type'],
                                            article_name=test_plan_dict['Article Name'],
                                            test_plan=test_plan_dict['Test Plan Name'])
        self.order_page.save(save_btn='order:save_btn')

        self.order_page.get_orders_page()
        orders_duplicate_data_after, _ = self.order_page.get_orders_duplicate_data(
            order_no=order_data['Order No.'])
        orders_records_after = self.order_page.get_table_records()

        self.base_selenium.LOGGER.info(
            ' + Assert there is a new suborder with the same order no.')
        self.assertEqual(orders_records_after, orders_records_before + 1)

        self.single_analysis_page.get_analysis_page()
        self.base_selenium.LOGGER.info(
            ' + Assert There is an analysis for this new suborder.')
        orders_analyess = self.single_analysis_page.search(order_data['Order No.'])
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            orders_duplicate_data_after[0]['Analysis No.'], latest_order_data['Analysis No.'])

    # will change that the duplicate many copies will be from the the child table not from the active table     
    def test012_duplicate_many_orders(self):
        """
        New: Orders: Duplication from active table Approach: When I duplicate order 5 times, it will create 5 analysis records with the same order number
        LIMS-4285
        :return:
        """
        number_of_copies = randint(2, 5)
        self.base_selenium.LOGGER.info(' Select Random Order')
        selected_row = self.order_page.get_random_order_row()
        selected_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=selected_row)
        self.order_page.click_check_box(source=selected_row)
        self.base_selenium.LOGGER.info(
            'Duplicate selected order  {} times  '.format(number_of_copies))
        self.order_page.duplicate_order_from_table_overview(number_of_copies)
        table_rows = self.order_page.result_table()
        self.base_selenium.LOGGER.info(
            'Make sure that created orders has same data of the oringal order')
        for index in range(number_of_copies):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(
                row=table_rows[index])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} with analyis  '.format(index + 1, ))
            self.assertTrue(row_data['Analysis No.'])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} has order number = {}   '.format(index + 1,
                                                                                     selected_order_data['Order No.']))
            self.assertEqual(
                selected_order_data['Order No.'], row_data['Order No.'])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} has Contact Name = {}   '.format(index + 1, selected_order_data[
                    'Contact Name']))
            self.assertEqual(
                selected_order_data['Contact Name'], row_data['Contact Name'])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} has Material Type = {}   '.format(index + 1, selected_order_data[
                    'Material Type']))
            self.assertEqual(
                selected_order_data['Material Type'], row_data['Material Type'])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} has Article Name = {}   '.format(index + 1, selected_order_data[
                    'Article Name']))
            self.assertEqual(
                selected_order_data['Article Name'], row_data['Article Name'])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} has Article Number = {}   '.format(index + 1, selected_order_data[
                    'Article No.']))
            self.assertEqual(
                selected_order_data['Article No.'], row_data['Article No.'])
            self.base_selenium.LOGGER.info(
                'Check if order created number:  {} has Shipment Date = {}   '.format(index + 1, selected_order_data[
                    'Shipment Date']))
            self.assertEqual(
                selected_order_data['Shipment Date'], row_data['Shipment Date'])
            self.base_selenium.LOGGER.info('Check if order created number:  {} has Test Date = {}   '.format(index + 1,
                                                                                                             selected_order_data[
                                                                                                                 'Test Date']))
            self.assertEqual(
                selected_order_data['Test Date'], row_data['Test Date'])
            self.base_selenium.LOGGER.info('Check if order created number:  {} has Test Plan = {}   '.format(index + 1,
                                                                                                             selected_order_data[
                                                                                                                 'Test Plans']))
            self.assertEqual(
                selected_order_data['Test Plans'], row_data['Test Plans'])

    # will continue with us
    # @skip("https://modeso.atlassian.net/browse/LIMS-4782")
    def test013_update_order_number(self):
        """
        New: Orders: Table: Update order number Approach: When I update order number all suborders inside it updated it's order number,
        and also in the analysis section.
        LIMS-4270
        """
        self.base_selenium.LOGGER.info(
            ' Running test case to check that when order no is updated, all suborders are updated')

        # create order with multiple suborders
        self.base_selenium.LOGGER.info(
            ' Create order with 5 sub orders to make sure of the count of the created/ updated orders')
        order_no_created = self.order_page.create_new_order(material_type='r', article='a', contact='a',
                                                                test_plans=['a'],
                                                                test_units=['a'], multiple_suborders=5)
        self.base_selenium.LOGGER.info(
            ' + orders_created_with_number : {}'.format(order_no_created))
        order_no_created = order_no_created.replace("'", '')

        # filter by the created order number and get the count
        orders_result = self.orders_page.search(order_no_created)
        self.base_selenium.LOGGER.info(
            ' + filter_by_order_no : {}'.format(order_no_created))
        orders_count = self.order_page.get_table_records()
        self.base_selenium.LOGGER.info(
            ' + count_of_the_created_orders : {}'.format(orders_count))

        # open the last created order to update its number and checking whether it will affect the rest of the orders or not
        self.order_page.get_random_x(row=orders_result[0])
        new_order_no = self.order_page.generate_random_text()
        self.order_page.set_no(no=new_order_no)
        self.order_page.save(save_btn='order:save_btn')
        self.base_selenium.LOGGER.info(
            ' + order_updated_with_number : {}'.format(new_order_no))
    
    @parameterized.expand(['save_btn', 'cancel'])
    def test014_update_first_order_material_type(self, save):
        """
        New: Orders: Edit material type: Make sure that user able to change material type of the first suborder and related test plan &
        article.
        New: Orders: Materiel type Approach: In case then material type of the first suborder updated then press on cancel button,
        Nothing update when I enter one more time
        LIMS-4281
        LIMS-4282
        :return:
        """
        test_plan_dict = self.get_active_article_with_tst_plan(
            test_plan_status='complete')

        self.order_page.get_orders_page()
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        order_material_type = self.order_page.get_material_type_of_first_suborder()
        self.order_page.set_material_type_of_first_suborder(
            material_type=test_plan_dict['Material Type'])
        self.order_page.confirm_popup(force=True)
        self.order_page.set_article(
            article=test_plan_dict['Article Name'])
        self.order_page.set_test_plan(
            test_plan=test_plan_dict['Test Plan Name'])
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)
        self.base_selenium.get(url=order_url, sleep=5)
        current_material_type = self.order_page.get_material_type_of_first_suborder()

        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_material_type) == {} (new_material_type)'.format(current_material_type,
                                                                                        test_plan_dict[
                                                                                            'Material Type']))
            self.assertEqual(test_plan_dict['Material Type'],
                             current_material_type)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_material_type) == {} (order_material_type)'.format(current_material_type,
                                                                                          order_material_type))
            self.assertEqual(current_material_type, order_material_type)

    # wiill continue with us
    def test015_filter_by_any_fields(self):
        """
        New: Orders: Filter Approach: I can filter by any field in the table view
        LIMS-3495
        """
        order_row = self.order_page.get_random_order_row()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        filter_fields_dict = self.order_page.order_filters_element()
        self.order_page.open_filter_menu()
        for key in filter_fields_dict:
            field = filter_fields_dict[key]
            self.order_page.filter(
                key, field['element'], order_data[key], field['type'])
            filtered_rows = self.order_page.result_table()
            for index in range(len(filtered_rows) - 1):
                row_data = self.base_selenium.get_row_cells_dict_related_to_header(
                    row=filtered_rows[index])
                self.base_selenium.LOGGER.info(
                    ' Assert {} in  (table row: {}) == {} '.format(key, index + 1, order_data[key]))
                self.assertEqual(order_data[key].replace(
                    "'", ""), row_data[key].replace("'", ""))
            self.order_page.filter_reset()

    # will continue with us
    def test016_validate_order_test_unit_test_plan(self):
        """
        New: orders Test plan /test unit validation
        LIMS-4349
        """
        self.base_selenium.LOGGER.info(
            ' Running test case to check that at least test unit or test plan is mandatory in order')

        self.order_page.create_new_order(material_type='r', article='a', contact='a', test_plans=[''],
                                         test_units=[''], multiple_suborders=0)
        # check both test plans and test units fields have error
        test_plan_class_name = self.base_selenium.get_attribute(
            element="order:test_plan", attribute='class')
        test_unit_class_name = self.base_selenium.get_attribute(
            element="order:test_unit", attribute='class')
        self.assertIn('has-error', test_plan_class_name)
        self.assertIn('has-error', test_unit_class_name)

        self.base_selenium.LOGGER.info(
            ' Choose Test Plan and save')
        # choose test plan and save
        self.order_page.set_test_plan(test_plan='r')
        self.order_page.save(save_btn='order:save_btn')

        self.base_selenium.LOGGER.info(
            ' Retry the test case but choose test unit and save')
        # try one more time but choose test unit and save
        self.order_page.create_new_order(material_type='r', article='a', contact='a', test_plans=[''],
                                         test_units=[''], multiple_suborders=0)
        self.order_page.set_test_unit(test_unit='r')
        self.order_page.save(save_btn='order:save_btn')

    # will continue wih us
    def test017_validate_order_test_unit_test_plan_edit_mode(self):
        """
        New: orders Test plan /test unit validation in edit mode
        LIMS-4826
        """
        self.base_selenium.LOGGER.info(
            ' Running test case to check that at least test unit or test plan is mandatory in order')

        # validate in edit mode, go to order over view
        self.order_page.get_orders_page()
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))

        self.base_selenium.LOGGER.info(
            ' Remove all selected test plans and test units')
        # delete test plan and test unit
        if self.order_page.get_test_plan():
            self.order_page.clear_test_plan()
            self.order_page.confirm_popup(force=True)

        if self.order_page.get_test_unit():
            self.order_page.clear_test_unit()
            self.order_page.confirm_popup(force=True)

        self.order_page.save(save_btn='order:save_btn')
        # check both test plans and test units fields have error
        test_plan_class_name = self.base_selenium.get_attribute(element="order:test_plan", attribute='class')
        test_unit_class_name = self.base_selenium.get_attribute(element="order:test_unit", attribute='class')
        self.assertIn('has-error', test_plan_class_name)
        self.assertIn('has-error', test_unit_class_name)

    @parameterized.expand(['save_btn', 'cancel'])
    def test032_update_test_date(self, save):
        """
        New: Orders: Test Date: I can update test date successfully with cancel/save buttons

        LIMS-4780
        :return:
        """
        # open random order edit page
        self.order_page.get_random_order()
        # preserve the url
        order_url = self.base_selenium.get_url()
        # get all the suborders
        all_suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        # get random suborder row_id
        row_id = 0
        if len(all_suborders) > 1:
            row_id = randint(0, len(all_suborders) - 1)

        # change the test date
        new_test_date = self.order_page.update_suborder(sub_order_index=row_id, test_date=True)

        # save or cancel
        if 'save_btn' == save:
            self.order_page.sleep_medium()
            self.order_page.save(save_btn='order:save_btn')
            self.order_page.sleep_medium()
        else:
            self.order_page.cancel(force=True)

        # refresh the page
        self.info('reopen the edited order page')
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        # get the saved test_date
        saved_test_date = self.order_page.get_suborder_data()['suborders'][row_id]['test_date']

        # check if the test date changed or not
        if 'cancel' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_test_date) != {} (new_test_date)'.format(new_test_date, saved_test_date))
            self.assertNotEqual(saved_test_date, new_test_date)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_test_date) == {} (new_test_date)'.format(new_test_date, saved_test_date))
            self.assertEqual(saved_test_date, new_test_date)

    # will continue with us
    @parameterized.expand(['save_btn', 'cancel'])
    def test017_update_shipment_date(self, save):
        """
        New: Orders: Shipment date Approach: I can update shipment date successfully with save/cancel button
        LIMS-4779
        LIMS-4779
        :return:
        """
        # open random order edit page
        self.order_page.get_random_order()
        # open the url
        order_url = self.base_selenium.get_url()
        # get all the suborders
        all_suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        # get random suborder row_id
        row_id = 0
        if len(all_suborders) > 1:
            row_id = randint(0, len(all_suborders) - 1)

        # update the shipment date
        new_shipment_date = self.order_page.update_suborder(sub_order_index=row_id, shipment_date=True)

        # save or cancel
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
            self.order_page.sleep_medium()
        else:
            self.order_page.cancel(force=True)

        # refresh the page
        self.info('reopen the edited order page')
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        # get the saved shipment date
        saved_shipment_date = self.order_page.get_suborder_data()['suborders'][row_id]['shipment_date']

        # check if the shipment date changed or not
        if 'cancel' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_shipment_date) != {} (new_shipment_date)'.format(new_shipment_date,
                                                                                            saved_shipment_date))
            self.assertNotEqual(saved_shipment_date, new_shipment_date)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_shipment_date) == {} (new_shipment_date)'.format(new_shipment_date,
                                                                                            saved_shipment_date))
            self.assertEqual(saved_shipment_date, new_shipment_date)

    # will continue with us
    def test018_validate_order_no_exists(self):
        """
        New: Orders: Create new order and change the autogenerated number
        LIMS-3406
        """
        self.base_selenium.LOGGER.info('Running test case to check that order number should be unique')
        order_row = self.base_selenium.get_row_cells_dict_related_to_header(self.order_page.get_random_order_row())

        self.order_page.click_create_order_button()
        self.order_page.set_new_order()
        self.order_page.copy_paste(element='order:no', value=order_row['Order No.'])
        self.order_page.sleep_small()
        order_no_class_name = self.base_selenium.get_attribute(element="order:no", attribute='class')
        self.assertIn('has-error', order_no_class_name)
        order_error_message = self.base_selenium.get_text(element="order:order_no_error_message")
        self.assertIn('No. already exist', order_error_message)

    # will continue with us
    def test019_validate_order_no_archived_exists(self):
        """
        New: Orders: Create new order and change the autogenerated number
        LIMS-3406
        """
        self.base_selenium.LOGGER.info(
            ' Running test case to check that order number should be unique with archived one')

        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        analysis_numbers_list = order_data['Analysis No.'].split(',')
        self.base_selenium.LOGGER.info(
            ' + Try to archive order with number : {}'.format(order_data['Order No.']))
        order_deleted = self.order_page.archive_selected_orders(
            check_pop_up=True)
        self.base_selenium.LOGGER.info(' + {} '.format(order_deleted))

        if order_deleted:
            self.base_selenium.LOGGER.info(
                ' + Order number : {} deleted successfully'.format(order_data['Order No.']))
            self.analyses_page.get_analyses_page()
            has_active_analysis = self.analyses_page.search_if_analysis_exist(
                analysis_numbers_list)
            self.base_selenium.LOGGER.info(
                ' + Has activated analysis? : {}.'.format(has_active_analysis))
        else:
            self.analyses_page.get_analyses_page()
            self.base_selenium.LOGGER.info(
                ' + Archive Analysis with numbers : {}'.format(analysis_numbers_list))
            self.analyses_page.search_by_number_and_archive(
                analysis_numbers_list)
            self.order_page.get_orders_page()
            rows = self.order_page.search(analysis_numbers_list[0])
            self.order_page.click_check_box(source=rows[0])
            self.base_selenium.LOGGER.info(
                ' + archive order has analysis number =  {}'.format(analysis_numbers_list[0]))
            self.order_page.archive_selected_orders()

        self.base_selenium.LOGGER.info(
            ' Creating new order with number ' + order_data['Order No.'])
        self.order_page.click_create_order_button()
        self.order_page.set_new_order()
        self.order_page.sleep_tiny()
        self.order_page.copy_paste(element='order:no', value=order_data['Order No.'])
        self.order_page.sleep_tiny()
        order_no_class_name = self.base_selenium.get_attribute(
            element="order:no", attribute='class')
        self.assertIn('has-error', order_no_class_name)
        order_error_message = self.base_selenium.get_text(
            element="order:order_no_error_message")
        self.assertIn('No. already exists in archived, you can go to Archive table and restore it', order_error_message)

    # will continue with us
    def test020_create_new_order_with_test_units(self):
        """
        New: Orders: Create a new order with test units
        LIMS-3267
        """
        self.base_selenium.LOGGER.info('Running test case to create a new order with test units')
        test_units_list = []
        test_unit_dict = self.get_active_tst_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        test_unit_dict = self.get_active_tst_unit_with_material_type(search='Quantitative')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        test_unit_dict = self.get_active_tst_unit_with_material_type(search='Quantitative Mibi')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])

        self.order_page.get_orders_page()
        created_order = self.order_page.create_new_order(material_type='r', article='a', contact='a',
                                                         test_units=test_units_list)

        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Assert There is an analysis for this new order.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
            testunit_name = row_with_headers['Test Unit']
            self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
            self.assertIn(testunit_name, test_units_list)

    def test021_create_existing_order_with_test_units(self):
        """
        New: Orders: Create an existing order with test units
        LIMS-3268
        """
        random_testunit, payload = self.test_unit_api.get_all_test_units(filter='{"materialTypes":"all"}')
        random_name = random.choice(random_testunit['testUnits'])

        self.order_page.get_orders_page()
        created_order = self.order_page.create_existing_order(no='',material_type='s', article='a', contact='',
                                                              test_units=[random_name['name']])
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.base_selenium.LOGGER.info(
            'Assert There is an analysis for this new order.')
        orders_analyess = self.analyses_page.search(value=created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
            testunit_name = row_with_headers['Test Unit']
            self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
            self.assertIn(testunit_name, random_name['name'])
            
    def test022_create_existing_order_with_test_units_and_change_material_type(self):
        """
        New: Orders with test units: Create a new order from an existing order with
        test units but change the material type
        LIMS-3269-case 1
        """   
        order_no = self.order_page.create_existing_order_with_auto_fill()
        self.order_page.sleep_tiny()

        self.order_page.set_material_type(material_type='Subassembely')
        self.assertEqual(self.base_selenium.get_value(element='order:article'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)

        article = self.order_page.set_article()
        test_unit = self.order_page.set_test_unit()
        self.order_page.save(save_btn='order:save_btn', sleep=True)

        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()

        self.info('Assert There is an analysis for this new order.')
        self.analyses_page.apply_filter_scenario(
            filter_element='orders:filter_order_no', filter_text=order_no, field_type='drop_down')
        latest_order_data = \
            self.base_selenium.get_row_cells_dict_related_to_header(row=self.analyses_page.result_table()[0])
        self.assertEqual(order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        self.assertEqual(article.split(' No:')[0], latest_order_data['Article Name'])
        self.assertEqual(test_unit.split(' Type:')[0], self.analyses_page.get_child_table_data()[0]['Test Unit'])
        self.assertEqual('Subassembely', latest_order_data['Material Type'])

    @skip("https://modeso.atlassian.net/browse/LIMSA-116")
    def test023_create_existing_order_with_test_units_and_change_article(self):
        """
        New: Orders with test units: Create a new order from an existing order with
        test units but change the article
        LIMS-3269- case 2
        """
        order_no = self.order_page.create_existing_order_with_auto_fill()
        self.order_page.sleep_tiny()

        test_unit = self.order_page.get_test_unit()
        material_type = self.order_page.get_material_type()
        article = self.order_page.set_article()
        # until bug in https://modeso.atlassian.net/browse/LIMSA-116 solved
        if self.order_page.get_test_unit() == [] and self.order_page.get_test_plan() == []:
            test_unit = self.order_page.set_test_unit()
        self.order_page.sleep_small()
        self.assertEqual(self.order_page.get_test_unit(), test_unit)
        self.assertEqual(self.order_page.get_material_type(), material_type)

        self.order_page.save(save_btn='order:save_btn')
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.info('Assert There is an analysis for this new order.')
        self.analyses_page.apply_filter_scenario(
            filter_element='orders:filter_order_no', filter_text=order_no, field_type='drop_down')

        latest_order_data = \
            self.base_selenium.get_row_cells_dict_related_to_header(row=self.analyses_page.result_table()[0])

        self.assertEqual(order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        self.assertEqual(article.split(' No:')[0], latest_order_data['Article Name'])
        self.assertEqual(test_unit, self.analyses_page.get_child_table_data()[0]['Test Unit'])
        self.assertEqual(material_type, latest_order_data['Material Type'])

    def test024_archive_sub_order(self):
        """
        New: Orders: Table:  Suborder /Archive Approach: : User can archive any suborder successfully
        LIMS-3739
        """
        orders, payload = self.orders_api.get_all_orders(limit =20)
        order = random.choice(orders['orders'])

        order_no = order['orderNo']
        self.info(('order no: {}'.format(order_no)))
        self.order_page.apply_filter_scenario(filter_element='orders:filter_order_no', filter_text=order_no,
                                              field_type='text')
        suborders_data = self.order_page.get_child_table_data(index=0)
        self.order_page.archive_table_suborder(index=0)
        self.info('make sure that suborder is archived successfully')
        if len(suborders_data) > 1:
            suborder_data_after_restore = self.order_page.get_table_data()
            self.assertNotEqual(suborder_data_after_restore[0], suborders_data[0])
        else:
            table_records_count = len(self.order_page.result_table()) - 1
            self.assertEqual(table_records_count, 0)
            
        self.base_selenium.refresh()
        self.orders_page.get_archived_items()
        analysis_no = self.order_page.search(suborders_data[0]['Analysis No.'])
        self.orders_page.open_child_table(source=analysis_no[0])
        results = self.order_page.result_table(element='general:table_child')[0].text
        self.assertIn(suborders_data[0]['Analysis No.'].replace("'", ""), results.replace("'", ""))

    # will continue with us
    @skip('https://modeso.atlassian.net/browse/LIMS-4914')
    def test027_update_material_type(self):
        """
        Apply this on suborder number 5 for example:-
        -When user update the materiel type from table view once I delete it message will appear
        (All analysis created with this order and test plan will be deleted )
        -Once you press on OK button, the material type & article & test pan will delete
        -You can update it by choose another one and choose corresponding article & test plan
        LIMS-4264
        """

        # new random order data
        basic_order_data = self.get_random_order_data()
        new_material_type = basic_order_data['material_type']
        new_article = basic_order_data['article_name']
        new_testplan_name = basic_order_data['testplan']
        testplan_testunits = basic_order_data['testunits_in_testplan']

        self.base_selenium.LOGGER.info('Create new order with intial data')
        # initial data is static because it won't affect the test case, but the updating data is generated dynamically
        self.order_page.create_new_order(multiple_suborders=3, test_plans=['tp1'], material_type='Raw Material',
                                         test_units=[''])

        self.base_selenium.LOGGER.info('Creating new order with 2 suborders')
        order_no = self.order_page.create_new_order(multiple_suborders=1, test_plans=['tp1'],
                                                    material_type='Raw Material')
        self.base_selenium.LOGGER.info('Created new order with no #{}, and test plan {}'.format(order_no, 'tp1'))

        # getting data of the created orders to make sure that everything created correctly
        rows = self.order_page.result_table()
        selected_order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
        analysis_no = selected_order_data['Analysis No.']

        self.order_page.get_random_x(row=rows[1])
        self.order_page.update_suborder(sub_order_index=1, test_plans=['tp2'])
        self.base_selenium.LOGGER.info('Update order with test plans: {}'.format('tp2'))
        sub_order_data = self.order_page.get_suborder_data(sub_order_index=1, test_plan=True)
        suborder_testplans = sub_order_data['test_plan']
        suborder_testplans = suborder_testplans.split('|')
        self.base_selenium.LOGGER.info('order update and has test plans: {}'.format(suborder_testplans))

        # getting the length of the table, should be 2
        self.base_selenium.LOGGER.info(
            'Get analysis page to filter with order no to make sure that new test plan did not trigger new analysis')
        self.analyses_page.get_analyses_page()

        self.base_selenium.LOGGER.info('Filter analysis page with order no: #{}'.format(order_no))
        analysis_records = self.analyses_page.search(value=order_no)
        analysis_count = len(analysis_records) - 1
        self.base_selenium.LOGGER.info(
            'comparing count of analysis triggered with this order after adding new test plan')
        self.base_selenium.LOGGER.info('analysis triggered count: {}, and it should be 2'.format(analysis_count))
        self.assertEqual(2, analysis_count)

        # get analysis data to make sure that the newly added test plan is added to analysis
        self.base_selenium.LOGGER.info(
            'Check the test plans in analysis from active table compared with selected test plans in order')
        selected_analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(row=analysis_records[0])
        analysis_test_plans = selected_analysis_data['Test Plans'].split(',')

        self.base_selenium.LOGGER.info('+ Comapring test plans in analysis and order')
        self.base_selenium.LOGGER.info(
            '+ Assert order\'s testplans are: {}, analysis test plans are: {}'.format(suborder_testplans,
                                                                                      analysis_test_plans))
        self.assertEqual(set(analysis_test_plans) == set(suborder_testplans), True)

        self.base_selenium.LOGGER.info('C omparing analysis status')
        # making sure that the status remained open after adding new test plan
        analysis_status = selected_analysis_data['Status']
        analysis_no_from_analysis_table = selected_analysis_data['Analysis No.']
        self.base_selenium.LOGGER.info(
            'Analysis with no #{}, has status: {}'.format(analysis_no_from_analysis_table, analysis_status))
        self.base_selenium.LOGGER.info(
            '+ Assert analysis has status: {}, and it should be: {}'.format(analysis_status, 'Open'))
        self.assertEqual(analysis_status, 'Open')

        # get order data to be updated
        self.base_selenium.LOGGER.info('Get order data to remove a test plan from the order')
        self.order_page.get_orders_page()

    # will continue with us & then put the test case number for it
    def test026_update_suborder_article(self):
        self.base_selenium.LOGGER.info('Order created with 4 suborders with the following data')
        self.base_selenium.LOGGER.info('Material type: {}, Article name: {}, Test plans: {}, Test Units: {}'.format(
            suborder_data['material_types'], suborder_data['article'], suborder_data['test_plan'],
            suborder_data['test_unit']))

        self.base_selenium.LOGGER.info(
            'Change Material type from {}, to {}, and press cancel'.format(suborder_data['material_types'],
                                                                           new_material_type))
        self.order_page.update_suborder(sub_order_index=3, material_type=new_material_type, form_view=False)
        self.base_selenium.LOGGER.info(
            'Change article from {}, to {}, and press cancel'.format(suborder_data['article'], new_article))
        self.order_page.update_suborder(sub_order_index=3, articles=new_article, form_view=False)
        self.base_selenium.click(element='order:confirm_cancel')

        self.base_selenium.LOGGER.info('Getting data after pressing cancel to make sure that it did not change')

        suborder_data_after_pressing_cancel = self.order_page.get_suborder_data(sub_order_index=3)

        self.base_selenium.LOGGER.info('Comparing order data after pressing cancel')

        self.base_selenium.LOGGER.info(
            '+Assert Compare Material type, old: {}, new: {}'.format(suborder_data['material_types'],
                                                                     suborder_data_after_pressing_cancel[
                                                                         'material_types']))
        self.assertEqual(suborder_data['material_types'], suborder_data_after_pressing_cancel['material_types'])

        self.base_selenium.LOGGER.info('+Assert Compare Article, old: {}, new: {}'.format(suborder_data['article'],
                                                                                          suborder_data_after_pressing_cancel[
                                                                                              'article']))
        self.assertEqual(suborder_data['article'], suborder_data_after_pressing_cancel['article'])

        self.base_selenium.LOGGER.info('+Assert Compare Test Plans, old: {}, new: {}'.format(suborder_data['test_plan'],
                                                                                             suborder_data_after_pressing_cancel[
                                                                                                 'test_plan']))
        self.assertEqual(suborder_data['test_plan'], suborder_data_after_pressing_cancel['test_plan'])

        self.base_selenium.LOGGER.info('+Assert Compare Test units, old: {}, new: {}'.format(suborder_data['test_unit'],
                                                                                             suborder_data_after_pressing_cancel[
                                                                                                 'test_unit']))
        self.assertEqual(suborder_data['test_unit'], suborder_data_after_pressing_cancel['test_unit'])

        self.base_selenium.LOGGER.info(
            'Change article from {}, to {}, and press confirm'.format(suborder_data['article'], new_article))
        self.order_page.update_suborder(sub_order_index=3, material_type=new_material_type, form_view=False)
        self.base_selenium.LOGGER.info(
            'Change article from {}, to {}, and press confirm'.format(suborder_data['article'], new_article))
        self.order_page.update_suborder(sub_order_index=3, articles=new_article, form_view=False)
        self.base_selenium.click(element='order:confirm_pop')

        self.base_selenium.LOGGER.info(
            'Get suborder data to make sure that all the data are removed after pressing confirm')

        suborder_data_after_pressing_confirm = self.order_page.get_suborder_data(sub_order_index=3)

        self.base_selenium.LOGGER.info('Comparing order data after pressing confirm')

        self.base_selenium.LOGGER.info(
            'Empty fields will have the word "Search" as a placeholder, so the results from the table will carry the value "Search" which denotes that the field is empty')
        self.base_selenium.LOGGER.info('+Assert Compare Material type, old: {}, new: {}'.format(new_material_type,
                                                                                                suborder_data_after_pressing_confirm[
                                                                                                    'material_types']))
        self.assertEqual(new_material_type, suborder_data_after_pressing_confirm['material_types'])

        self.base_selenium.LOGGER.info('+Assert Compare Article, old: {}, new: {}'.format('Search',
                                                                                          suborder_data_after_pressing_confirm[
                                                                                              'article']))
        self.assertEqual('Search', suborder_data_after_pressing_confirm['article'])

        self.base_selenium.LOGGER.info('+Assert Compare Test Plans, old: {}, new: {}'.format('Search',
                                                                                             suborder_data_after_pressing_confirm[
                                                                                                 'test_plan']))
        self.assertEqual('earch', suborder_data_after_pressing_confirm['test_plan'])

        self.base_selenium.LOGGER.info('+Assert Compare Test units, old: {}, new: {}'.format('Search',
                                                                                             suborder_data_after_pressing_confirm[
                                                                                                 'test_unit']))
        self.assertEqual('earch', suborder_data_after_pressing_confirm['test_unit'])

        self.base_selenium.LOGGER.info('Update data and press save to make sure that it is updated')

        self.order_page.update_suborder(sub_order_index=3, test_plans=[new_testplan_name],
                                        material_type=new_material_type, articles=new_article, test_units=[''],
                                        form_view=False)
        suborder_data_after_changing_data = self.order_page.get_suborder_data(sub_order_index=3)

        self.base_selenium.LOGGER.info('Update test plans from {}, to {}'.format(suborder_data['test_plan'],
                                                                                 suborder_data_after_changing_data[
                                                                                     'test_plan']))

        self.base_selenium.LOGGER.info(
            '+Assert Compare Material type, old: {}, new: {}'.format(suborder_data['material_types'],
                                                                     suborder_data_after_pressing_confirm[
                                                                         'material_types']))
        self.assertEqual(suborder_data['material_types'], suborder_data_after_pressing_confirm['material_types'])

        self.base_selenium.LOGGER.info('+Assert Compare Article, old: {}, new: {}'.format(new_article,
                                                                                          suborder_data_after_pressing_confirm[
                                                                                              'article']))
        self.assertEqual(new_article, suborder_data_after_pressing_confirm['article'])

        # written as earch because the function that retrieves the data removes the first char in case of test unit/ test plan to remove the 'x'
        # so in case no test unit or no test plan, it removes the first char in the placeholder word which is search, so i match with earch
        self.base_selenium.LOGGER.info('+Assert Compare Test Plans, old: {}, new: {}'.format('Search',
                                                                                             suborder_data_after_pressing_confirm[
                                                                                                 'test_plan']))
        self.assertEqual('earch', suborder_data_after_pressing_confirm['test_plan'])

        self.base_selenium.LOGGER.info('+Assert Compare Test units, old: {}, new: {}'.format(suborder_data['test_unit'],
                                                                                             suborder_data_after_pressing_confirm[
                                                                                                 'test_unit']))
        self.assertEqual(suborder_data['test_unit'], suborder_data_after_pressing_confirm['test_unit'])

        self.base_selenium.LOGGER.info('Update Test plans and press save to make sure that it is updated')

        self.order_page.update_suborder(sub_order_index=3, test_plans=[new_testplan], form_view=False)
        suborder_data_after_changing_testplans = self.order_page.get_suborder_data(sub_order_index=3)

        self.base_selenium.LOGGER.info('Update test plans from {}, to {}'.format(suborder_data['test_plan'],
                                                                                 suborder_data_after_changing_testplans[
                                                                                     'test_plan']))
        self.order_page.save(save_btn="order:save_btn")

    ### SYNTAX ERROR ###
    # will continue with us
    # this bug will only affect the delete case, but the adding case is working fine
    # @skip('https://modeso.atlassian.net/browse/LIMS-4915')
    # @skip('https://modeso.atlassian.net/browse/LIMS-4916')
    # @parameterized.expand(['add', 'delete'])
    # def test021_update_suborder_testunits(self, save):
    #     """
    #     Try this on suborder number 5 for example:-
    #     -When I delete test unit to update it message will appear
    #     ( This Test Unit will be removed from the corresponding analysis )
    #     -Make sure the corresponding analysis records created according to this update in test unit.

    #     LIMS-4269

    #     """

    #     # create order with 2 suborders to make sure that update in the suborder is working
    #     # order is create with Raw Material as a mteria type because it has multiple test units, and it won't affect the case logic, since the update is test unit related not material type related
    #     self.base_selenium.LOGGER.info('Creating new order with 2 suborders')
    #     order_no_created = self.order_page.create_new_order(multiple_suborders=1, material_type='Raw Material', test_units=['', ''])

    #     rows = self.order_page.search(value=order_no_created)
    #     selected_order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
    #     analysis_no = selected_order_data['Analysis No.']
    #     order_no = selected_order_data['Order No.']

    #     if save == 'add':
    #         # checking that when adding new test unit, the newly added test unit is added to the order's analysis instead of creating new analysis
    #         self.base_selenium.LOGGER.info('Update the 2nd suborder by adding new test unit')
    #         self.order_page.get_random_x(row=rows[1])
    #         self.order_page.update_suborder(sub_order_index=1, test_units=[''])
    #         suborder_testunits_before_refresh = self.order_page.get_suborder_data(sub_order_index=1)
    #         suborder_testunits_before_refresh = suborder_testunits_before_refresh['test_unit'].split('|')
    #         self.order_page.save(save_btn='order:save_btn')

    #         self.base_selenium.LOGGER.info('Refresh to make sure that data are saved correctly')
    #         self.base_selenium.refresh(sleep=10)

    #         self.base_selenium.LOGGER.info('Get suborder data to check it')
    #         self.order_page.get_suborder_table()
    #         suborder_testunits_after_refresh = self.order_page.get_suborder_data(sub_order_index=1)
    #         suborder_testunits_after_refresh = suborder_testunits_after_refresh['test_unit'].split('|')

    #         self.base_selenium.LOGGER.info('+ Assert Test units: test units are: {}, and should be: {}'.format(suborder_testunits_after_refresh, suborder_testunits_before_refresh))

    #     suborder_data_after_saving = self.order_page.get_suborder_data(sub_order_index=3)
    #         # getting the length of the table, should be 2
    #         self.base_selenium.LOGGER.info('Getting analysis page to check the data in this child table')
    #         self.analyses_page.get_analyses_page()

    #         self.base_selenium.LOGGER.info('Filter with order no to check analysis count')
    #         analysis_records=self.analyses_page.search(value=order_no)
    #         analysis_count = len(analysis_records) -1

    #     self.base_selenium.LOGGER.info('+Assert Compare Material type, old: {}, new: {}'.format(
    #         suborder_data_after_changing_data['material_types'], suborder_data_after_saving['material_types']))
    #     self.assertEqual(suborder_data_after_changing_data['material_types'],
    #                      suborder_data_after_saving['material_types'])

    #     self.base_selenium.LOGGER.info(
    #         '+Assert Compare Article, old: {}, new: {}'.format(suborder_data_after_changing_data['article'],
    #                                                            suborder_data_after_saving['article']))
    #     self.assertEqual(suborder_data_after_changing_data['article'], suborder_data_after_saving['article'])

    #     self.base_selenium.LOGGER.info(
    #         '+Assert Compare Test Plans, old: {}, new: {}'.format(suborder_data_after_changing_data['test_plan'],
    #                                                               suborder_data_after_saving['test_plan']))
    #     self.assertEqual(suborder_data_after_changing_data['test_plan'], suborder_data_after_saving['test_plan'])

    #     self.base_selenium.LOGGER.info(
    #         '+Assert Compare Test units, old: {}, new: {}'.format(suborder_data_after_changing_data['test_unit'],
    #                                                               suborder_data_after_saving['test_unit']))
    #     self.assertEqual(suborder_data_after_changing_data['test_unit'], suborder_data_after_saving['test_unit'])

    #     testplan_testunits.append(suborder_data_after_saving['test_unit'])

    #     self.base_selenium.LOGGER.info('Get analysis page to make sure that update took place in analysis')
    #     self.analyses_page.get_analyses_page()

    #     self.base_selenium.LOGGER.info(
    #         'Filter by order no: #{}, to make sure that no new analysis have been created'.format(
    #             basic_order_data['Order No.']))
    #     rows = self.analyses_page.search(value=basic_order_data['Order No.'])
    #     self.base_selenium.LOGGER.info('Count of analysis is #{}, and it shpuld be {}'.format(len(rows) - 1, 4))
    #     self.assertEqual(len(rows) - 1, 4)

    #     self.base_selenium.LOGGER.info(
    #         'Filter by analysis no: #{}, to check the order data'.format(basic_order_data['Analysis No.']))
    #     self.base_selenium.LOGGER.info('Get first row data, because it is the analysis of the updated order')
    #     rows = self.analyses_page.search(value=basic_order_data['Analysis No.'])

    #     analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])

    #     self.base_selenium.LOGGER.info(
    #         'Comparing analysis data with the updated order data to make sure that it is updated correctly')

    #     self.base_selenium.LOGGER.info('+Assert Material type, should be: {}, and it is: {}'.format(new_material_type,
    #                                                                                                 analysis_data[
    #                                                                                                     'Material Type']))
    #     self.assertEqual(new_material_type, analysis_data['Material Type'])

    #     self.base_selenium.LOGGER.info(
    #         '+Assert Article Name, should be: {}, and it is: {}'.format(new_article, analysis_data['Article Name']))
    #     self.assertEqual(new_article, analysis_data['Article Name'])

    #     self.base_selenium.LOGGER.info(
    #         '+Assert Test plans, should be: {}, and it is: {}'.format(suborder_data_after_saving['test_plan'],
    #                                                                   analysis_data['Test Plans']))
    #     self.assertEqual(suborder_data_after_saving['test_plan'], analysis_data['Test Plans'])
    #             analysis_test_units = []

    #     for testunit in analysis_child_table:
    #         analysis_test_units.append(testunit['Test Unit'])

    #     self.base_selenium.LOGGER.info(
    #         'analysis test units are: {}, and it should be: {}'.format(analysis_test_units, testplan_testunits))
    #     self.assertEqual(set(analysis_test_units) == set(testplan_testunits), True)

    # def test_test(self):
    #     import ipdb; ipdb.set_trace()
    #     suborder_data = self.order_page.get_suborder_data(sub_order_index=3)
    ### SYNTAX ERROR ###

    # will continue with us apply it from the second suborder & need test case number for it to apply from the second suborder
    @parameterized.expand(['save_btn', 'cancel'])
    def test025_update_contact_departments(self, save):
        """
        Orders: department Approach: In case I update the department then press on save button
        ( the department updated successfully )
        &
        when I press on cancel button ( this department not updated )

        LIMS-4765
        """
        self.base_selenium.LOGGER.info(
            'Getting contact with departments to make sure that the new selected contact has departments')
        new_contact = self.contacts_page.get_contact_with_departments()
        self.order_page.get_orders_page()

        self.base_selenium.LOGGER.info(
            'Create order with 2 suborders with any random data, just to test updating contacts/ departments')
        order_no_created = self.order_page.create_new_order(multiple_suborders=1, material_type='Raw Material',
                                                            article='', test_units=[''])

        self.base_selenium.LOGGER.info('Open the 2nd order from the table')
        rows = self.order_page.result_table()
        self.order_page.get_random_x(row=rows[1])

        self.base_selenium.LOGGER.info(
            'update the contact to {}, and select departments to make sure that it is update correctly'.format(
                new_contact))
        old_contact = self.order_page.get_contact()
        old_departments = self.order_page.get_departments()
        self.order_page.set_contact(contact=new_contact)

        self.base_selenium.LOGGER.info('Update the departments of the 2nd suborder')
        self.order_page.update_suborder(sub_order_index=1, departments=[''], form_view=True)
        suborder_data = self.order_page.get_suborder_data(sub_order_index=1)

        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
            self.base_selenium.LOGGER.info('Refresh to make sure that data are saved correctly')
            self.base_selenium.refresh()

            contact_after_update = self.order_page.get_contact()

            self.base_selenium.LOGGER.info(
                '+ Assert Contacts: contact is: {}, and should be: {})'.format(contact_after_update, new_contact))
            self.assertEqual(contact_after_update, new_contact)

            self.base_selenium.LOGGER.info('Get suborder data to compare it')
            self.order_page.get_suborder_table()
            order_data_after_refresh = self.order_page.get_suborder_data(sub_order_index=1)

            self.base_selenium.LOGGER.info('+ Assert Departments: departments are: {}, and should be: {})'.format(
                order_data_after_refresh['departments'], suborder_data['departments']))
            self.assertEqual(order_data_after_refresh['departments'], suborder_data['departments'])

            self.order_page.get_orders_page()
            self.base_selenium.LOGGER.info('Filter by order no')
            rows = self.order_page.search(value=order_no_created)

            for row in range(0, len(rows) - 1):
                if row:
                    temp_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[row])
                    self.base_selenium.LOGGER.info(
                        '+ Assert Contact in order active table: contact is: {}, and should be: {})'.format(
                            temp_data['Contact Name'], new_contact))
                    self.assertEqual(temp_data['Contact Name'], new_contact)

            suborder_data_from_table = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
            self.base_selenium.LOGGER.info(
                '+ Assert Departments in order active table, departments are {}, and should be {}'.format(
                    suborder_data_from_table['Departments'], order_data_after_refresh['departments']))
            self.assertEqual(suborder_data_from_table['Departments'], order_data_after_refresh['departments'])

            self.base_selenium.LOGGER.info(
                'Get analysis page to make sure that the updates have affected the analysis records')
            self.analyses_page.get_analyses_page()

            self.base_selenium.LOGGER.info('Filter by order no')
            rows = self.analyses_page.search(value=order_no_created)

            for row in range(0, len(rows) - 1):
                if row:
                    temp_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[row])
                    self.base_selenium.LOGGER.info(
                        '+ Assert Contact in analysis active table: contact is: {}, and should be: {})'.format(
                            temp_data['Contact Name'], new_contact))
                    self.assertEqual(temp_data['Contact Name'], new_contact)

            suborder_data_from_table = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
            self.base_selenium.LOGGER.info(
                '+ Assert Departments in analysis active table, departments are {}, and should be {}'.format(
                    suborder_data_from_table['Departments'], order_data_after_refresh['departments']))
            self.assertEqual(suborder_data_from_table['Departments'], order_data_after_refresh['departments'])

        else:
            self.order_page.cancel(force=True)
            self.order_page.sleep_tiny()
            self.base_selenium.LOGGER.info('Filter by order no to select the choosen order to check its data')
            rows = self.order_page.search(value=order_no_created)

            self.base_selenium.LOGGER.info('Select the choosen order to check its data')
            self.order_page.get_random_x(row=rows[1])

            contacta_after_pressing_cancel = self.order_page.get_contact()
            departmentsa_after_pressing_cancel = self.order_page.get_departments()

    # will continue with us
    @skip('https://modeso.atlassian.net/browse/LIMS-5070')
    def test031_user_can_add_suborder_with_test_units(self):
        """
        New: Orders: Create Approach: I can create suborder with test unit successfully,
        make sure the record created successfully in the analysis section.
        ( create with any type of test unit )
        LIMS-4255
        LIMS-4255
        :return:
        """

        # Go to the order page
        self.order_page.get_orders_page()
        order_row = self.order_page.get_random_order_row()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        orders_duplicate_data_before, orders = self.order_page.get_orders_duplicate_data(
            order_no=order_data['Order No.'])
        orders_records_before = self.order_page.get_table_records()

        self.base_selenium.LOGGER.info(
            ' + Select random order with {} no.'.format(order_data['Order No.']))
        self.order_page.get_random_x(orders[0])
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + Order url : {}'.format(order_url))
        # create order with random data
        self.order_page.create_new_suborder_with_test_units(material_type='Raw Material', article_name='a',
                                                            test_unit='')
        self.order_page.save(save_btn='order:save_btn')

        # filter one more time to make sure new record added to the active table
        self.order_page.get_orders_page()
        orders_duplicate_data_after, _ = self.order_page.get_orders_duplicate_data(
            order_no=order_data['Order No.'])
        orders_records_after = self.order_page.get_table_records()

        self.base_selenium.LOGGER.info(
            ' + Assert there is a new suborder with the same order no.')
        self.assertEqual(orders_records_after, orders_records_before + 1)

        # go to the analysis section to make sure new analysis record created successfully
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info('Filter by order no to make sure that the analysis was not deleted')

        analysis_records = self.analyses_page.search(value=order_no)
        analysis_count = len(analysis_records) - 1

        self.base_selenium.LOGGER.info(
            '+ Assert count of analysis is: {}, and it should be {}'.format(analysis_count, 2))
        self.assertEqual(2, analysis_count)

        # making sure that the new test unit is added to the order's analysis no with the same analysis no not new number
        selected_analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(row=analysis_records[0])
        analysis_no_from_analysis_table_after_update = selected_analysis_data['Analysis No.']
        self.base_selenium.LOGGER.info('Making sure that when test plan is deleted, analysis number did not change')
        self.base_selenium.LOGGER.info(
            '+ Assert analysis no before update is: {}, and analysis number after update is: {}'.format(
                analysis_no_from_analysis_table_after_update, analysis_no))
        self.assertEqual(analysis_no_from_analysis_table_after_update, analysis_no)

        # making sure that the status remained open after adding new test unit
        self.base_selenium.LOGGER.info('Getting analysis status after removing test plan to make sure that it is Open')
        analysis_status_after_update = selected_analysis_data['Status']

        self.base_selenium.LOGGER.info(
            '+ Assert analysis status is {}, and it should be {}'.format(analysis_status_after_update, 'Open'))
        self.assertEqual(analysis_status_after_update, 'Open')

        # getting tezt plan value to make sure that it is equal to the one form order's
        analysis_test_plan_after_update = selected_analysis_data['Test Plans']
        self.base_selenium.LOGGER.info('Getting test plan from analysis to make sure test plans have been removed')
        self.base_selenium.LOGGER.info(
            '+ Assert test plan is: {}, and it should be {}'.format(analysis_test_plan_after_update,
                                                                    suborder_testplans[1]))
        self.assertEqual(analysis_test_plan_after_update, suborder_testplans[1])
      
    ### SYNTAX ERROR ###
    # will continue with us ( apply it from the second order & need diff test case number for it
    # @parameterized.expand(['save_btn', 'cancel'])
    # def test025_update_article(self, save):
    #     """
    #     New: Orders: Edit Approach: I can update the article successfully and press on ok button
    #     then press on cancel button, Nothing updated

    #     New: Orders: Edit Approach: I can update the article filed successfully with save button

    #     LIMS-3423
    #     implemented in another testcase
    #     :return:
    #     """

    #     """
    #     test case logic
    #     i'll filter with raw material material type just to make sure that it has multiple articles
    #     and then select and record
    #     and then update it's article and try to press save and press cancel
    #     """

    #     self.base_selenium.LOGGER.info('Filter with Raw Material material type, just to make sure that it has multiple articles')
    #     rows=self.order_page.search(value='Raw Material')

    #     order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
    #     self.base_selenium.LOGGER.info('Getting the selected order data to keep track of it')
    #     analysis_no=order_data['Analysis No.']
    #     article_name = order_data['Article Name']

    #     self.base_selenium.LOGGER.info('select the required order to update it')
    #     self.order_page.get_random_x(row=rows[0])

    #     order_article = self.order_page.get_article()
    #     self.order_page.set_article(
    #         article='')
    #     new_article = self.order_page.get_article()
    #     testplans=self.order_page.get_test_plan()
    #     if testplans:
    #         self.order_page.confirm_popup(force=True)
    #     self.order_page.set_test_plan(
    #         test_plan='')

    #     if 'save_btn' == save:
    #         self.order_page.save(save_btn='order:save_btn')
    #         self.base_selenium.LOGGER.info('Refresh to make sure that data are saved correctly')
    #         self.base_selenium.refresh()
    #         current_article = self.order_page.get_article()
    #     else:
    #         self.order_page.cancel(force=True)

    #     if 'save_btn' == save:
    #         self.base_selenium.LOGGER.info(
    #             ' + Assert {} (current_article) == {} (new_article)'.format(current_article,
    #                                                                         new_article))
    #         self.assertEqual(new_article, current_article)

    #     else:
    #         self.base_selenium.LOGGER.info('Filter by analysis no to get the same order that was selected')
    #         rows=self.order_page.search(value=analysis_no)
    #         self.order_page.get_random_x(row=rows[0])
    #         self.base_selenium.LOGGER.info('Select the order to make sure that the data didn\'t change' )
    #         current_article = self.order_page.get_article()
    #         self.base_selenium.LOGGER.info(
    #             ' + Assert {} (current_article) == {} (order_article)'.format(current_article,
    #                                                                         order_article))
    #         self.assertEqual(current_article, order_article)
    #         self.base_selenium.LOGGER.info('+ Assert contacts before and after pressing cancel, before: {}, after: {}'.format(old_contact, contacta_after_pressing_cancel))
    #         self.assertEqual(old_contact, contacta_after_pressing_cancel)

    #         self.base_selenium.LOGGER.info('+ Assert departments before and after pressing cancel, before: {}, after: {}'.format(old_departments, departmentsa_after_pressing_cancel))
    #         self.assertEqual(old_departments, departmentsa_after_pressing_cancel)

    #         self.base_selenium.LOGGER.info('+ Assert Analysis count is: {}, and should be: {}'.format(analysis_count, 2))
    #         self.assertEqual(2, analysis_count)

    #         child_table = self.analyses_page.get_child_table_data(index=0)
    #         analysis_testunits = []
    #         for record in child_table:
    #             analysis_testunits.append(record['Test Unit'])

    #         self.base_selenium.LOGGER.info('+ Assert analysis test units are: {}, and it should be: {}'.format(analysis_testunits, suborder_testunits_after_refresh))
    #         self.assertEqual(set(suborder_testunits_after_refresh) == set(analysis_testunits), True)

    #     else :
    #         self.base_selenium.LOGGER.info('Select the order to delete test unit form it')
    #         self.order_page.get_orders_page()
    #         rows = self.order_page.search(value=order_no)
    #         self.order_page.get_random_x(row=rows[1])

    #         self.order_page.get_suborder_table()
    #         sub_order_data = self.order_page.get_suborder_data(sub_order_index=1)
    #         suborder_testunits = sub_order_data['test_unit']
    #         suborder_testunits = suborder_testunits.split('|')
    #         self.order_page.remove_testunit_by_name(index=1, testunit_name=suborder_testunits[0])
    #         self.order_page.confirm_popup(force=True)

    #         self.base_selenium.LOGGER.info('Remove test unit with name: {}'.format(suborder_testunits[0]))
    #         sub_order_data = self.order_page.get_suborder_data(sub_order_index=1)
    #         suborder_testunits_before_refresh = sub_order_data['test_unit'].split('|')
    #         self.order_page.save(save_btn='order:save_btn')

    #         self.base_selenium.LOGGER.info('Refresh to make sure that data are saved correctly')
    #         self.base_selenium.refresh()

    #         self.base_selenium.LOGGER.info('Get suborder data to check it')
    #         sub_order_data = self.order_page.get_suborder_data(sub_order_index=1)
    #         suborder_testunits_after_refresh = sub_order_data['test_unit'].split('|')

    #         self.base_selenium.LOGGER.info('+ Assert Test units: test units are: {}, and should be: {}'.format(suborder_testunits_after_refresh, suborder_testunits_before_refresh))

    #         # getting the length of the table, should be 2
    #         self.base_selenium.LOGGER.info('Getting analysis page to check the data in this child table')
    #         self.analyses_page.get_analyses_page()

    #         self.base_selenium.LOGGER.info('Filter with order no to check analysis count')
    #         analysis_records=self.analyses_page.search(value=order_no)
    #         analysis_count = len(analysis_records) -1

    #         self.base_selenium.LOGGER.info('+ Assert Analysis count is: {}, and should be: {}'.format(analysis_count, 2))
    #         self.assertEqual(2, analysis_count)

    #         child_table = self.analyses_page.get_child_table_data(index=0)
    #         analysis_testunits = []
    #         for record in child_table:
    #             analysis_testunits.append(record['Test Unit'])

    #         self.base_selenium.LOGGER.info('+ Assert analysis test units are: {}, and it should be: {}'.format(analysis_testunits, suborder_testunits_after_refresh))
    #         self.assertEqual(set(suborder_testunits_after_refresh) == set(analysis_testunits), True)

    # def test_test(self):
    #     import ipdb; ipdb.set_trace()	        import ipdb; ipdb.set_trace()
    #     suborder_data = self.order_page.get_suborder_data(sub_order_index=3)	        suborder_data = self.order_page.get_suborder_data(sub_order_index=3)
    # discard no need form the form
    ### SYNTAX ERROR ###

    def test027_update_test_unit_with_add_more_in_form(self):
        """
        New: Orders: Form: Update test unit: update test unit by add more &
        this effect should display in the child table of the analysis section.
        LIMS-4268
        LIMS-4268
         :return:
         """
        # Go to test units section then search by qualitative test unit type
        test_units_list = []
        test_unit_dict = self.get_active_tst_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
        test_units_list.append(test_unit_dict['Test Unit Name'])

        # Then go to the order section to create new order with this test unit
        self.order_page.get_orders_page()
        created_order = self.order_page.create_new_order(material_type='s', article='r', contact='a',
                                                         test_units=test_units_list)

        # Go to the analysis section and search by the order number that created
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Make sure there is analysis for this order number.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        # Open the child table tp check the test unit display correct
        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
        testunit_name = row_with_headers['Test Unit']
        self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
        self.assertIn(testunit_name, test_units_list)

        # Go to the same order record and update test unit by add one more
        self.order_page.get_orders_page()
        orders_result = self.orders_page.result_table()
        self.order_page.get_random_x(row=orders_result[0])
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        self.order_page.set_test_unit()
        self.order_page.save(save_btn='order:save_btn')

        # Go to the analsyis section and search by the order number
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Make sure there is analysis for this order number.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        # Open the child table to make sure the update reflected successfully
        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
        testunit_name = row_with_headers['Test Unit']
        self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
        self.assertIn(testunit_name, testunit_name)

    # discarded no need for the form
    def test028_update_test_unit_with_delete_in_form(self):
        """
        New: Orders: Form: Update test unit: update test unit by replace it by another one ( remove it ) &
        this effect should display in the child table of the analysis section.
        ( use any type of test unit )
        LIMS-3062
        LIMS-3062
         :return:
         """
        # Go to test units section then search by qualitative test unit type
        test_units_list = []
        test_unit_dict = self.get_active_tst_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
        test_units_list.append(test_unit_dict['Test Unit Name'])

        # Then go to the order section to create new order with this test unit
        self.order_page.get_orders_page()
        created_order = self.order_page.create_new_order(material_type='s', article='r', contact='a',
                                                         test_units=test_units_list)

        # Go to the analysis section and search by the order number that created
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Make sure there is analysis for this order number.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        # Open the child table tp check the test unit display correct
        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
        testunit_name = row_with_headers['Test Unit']
        self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
        self.assertIn(testunit_name, test_units_list)

        # Go to the same order record and update test unit by deleting the old one and replace with new one
        self.order_page.get_orders_page()
        orders_result = self.orders_page.result_table()
        self.order_page.get_random_x(row=orders_result[0])
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        self.order_page.clear_test_unit()
        self.order_page.confirm_popup(force=True)
        self.order_page.set_test_unit()
        self.order_page.save(save_btn='order:save_btn')

        # Go to the analsyis section and search by the order number
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Make sure there is analysis for this order number.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        # Open the child table to make sure the update reflected successfully
        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
        testunit_name = row_with_headers['Test Unit']
        self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
        self.assertIn(testunit_name, testunit_name)

    @parameterized.expand(['save_btn', 'cancel_btn'])
    @skip('https://modeso.atlassian.net/browse/LIMS-6561')
    def test029_update_article_in_suborder(self, action):
        """
        Apply this on the suborder number 5 for example:
        Make sure once you delete the article, the test plan that corresponding to it will  deleted also to choose another one
        Make sure once you delete the article, the test unit will not delete
        updated it then press on save button, and make sure that the article updated successfully according to that
        LIMS-6524
        Apply this on the table view ( from the second suborder )
        In case I update the article then press on ok button ( In pop-up) & when you press on cancel button nothing updated
        LIMS-4297
        """

        self.info('open random order')
        self.order_page.get_random_order()
        order_data = self.order_page.get_suborder_data()
        random_index_to_edit = self.generate_random_number(lower=0, upper=len(order_data['suborders']) - 1) or 0
        self.info('index to edit {}'.format(random_index_to_edit))
        selected_suborder_data = order_data['suborders'][random_index_to_edit]

        self.base_selenium.LOGGER.info('get completed testplans with articles based on the suborder materialtype')
        materialtype_list = self.general_utilities_api.list_all_material_types()['materialTypes']
        materialtype_object = \
            list(filter(lambda x: x['name'] == selected_suborder_data['material_type'], materialtype_list))[0]

        testunit_with_materialtype_all = \
            self.test_unit_api.get_all_test_units(filter='{"materialTypes":"all"}').json()['testUnits'][0]
        testunit_form_data = self.test_unit_api.get_testunit_form_data(id=testunit_with_materialtype_all['id'])
        # create random article
        random_article_name = self.order_page.generate_random_text()
        random_article_number = self.order_page.generate_random_number()
        materialtype_object = {
            'id': materialtype_object['id'],
            'text': materialtype_object['name']
        }
        article_data = self.article_api.create_article(No=random_article_number, name=random_article_name,
                                                       materialType=materialtype_object)

        # create random testplan
        article = {
            'id': article_data['id'],
            'text': random_article_name
        }
        material_type = materialtype_object
        testunit = self.test_unit_page.map_testunit_to_testplan_format(testunit=testunit_form_data)
        testplan_name = self.test_unit_page.generate_random_text()
        testplan_number = self.test_unit_page.generate_random_number()
        testplan_object = {
            'text': testplan_name,
            'id': 'new'
        }
        self.base_selenium.LOGGER.info(
            self.test_plan_api.create_testplan(number=testplan_number, testPlan=testplan_object,
                                               materialType=material_type, selectedArticles=[article],
                                               testUnits=[testunit]))

        self.base_selenium.LOGGER.info(
            'update suborder with article {}, and testplan {}'.format(random_article_name, testplan_name))
        self.order_page.update_suborder(sub_order_index=random_index_to_edit, articles=random_article_name,
                                        test_plans=[testplan_name])

        self.order_page.save(save_btn='order:' + action)
        if action == 'save_btn':
            self.base_selenium.refresh()
            self.base_selenium.LOGGER.info('asserting suborder data after update')
            order_data_after_update = self.order_page.get_suborder_data()
            self.assertEqual(order_data_after_update['suborders'][random_index_to_edit]['article']['name'],
                             random_article_name)
            self.assertEqual(order_data_after_update['suborders'][random_index_to_edit]['testplans'][0], testplan_name)
        else:
            self.order_page.confirm_popup()
            self.order_page.open_edit_page(row=self.order_page.result_table()[0])
            suborder_data_after_cancel = self.order_page.get_suborder_data()
            self.assertEqual(suborder_data_after_cancel['suborders'][random_index_to_edit], selected_suborder_data)

    def test30_create_new_suborder_with_testunit(self):
        """
        New: Orders: Create Approach: I can create suborder with test unit successfully,
        make sure the record created successfully in the analysis section.
        LIMS-4255
        """
        article, article_data = self.article_api.create_article()
        testunit_record = random.choice \
            (self.test_unit_api.get_all_test_units(filter='{"materialTypes":"all"}').json()['testUnits'])

        order = random.choice(self.orders_api.get_all_orders(limit=50)['orders'])
        self.orders_page.get_order_edit_page_by_id(id=order['id'])

        self.info('getting analysis tab to check out the count of the analysis')
        self.order_page.navigate_to_analysis_tab()
        analysis_count_before_adding = self.single_analysis_page.get_analysis_count()

        self.info('get back to order tab')
        self.single_analysis_page.navigate_to_order_tab()
        order_data_before_adding_new_suborder = self.order_page.get_suborder_data()
        suborder_count_before_adding = len(order_data_before_adding_new_suborder['suborders'])
        self.info('count of analysis equals: ' + str(analysis_count_before_adding) +
                  "\t count of suborders equals: " + str(suborder_count_before_adding))

        self.info('create new suborder with materialType {}, and article {}, and testUnit {}'.format(
            article_data['materialType']['text'], article['name'], testunit_record['name']))

        self.order_page.create_new_suborder_with_test_units(
            material_type=article_data['materialType']['text'],
            article_name=article['name'], test_unit=testunit_record['name'])
        self.order_page.save(save_btn='order:save_btn', sleep=True)
        self.base_selenium.refresh()
        self.order_page.sleep_tiny()

        order_data_after_adding_new_suborder = self.order_page.get_suborder_data()
        self.assertEqual(suborder_count_before_adding + 1,
                         len(order_data_after_adding_new_suborder['suborders']))

        self.info('navigate to analysis page to make sure that only one analysis is added')
        self.order_page.navigate_to_analysis_tab()
        analysis_count = self.single_analysis_page.get_analysis_count()

        self.info('check analysis count\t' + str(analysis_count) + "\tequals\t" + str(analysis_count_before_adding + 1))
        self.assertGreaterEqual(analysis_count, analysis_count_before_adding + 1)

        analysis_record = self.single_analysis_page.open_accordion_for_analysis_index(analysis_count - 1)
        testunit_in_analysis = self.single_analysis_page.get_testunits_in_analysis(source=analysis_record)
        self.assertEqual(len(testunit_in_analysis), 1)
        testunit_name = testunit_in_analysis[0]['']
        self.assertIn(testunit_record['name'], testunit_name)

    @parameterized.expand(['save_btn', 'cancel_btn'])
    def test31_update_departments_in_second_suborder(self, action):
        """
         Orders: department Approach: In case I update the department then press on save button
         (the department updated successfully) & when I press on cancel button (this department
         not updated) (this will apply from the second order)
         LIMS-6523
        """
        self.info('create contact')
        response, payload = self.contacts_api.create_contact()
        contact, contact_id = payload, response['company']['companyId']

        self.info('open random order record')
        order = random.choice(self.orders_api.get_all_orders(limit=50)['orders'])
        order_id = order['id']
        self.orders_page.get_order_edit_page_by_id(id=order_id)
        order_data = self.order_page.get_suborder_data()
        if len(order_data['suborders']) <= 1:
            self.order_page.duplicate_from_table_view()
            self.order_page.save(save_btn='order:save_btn')

        self.order_page.set_contact(contact=contact['name'])
        self.order_page.sleep_small()
        self.order_page.save(save_btn='order:save_btn', sleep=True)
        self.base_selenium.refresh()

        selected_suborder_data = self.order_page.get_suborder_data()
        self.order_page.update_suborder(sub_order_index=1, departments=contact['departments'][0]['text'])
        self.order_page.save(save_btn='order:' + action)
        if action == 'save_btn':
            self.base_selenium.refresh()
            suborder_data_after_update = self.order_page.get_suborder_data()
            self.assertIn(contact['departments'][0]['text'], suborder_data_after_update['suborders'][1]['departments'])
        else:
            self.order_page.confirm_popup()
            self.orders_page.get_order_edit_page_by_id(id=order_id)
            suborder_data_after_cancel = self.order_page.get_suborder_data()
            self.assertEqual(suborder_data_after_cancel['suborders'][1], selected_suborder_data['suborders'][1])

    def test32_update_order_no_should_reflect_all_suborders_and_analysis(self):
        """
        In case I update the order number of record that has multiple suborders inside it
        all those suborders numbers updated according to that and (this will effect in the
        analysis records also that mean all order number of those records will updated
        according to that in the active table )
        LIMS-4270
        """
        self.info('generate new order number to use it for update')
        new_order_no = self.orders_api.get_auto_generated_order_no()
        year_value = self.order_page.get_current_year()[2:]
        formated_order_no = new_order_no + '-' + year_value
        self.info('newly generated order number = {}'.format(formated_order_no))
        order = self.orders_api.get_all_orders(limit=50)['orders'][1]
        self.orders_page.get_order_edit_page_by_id(id=order['id'])
        self.order_page.set_no(no=formated_order_no)
        self.order_page.sleep_small()
        self.order_page.save(save_btn='order:save_btn', sleep=True)

        self.info('refresh to make sure that data are saved correctly')
        self.base_selenium.refresh()
        order_no_after_update = self.order_page.get_no()

        self.info('order no is {}, and it should be {}'.format(order_no_after_update, formated_order_no))
        self.assertEqual(order_no_after_update.replace("'", ""), formated_order_no)

        self.info('navigate to analysis tab to make sure that order no updated correctly')
        self.order_page.navigate_to_analysis_tab()
        analysis_records = self.single_analysis_page.get_all_analysis_records()

        self.info('checking order no of each analysis')
        for record in analysis_records:
            self.assertEqual(record['Order No.'], formated_order_no)

    def test033_Duplicate_main_order_and_cahange_materiel_type(self):
        """
        duplicate the main order then change the materiel type
        LIMS-6219
        """
        self.info('get random order')
        orders, payload = self.orders_api.get_all_orders(limit=50)
        main_order = random.choice(orders['orders'])
        self.order_page.search(main_order['orderNo'])
        self.info('duplicate the main order')
        self.order_page.duplicate_main_order_from_order_option()
        self.order_page.wait_until_page_is_loaded()
        duplicated_order_number = self.order_page.get_order_number()
        self.info('order to be duplicated is {}, new order no is {}'.
                  format(main_order['orderNo'], duplicated_order_number))
        self.assertNotEqual(main_order['orderNo'], duplicated_order_number)
        
        self.info('get material type of first suborder')
        old_material_type = self.order_page.get_material_type_of_first_suborder()
        self.info('get completed test plan with different material type')
        self.test_plan_api = TestPlanAPI()
        completed_test_plans = self.test_plan_api.get_completed_testplans()
        for test_plan in completed_test_plans:
            if test_plan['materialType'] != old_material_type:
                selected_test_plan = test_plan
                break
        self.info('change material type of first suborder')
        self.order_page.set_material_type_of_first_suborder(material_type=selected_test_plan['materialType'])
        self.info('Make sure that article, test unit, and test plan are empty')
        self.assertEqual(self.base_selenium.get_value(element='order:article'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
        self.info('select random article, test unit and test plan')
        self.order_page.set_article(article=selected_test_plan['article'][0])
        test_unit = self.order_page.set_test_unit()
        self.order_page.set_test_plan(test_plan=selected_test_plan['testPlanName'])
        self.info('duplicated order material is {}, article {}, test_unit {} and test_plan {}'.
                  format(selected_test_plan['materialType'], selected_test_plan['article'][0],
                         test_unit, selected_test_plan['testPlanName']))
        self.order_page.save(save_btn='order:save_btn', sleep=True)
        self.info("navigate to orders' page to make sure that order duplicated correctly with selected data")
        self.order_page.get_orders_page()
        self.order_page.search(duplicated_order_number)
        child_data = self.order_page.get_child_table_data()
        if len(child_data) > 1:
            suborder_data = child_data[-1]
        else:
            suborder_data = child_data[0]
        
        self.info('Make sure that suborder data is correct')
        self.assertEqual(suborder_data['Material Type'], selected_test_plan['materialType'])
        self.assertEqual(suborder_data['Article Name'].replace("'", ""), selected_test_plan['article'][0])
        self.assertEqual(suborder_data['Test Units'], test_unit)
        self.assertEqual(suborder_data['Test Plans'], selected_test_plan['testPlanName'])

    def test034_duplicate_sub_order_table_with_add(self):
        """
        Orders: User can duplicate any suborder from the order form ( table with add )
        LIMS-3738
        :return:
        """
        # get random order
        self.info('select random record')
        orders, payload = self.orders_api.get_all_orders(limit=20)
        data_before_duplicate_main_order = random.choice(orders['orders'])

        self.orders_page.get_order_edit_page_by_id(id=data_before_duplicate_main_order['id'])
        data_before_duplicate = self.order_page.get_suborder_data()

        self.order_page.duplicate_from_table_view(index_to_duplicate_from=0)
        after_duplicate_order = self.order_page.get_suborder_data()

        # make sure that the new order has same order No
        self.assertEqual(data_before_duplicate['orderNo'].replace("'", ""), after_duplicate_order['orderNo'].replace("'", ""))
        # compare the contacts between two records
        self.assertCountEqual(data_before_duplicate['contacts'], after_duplicate_order['contacts'])
        # compare the data of suborders data in both orders
        self.assertNotEqual(data_before_duplicate['suborders'], after_duplicate_order['suborders'])

        # save the duplicated order
        self.order_page.save(save_btn='orders:save_order')
        # go back to the table view
        self.order_page.get_orders_page()
        # search for the created order no
        self.order_page.search(after_duplicate_order['orderNo'])
        suborder_data = self.order_page.get_child_table_data()[0]
        order_result = self.order_page.result_table()[0].text
        # check that it exists
        self.assertIn(after_duplicate_order['orderNo'].replace("'", ""), order_result.replace("'", ""))
        self.order_page.navigate_to_analysis_tab()
        self.order_page.search(suborder_data['Analysis No.'])
        analysis_result = self.order_page.result_table()[0].text
        self.assertIn(suborder_data['Analysis No.'].replace("'", ""), analysis_result.replace("'", ""))
             
    def test034_Duplicate_sub_order_and_cahange_materiel_type(self):
        """
        duplicate sub-order of any order then change the materiel type

        LIMS-6227
        """
        self.info('get random main order data')
        orders, payload = self.orders_api.get_all_orders(limit=50)
        main_order = random.choice(orders['orders'])
        self.order_page.search(main_order['orderNo'])
        self.order_page.get_child_table_data()
        self.info("duplicate the sub order of order {} from suborder's options".format(main_order['orderNo']))
        self.order_page.duplicate_sub_order_from_table_overview()

        old_material_type = self.order_page.get_material_type_of_first_suborder()
        self.info('old material type of suborder is {}'.format(old_material_type))
        self.info('get completed test plan with different material type')
        self.test_plan_api = TestPlanAPI()
        completed_test_plans = self.test_plan_api.get_completed_testplans()
        for test_plan in completed_test_plans:
            if test_plan['materialType'] != old_material_type:
                selected_test_plan = test_plan
                break
        self.info('change material type of first suborder to {}'.format(selected_test_plan['materialType']))
        self.order_page.set_material_type_of_first_suborder(material_type=selected_test_plan['materialType'])
        self.info('Make sure that article, test unit, and test plan are empty')
        self.assertEqual(self.base_selenium.get_value(element='order:article'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
        self.info('set suborder new data')
        self.order_page.set_article(article=selected_test_plan['article'][0])
        test_unit = self.order_page.set_test_unit()
        self.order_page.set_test_plan(test_plan=selected_test_plan['testPlanName'])
        self.info('duplicated sub order material is {}, article {}, test_unit {} and test_plan {}'.
                  format(selected_test_plan['materialType'], selected_test_plan['article'][0],
                         test_unit, selected_test_plan['testPlanName']))
        self.order_page.save(save_btn='order:save_btn', sleep=True)

        self.info("navigate to orders' active table and check that duplicated suborder found")
        self.order_page.get_orders_page()
        self.order_page.search(main_order['orderNo'])
        child_data = self.order_page.get_child_table_data()
        duplicated_suborder_data = child_data[0]
        self.assertEqual(duplicated_suborder_data['Material Type'], selected_test_plan['materialType'])
        self.assertEqual(duplicated_suborder_data['Article Name'], selected_test_plan['article'][0])
        self.assertEqual(duplicated_suborder_data['Test Units'], test_unit)
        self.assertEqual(duplicated_suborder_data['Test Plans'], selected_test_plan['testPlanName'])

    def test035_delete_suborder(self):
        """
         Delete sub order Approach: In case I have main order with multiple sub orders,
         make sure you can delete one of them

         LIMS-6853
        """
        self.info('get random order with multiple suborders')
        order = self.orders_api.get_order_with_multiple_sub_orders()
        self.order_page.search(order['orderNo'])

        self.info('archive first suborder')
        suborder_data = self.order_page.get_child_table_data()[0]
        self.order_page.archive_sub_order_from_active_table()
        self.orders_page.delete_sub_order(analysis_no=suborder_data['Analysis No.'])

        self.info('Navigate to order page to make sure that suborder is deleted and main order still active')
        self.order_page.get_orders_page()
        self.order_page.search(order['orderNo'])
        suborders_after_delete = self.order_page.get_child_table_data()
        self.assertNotIn(suborder_data['Analysis No.'], suborders_after_delete)
        self.assertGreater(len(suborder_data), 0)

        self.info('Navigate to Analysis page to make sure that analysis related to deleted suborder not found')
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
                                                 filter_text=suborder_data['Analysis No.'], field_type='text')
        self.assertEqual(len(self.order_page.result_table()), 1)

    def test036_Duplicate_sub_order_with_multiple_testplans_and_testunits_delet_approach(self):
        """
        Duplicate suborder Approach: Duplicate any sub order then delete the units & test plans

        LIMS-6852
        """
        self.info('create order data multiple testplans and test units')
        response, payload = self.orders_api.create_order_with_double_test_plans()
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        suborder_data_before_duplicate = self.orders_page.get_child_table_data()
        test_plans = [suborder_data_before_duplicate[0]['Test Plans'].split(',\n')[0],
                      suborder_data_before_duplicate[0]['Test Plans'].split(',\n')[1]]
        test_units = [suborder_data_before_duplicate[0]['Test Units'].split(',\n')[0],
                      suborder_data_before_duplicate[0]['Test Units'].split(',\n')[1]]
        self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
        self.orders_page.duplicate_sub_order_from_table_overview()
        self.base_selenium.clear_items_in_drop_down(element='order:test_plan', one_item_only=True)
        self.base_selenium.clear_items_in_drop_down(element='order:test_unit', one_item_only=True)
        self.order_page.save(save_btn='order:save')
        self.order_page.wait_until_page_is_loaded()
        self.info("navigate to orders' active table and check that duplicated suborder found")
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        child_data = self.order_page.get_child_table_data()
        duplicated_suborder_data = child_data[0]
        self.assertEqual(len(child_data), 2)
        self.assertEqual(duplicated_suborder_data['Article Name'], suborder_data_before_duplicate[0]['Article Name'])
        self.assertEqual(duplicated_suborder_data['Material Type'], suborder_data_before_duplicate[0]['Material Type'])
        self.assertIn(duplicated_suborder_data['Test Units'], test_units)
        self.assertIn(duplicated_suborder_data['Test Plans'], test_plans)

