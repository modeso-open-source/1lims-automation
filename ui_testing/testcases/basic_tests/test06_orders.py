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
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from ui_testing.pages.contacts_page import Contacts
from random import randint
import random
import time


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.article_api = ArticleAPI()
        self.test_unit_api = TestUnitAPI()
        self.contacts_api = ContactsAPI()
        self.single_analysis_page = SingleAnalysisPage()
        self.test_plan_api = TestPlanAPI()
        self.contacts_api = ContactsAPI()
        self.general_utilities_api = GeneralUtilitiesAPI()
        self.contacts_page = Contacts()
        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.order_page.get_orders_page()

    @parameterized.expand(['save_btn', 'cancel'])
    def test001_edit_order_number_with_save_cancel_btn(self, save):
        """
        New: Orders: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be
        LIMS-7200
        :return:
        """
        orders, payload = self.orders_api.get_all_orders(limit=40)
        random_order = random.choice(orders['orders'])

        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        old_number = self.order_page.get_no()
        new_number = self.generate_random_string()
        self.order_page.set_no(new_number)
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(
            url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        current_number = self.order_page.get_no()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_number) == {} (new_number)'.format(current_number, new_number))
            self.assertNotEqual(current_number, new_number)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_number) == {} (old_number)'.format(current_number, old_number))
            self.assertEqual(current_number, old_number)

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
        order_row = self.orders_page.search(random_order['orderNo'])[0]

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
        re, payload = self.orders_api.create_new_order()
        order_no = payload[0]['orderNo']
        self.order_page.apply_filter_scenario(filter_element='orders:filter_order_no', filter_text=order_no,
                                              field_type='text')

        row = self.order_page.get_last_order_row()
        self.order_page.click_check_box(source=row)
        self.order_page.duplicate_main_order_from_table_overview()

        # get the new order data
        after_duplicate_order = self.order_page.get_suborder_data()

        # make sure that its the duplication page
        self.assertTrue('duplicateMainOrder' in self.base_selenium.get_url())
        # make sure that the new order has different order No
        self.assertNotEqual(payload[0]['orderNo'], after_duplicate_order['orderNo'])
        # compare the contacts
        self.assertCountEqual([payload[0]['contact'][0]['text']], after_duplicate_order['contacts'])

        # save the duplicated order
        self.order_page.save(save_btn='orders:save_order')
        # go back to the table view
        self.order_page.get_orders_page()
        # search for the created order no
        self.order_page.search(after_duplicate_order['orderNo'])
        results = self.order_page.result_table()[0].text
        # check that it exists
        self.assertIn(after_duplicate_order['orderNo'].replace("'", ""), results.replace("'", ""))

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

    def test010_user_can_add_suborder(self):
        """
        New: Orders: Table view: Suborder Approach: User can add suborder from the main order
        LIMS-3817
        """
        self.info("get active suborder data to use")
        completed_test_plans = TestPlanAPI().get_completed_testplans(limit=50)
        test_plan = random.choice(completed_test_plans)
        self.info("get random order")
        orders, api = self.orders_api.get_all_orders(limit=50)
        order = random.choice(orders['orders'])
        self.orders_page.get_order_edit_page_by_id(order['id'])
        suborder_data = self.order_page.create_new_suborder(material_type=test_plan['materialType'],
                                                            article_name=test_plan['article'][0],
                                                            test_plan=test_plan['testPlanName'],
                                                            test_unit='',
                                                            add_new_suborder_btn='order:add_another_suborder')

        self.assertEqual(suborder_data['orderNo'].replace("'", "").split("-")[0],
                         order['orderNo'].split("-")[0])

        self.order_page.save(save_btn='order:save_btn')

        self.order_page.get_orders_page()
        suborders_data_after, _ = self.order_page.get_orders_and_suborders_data(order_no=order['orderNo'])
        suborder_data = suborders_data_after[0]
        self.assertEqual(suborder_data['Test Plans'], test_plan['testPlanName'])
        self.assertEqual(suborder_data['Material Type'], test_plan['materialType'])
        if test_plan['article'][0] != 'all':
            self.assertEqual(suborder_data['Article Name'], test_plan['article'][0])

        self.order_page.navigate_to_analysis_active_table()
        self.info('Assert There is an analysis for this new suborder')
        orders_analyses = self.analyses_page.search(order['orderNo'])
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=orders_analyses[0])
        self.assertEqual(suborders_data_after[0]['Analysis No.'], latest_order_data['Analysis No.'])

    # will change that the duplicate many copies will be from the the child table not from the active tabl
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

    @parameterized.expand(['materialType', 'article', 'testPlans',
                           'testUnit', 'lastModifiedUser', 'analysis'])
    def test015_filter_by_any_fields(self, key):
        """
        New: Orders: Filter Approach: I can filter by any field in the table view
        LIMS-3495
        """
        self.info('select random order using api')
        order, suborder = self.orders_api.get_order_with_testunit_testplans()
        order_data = suborder[0]
        filter_element = self.order_page.order_filters_element(key=key)
        if key == 'testPlans':
            filter_value = order_data[key][0]
        elif key == 'testUnit':
            filter_value = order_data[key][0]['testUnit']['name']
        else:
            filter_value = order_data[key]

        self.info('filter by {} with value {}'.format(key, filter_value))

        self.orders_page.apply_filter_scenario(
            filter_element=filter_element['element'],
            filter_text=filter_value,
            field_type=filter_element['type'])

        suborders = self.orders_page.get_child_table_data()
        filter_key_found = False
        for suborder in suborders:
            if filter_value in suborder[filter_element['result_key']].split(",\n"):
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)
        self.assertGreater(len(self.order_page.result_table()), 1)

    def test016_filter_by_order_No(self):
        """
        I can filter by any order No.
        LIMS-3495
        """
        self.info('select random order using api')
        orders, _ = self.orders_api.get_all_orders()
        order = random.choice(orders['orders'])
        self.info('filter by order No. {}'.format(order['orderNo']))
        self.orders_page.filter_by_order_no(order['orderNo'])
        result_order = self.orders_page.result_table()[0]
        self.assertIn(order['orderNo'], result_order.text.replace("'", ""))

    def test017_filter_by_Status(self):
        """
            I can filter by status
            LIMS-3495
        """
        self.info("filter by status: Open")
        self.orders_page.apply_filter_scenario(filter_element='orders:status_filter',
                                               filter_text='Open', field_type='drop_down')

        self.info('get random suborder from result table to check that filter works')
        suborders = self.orders_page.get_child_table_data(index=randint(0, 10))
        filter_key_found = False
        for suborder in suborders:
            if suborder['Status'] == 'Open':
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)
        self.assertGreater(len(self.order_page.result_table()), 1)

    def test018_filter_by_analysis_result(self):
        """
            I can filter by Analysis result
            LIMS-3495
        """
        self.info("filter by analysis_result: Conform")
        self.orders_page.apply_filter_scenario(filter_element='orders:analysis_result_filter',
                                               filter_text='Conform', field_type='drop_down')

        self.info('get random suborder from result table to check that filter works')
        suborders = self.orders_page.get_child_table_data(index=randint(0, 10))
        filter_key_found = False
        for suborder in suborders:
            if suborder['Analysis Results'].split(' (')[0] == 'Conform':
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)
        self.assertGreater(len(self.order_page.result_table()), 1)

    def test019_filter_by_contact(self):
        """
            New: Orders: Filter Approach: I can filter by contact
            LIMS-3495
        """
        self.info('get contact of random order')
        contact = self.orders_api.get_random_contact_in_order()
        self.info('filter by contact {}'.format(contact))
        self.orders_page.apply_filter_scenario(filter_element='orders:contact_filter',
                                               filter_text=contact, field_type='drop_down')
        order = self.orders_page.result_table()[0]
        self.assertIn(contact, order.text)

    def test020_filter_by_department(self):
        """
            I can filter by department
            LIMS-3495
        """
        self.info('get create order with department')
        api, payload = self.orders_api.create_order_with_department()
        self.assertEqual(api['status'], 1)
        department = payload[0]['departments'][0]['text']
        self.info('filter by department value {}'.format(department))
        self.orders_page.apply_filter_scenario(filter_element='orders:departments_filter',
                                               filter_text=department, field_type='text')

        suborders = self.orders_page.get_child_table_data()
        filter_key_found = False
        for suborder in suborders:
            if suborder['Departments'] == department:
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)
        self.assertGreater(len(self.order_page.result_table()), 1)

    @parameterized.expand(['testDate', 'shipmentDate', 'createdAt'])
    def test021_filter_by_date(self, key):
        """
         I can filter by testDate, shipmentDate, or createdAt fields
         LIMS-3495
        """
        orders, _ = self.orders_api.get_all_orders(limit=20)
        order = random.choice(orders['orders'])
        suborder, _ = self.orders_api.get_suborder_by_order_id(id=order['id'])
        date_list = suborder['orders'][0][key].split('T')[0].split('-')
        date_list.reverse()
        filter_value = "{}.{}.{}".format(date_list[0], date_list[1], date_list[2])
        filter_element = self.order_page.order_filters_element(key=key)
        self.orders_page.filter_by_date(first_filter_element=filter_element['element'][0],
                                        first_filter_text=filter_value,
                                        second_filter_element=filter_element['element'][1],
                                        second_filter_text=filter_value)

        suborders = self.orders_page.get_child_table_data()
        filter_key_found = False
        for suborder in suborders:
            if suborder[filter_element['result_key']] == filter_value:
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)
        self.assertGreater(len(self.order_page.result_table()), 1)

    def test016_validate_order_test_unit_test_plan(self):
        """
        New: orders Test plan /test unit validation
        LIMS-4349
        """
        self.base_selenium.LOGGER.info(
            ' Running test case to make sure from the validation of the test plan & test unit ')

        self.order_page.create_new_order(material_type='r', article='', contact='a', test_plans=[],
                                         test_units=[], multiple_suborders=0)
        self.base_selenium.LOGGER.info(
            'waiting to validation message appear when I didnt enter test plan & test unit')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.info(
            'Assert the error message to make sure that validation of the test plan & test units fields ? {}'.format(
                validation_result))
        self.assertTrue(validation_result)

    def test017_validate_order_test_unit_test_plan_edit_mode(self):
        """
        New: orders Test plan /test unit validation in edit mode
        LIMS-4826
        """
        self.base_selenium.LOGGER.info(
            ' Running test case to check that at least test unit or test plan is mandatory in order')
        # Get random order
        orders, payload = self.orders_api.get_all_orders(limit=20)
        selected_order_record = random.choice(orders['orders'])
        # Open random order edit page
        self.orders_page.get_order_edit_page_by_id(id=selected_order_record['id'])
        # edit suborder
        self.base_selenium.LOGGER.info(' Remove all selected test plans and test units')
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[0]
        suborder_row.click()
        self.order_page.sleep_small()

        # delete test plan and test unit
        if self.order_page.get_test_plan():
            self.order_page.clear_test_plan()
            self.order_page.confirm_popup(force=True)

        if self.order_page.get_test_unit():
            self.order_page.clear_test_unit()
            self.order_page.confirm_popup(force=True)

        self.order_page.save(save_btn='order:save_btn')
        # the red border will display on the test unit only because one of them should be mandatory
        test_unit_class_name = self.base_selenium.get_attribute(element="order:test_unit", attribute='class')
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

    def test018_validate_order_no_exists(self):
        """
        New: Orders: Create new order and change the autogenerated number
        LIMS-3406
        """
        orders, payload = self.orders_api.get_all_orders(limit=40)
        random_order = random.choice(orders['orders'])

        self.orders_page.get_order_edit_page_by_id(random_order['id'])

        self.order_page.set_order_number(no=random_order['orderNo'].replace("'", ""))
        self.base_selenium.LOGGER.info(
            'waiting fo validation message appear when I enter number already exists')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            'Assert the error message to make sure that validation when I enter number already exists? {}'.format(
                validation_result))
        self.assertTrue(validation_result)

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

    def test020_create_new_order_with_test_units(self):
        """
        New: Orders: Create a new order with test units
        LIMS-3267
        """
        testunits, payload = self.test_unit_api.get_all_test_units(limited=20)
        testunit = random.choice(testunits['testUnits'])

        self.order_page.get_orders_page()
        created_order = self.order_page.create_new_order(material_type='r', article='a', contact='a', test_plans=[],
                                                         test_units=[testunit['name']])

        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.base_selenium.LOGGER.info(
            'Assert There is an analysis for this new order.')
        orders_analyess = self.analyses_page.search(value=created_order['orderNo'])
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            created_order['orderNo'].replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:
            row_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(row=row,
                                                                                       table_element='general:table_child')
            testunit_name = row_with_headers['Test Unit']
            self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
            self.assertIn(testunit_name, testunit['name'])

    def test021_create_existing_order_with_test_units(self):
        """
        New: Orders: Create an existing order with test units
        LIMS-3268
        """
        random_testunit, payload = self.test_unit_api.get_all_test_units(filter='{"materialTypes":"all"}')
        random_name = random.choice(random_testunit['testUnits'])

        self.order_page.get_orders_page()
        created_order = self.order_page.create_existing_order(no='', material_type='s', article='a', contact='',
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
        orders, payload = self.orders_api.get_all_orders(limit=20)
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

    def test027_update_material_type(self):
        """
        Apply this on suborder number 5 for example:-
        -When user update the materiel type from table view once I delete it message will appear
        (All analysis created with this order and test plan will be deleted )
        -Once you press on OK button, the material type & article & test pan will delete
        -You can update it by choose another one and choose corresponding article & test plan
        LIMS-4264
        """
        self.info('get random order')
        orders, _ = self.orders_api.get_all_orders(limit=50)
        order = random.choice(orders['orders'])
        suborders, _ = self.orders_api.get_suborder_by_order_id(order['id'])
        suborder = suborders['orders'][0]
        suborder_update_index = len(suborders['orders']) - 1

        self.info('get random completed test plan with different material type')
        test_plans = TestPlanAPI().get_completed_testplans()
        # I need to make sure that material type not equal '47d56b4399' due to this open bug
        # https://modeso.atlassian.net/browse/LIMS-7710
        test_plans_without_duplicate = [test_plan for test_plan in test_plans if
                                        test_plan['materialType'] not in
                                        [suborder['materialType'], '47d56b4399']]
        test_plan = random.choice(test_plans_without_duplicate)

        self.info('update material type of order {} with {}'.format(order['orderNo'], test_plan['materialType']))
        self.orders_page.get_order_edit_page_by_id(order['id'])
        self.order_page.update_suborder(sub_order_index=suborder_update_index, material_type=test_plan['materialType'])
        confirm_edit = self.base_selenium.check_element_is_exist(element="general:confirmation_pop_up")
        confirm_edit_message = self.base_selenium.get_text(element="general:confirmation_pop_up")
        self.assertTrue(confirm_edit)
        self.assertIn('All analysis created with this order and test plan will be deleted', confirm_edit_message)
        self.info('confirm pop_up')
        self.orders_page.confirm_popup()
        self.info('assert test plan and articles are empty')
        self.assertFalse(self.order_page.get_test_plan())
        self.assertEqual(self.order_page.get_article(), 'Search')  # empty article return 'Search'
        self.info("set article to {} and test plan to {}".format(test_plan['article'][0], test_plan['testPlanName']))
        if test_plan['article'][0] == 'all':
            article = self.order_page.set_article('')
        else:
            self.order_page.set_article(test_plan['article'][0])
            article = test_plan['article'][0]

        self.order_page.set_test_plan(test_plan['testPlanName'])
        self.info('save the changes then refresh')
        self.order_page.save(save_btn='order:save_btn')
        self.base_selenium.refresh()
        self.info('get order data after edit and refresh')
        order_data_after_refresh = self.order_page.get_suborder_data()
        suborder_after_refresh = order_data_after_refresh['suborders'][suborder_update_index]
        self.info('navigate to analysis page to make sure analysis corresponding to suborder updated')
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_analysis_number(suborder_after_refresh['analysis_no'])
        analyses = self.analyses_page.result_table()[0]
        self.assertIn(test_plan['materialType'], analyses.text)
        self.assertIn(article, analyses.text)
        self.assertIn(test_plan['testPlanName'], analyses.text)

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

    def test022_update_suborder_testunits(self):
        """
        -When I delete test unit to update it message will appear
        ( This Test Unit will be removed from the corresponding analysis )
        -Make sure the corresponding analysis records created according to this update in test unit.
        LIMS-4269 case 2
        """
        self.info(" get random order with one test unit")
        order, sub_order, sub_order_index = self.orders_api.get_order_with_field_name(field='testUnit', no_of_field=1)
        self.info("get new test unit with material_type {}".format(sub_order[sub_order_index]['materialType']))

        new_test_unit_name = TestUnitAPI().get_test_unit_name_with_value_with_material_type(
            material_type=sub_order[sub_order_index]['materialType'], avoid_duplicate=True,
            duplicated_test_unit=sub_order[sub_order_index]['testUnit'][0]['testUnit']['name'])['name']

        self.info("Edit sub-order {} in order no. {} with test_unit {}".format(
            len(sub_order) - 1 - sub_order_index, order['orderNo'], new_test_unit_name))
        self.info("open order edit page")
        self.orders_page.get_order_edit_page_by_id(order['orderId'])
        self.order_page.update_suborder(sub_order_index=int(len(sub_order) - 1 - sub_order_index),
                                        test_units=[new_test_unit_name], remove_old=True)
        # checking that when adding new test unit, the newly added test unit is added to the
        # order's analysis instead of creating new analysis
        self.order_page.save_and_wait(save_btn='order:save_btn')
        self.info('Get suborder data to check it')
        suborder_testunits_after_edit = self.orders_api.get_suborder_by_order_id(
            order['orderId'])[0]['orders'][sub_order_index]['testUnit']
        testunits_after_edit = [testunit['testUnit']['name'] for testunit in suborder_testunits_after_edit]
        self.assertEqual(len(testunits_after_edit), 1)
        self.info('Assert Test units: test units are: {}, and should be: {}'.
                  format(testunits_after_edit, new_test_unit_name))
        self.assertEqual(testunits_after_edit[0], new_test_unit_name)

        self.info('Getting analysis page to check the data in this child table')
        self.order_page.get_orders_page()
        self.orders_page.filter_by_analysis_number(sub_order[sub_order_index]['analysis'])
        sub_order_data = self.orders_page.get_child_table_data()[0]
        self.assertEqual(sub_order_data['Test Units'], new_test_unit_name)
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
                                                 filter_text=sub_order[sub_order_index]['analysis'],
                                                 field_type='text')
        analysis_records = self.analyses_page.get_child_table_data()
        test_units = [analysis_record['Test Unit'] for analysis_record in analysis_records]
        self.assertIn(new_test_unit_name, test_units)

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

    @skip("https://modeso.atlassian.net/browse/LIMSA-127")
    def test025_update_order_article(self):
        """
        New: Orders: Edit Approach: I can update the article successfully and press on ok button
        then press on cancel button, Nothing updated

        LIMS-4297 - save case

        New: Orders: Edit Approach: I can update the article filed successfully with save button

        LIMS-3423
        """
        self.info('get random order')
        orders, _ = self.orders_api.get_all_orders(limit=50)
        order = random.choice(orders['orders'])
        suborders, _ = self.orders_api.get_suborder_by_order_id(order['id'])
        suborder = suborders['orders'][0]
        suborder_update_index = len(suborders['orders']) - 1
        test_units = [test_unit['testUnit']['name'] for test_unit in suborder['testUnit']]

        self.info('get random completed test plan with different article')
        test_plans = TestPlanAPI().get_completed_testplans()
        test_plans_with_different_article = [test_plan for test_plan in test_plans if
                                        test_plan['materialType'] == suborder['materialType'] and
                                        suborder['article'] != test_plan['article'][0]]
        if test_plans_with_different_article:
            test_plan_data = random.choice(test_plans_with_different_article)
            test_plan = test_plan_data['testPlanName']
            article = test_plan_data['article'][0]
        else:
            article_data = ArticleAPI().get_article_with_material_type(suborder['materialType'])
            article = article_data['name']
            formatted_article = {'id': article_data['id'], 'text': article}
            new_test_plan = TestPlanAPI().create_completed_testplan(
                material_type=suborder['materialType'], formatted_article=formatted_article)
            test_plan = new_test_plan['testPlanEntity']['name']

        test_plans = [test_plan]
        self.info('update order {} with article {}'.format(order['orderNo'], article))
        self.orders_page.get_order_edit_page_by_id(order['id'])
        if article == 'all':
            self.order_page.update_suborder(sub_order_index=suborder_update_index, articles='')
            article = self.order_page.get_article()
        else:
            self.order_page.update_suborder(sub_order_index=suborder_update_index, articles=article)

        self.info('assert test plan is empty')
        self.assertFalse(self.order_page.get_test_plan())
        if test_units:
            self.assertCountEqual(self.order_page.get_test_unit(), test_units)
        else:
            self.assertFalse(self.order_page.get_test_unit())

        self.order_page.set_test_plan(test_plan)
        self.info('save the changes then refresh')
        self.order_page.save(save_btn='order:save_btn')
        self.order_page.get_orders_page()

        self.info('navigate to analysis page to make sure analysis corresponding to suborder updated')
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_analysis_number(suborder['analysis'])
        analyses = self.analyses_page.get_the_latest_row_data()
        analyses_test_plans = analyses['Test Plans'].replace("'", '').split(", ")
        self.info('assert that article and test plan changed but test unit still the same')
        self.assertEqual(article.replace(' ', ''), analyses['Article Name'].replace(' ', ''))
        self.assertCountEqual(test_plans, analyses_test_plans)
        child_data = self.analyses_page.get_child_table_data()
        result_test_units = [test_unit['Test Unit'] for test_unit in child_data]
        for testunit in test_units:
            self.assertIn(testunit, result_test_units)

    def test026_update_order_article_cancel_approach(self):
        """
        New: Orders: Edit Approach: I can update the article successfully and press on ok button
        then press on cancel button, Nothing updated

        LIMS-4297 - cancel case
        """
        self.info('get random order')
        orders, _ = self.orders_api.get_all_orders(limit=50)
        order = random.choice(orders['orders'])
        suborders, _ = self.orders_api.get_suborder_by_order_id(order['id'])
        suborder = suborders['orders'][0]
        suborder_update_index = len(suborders['orders']) - 1
        test_units = [test_unit['testUnit']['name'] for test_unit in suborder['testUnit']]

        self.info('update order {} with random article'.format(order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(order['orderId'])
        self.order_page.update_suborder(sub_order_index=suborder_update_index, articles='')
        self.info('assert test plan is empty')
        self.assertFalse(self.order_page.get_test_plan())
        if test_units:
            self.assertCountEqual(self.order_page.get_test_unit(), test_units)
        else:
            self.assertCountEqual(self.order_page.get_test_unit(), ['Search'])
        self.order_page.cancel()
        self.info('navigate to analysis page to make sure analysis corresponding to suborder updated')
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_analysis_number(suborder['analysis'])
        analyses = self.analyses_page.get_the_latest_row_data()
        analyses_test_plans = analyses['Test Plans'].replace("'", '').split(", ")
        self.info('assert that article, test plan and test unit still the same')
        self.assertEqual(suborder['article'].replace(' ', ''), analyses['Article Name'].replace(' ', ''))
        if suborder['testPlans']:
            self.assertCountEqual(suborder['testPlans'], analyses_test_plans)
        else:
            self.assertCountEqual(['-'], analyses_test_plans)
        child_data = self.analyses_page.get_child_table_data()
        result_test_units = [test_unit['Test Unit'] for test_unit in child_data]
        for testunit in test_units:
            self.assertIn(testunit, result_test_units)

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

    def test035_archived_test_unit_shoudnt_display_in_the_order_drop_down_list(self):
        """
        Orders: Archived Test unit: Archive Approach: Archived test units shouldn't appear in orders in the drop down list
        LIMS-3710
        :return:
        """
        re, payload = self.test_unit_api.create_qualitative_testunit()
        self.test_unit_api.archive_testunits(ids=[str(re['testUnit']['testUnitId'])])
        self.base_selenium.click(element='orders:new_order')
        self.order_page.set_new_order()
        self.order_page.sleep_small()
        self.order_page.set_material_type_of_first_suborder(material_type='r', sub_order_index=0)

        self.info('Asset test unit is not existing in the list')
        self.assertFalse(self.order_page.is_testunit_existing(
            test_unit=payload['name']))

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
        self.assertEqual(data_before_duplicate['orderNo'].replace("'", ""),
                         after_duplicate_order['orderNo'].replace("'", ""))
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

    def test036_archive_new_order_and_analysis(self):
        """
        New: Orders Form: Archive main order: Make sure when the user archive main order,
        the analysis corresponding to it will be archived also
        LIMS-6873
        """
        self.info("select random order to archive")
        orders, api = self.orders_api.get_all_orders(limit=20)
        order = random.choice(orders['orders'])
        suborder_data, api = self.orders_api.get_suborder_by_order_id(order['id'])
        suborders = suborder_data['orders']
        analysis_no_list = []
        for suborder in suborders:
            analysis_no_list.append(suborder['analysis'])

        self.info(" Archive order with number : {}".format(order['orderNo']))
        order_row = self.order_page.search(order['orderNo'])
        self.order_page.click_check_box(source=order_row[0])
        self.order_page.archive_selected_orders(check_pop_up=True)
        self.info("Navigate to archived orders' table and filter by analysis no")
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_analysis_number(analysis_no_list[0])
        self.assertTrue(self.orders_page.is_order_in_table(value=order['orderNo']))
        child_data = self.orders_page.get_child_table_data()
        result_analysis = []
        for suborder in child_data:
            result_analysis.append(suborder['Analysis No.'].replace("'", ""))
        self.assertCountEqual(result_analysis, analysis_no_list)

    def test037_Duplicate_sub_order_with_multiple_testplans_and_testunits_delet_approach(self):
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

    def test037_duplicate_main_order_change_contact(self):
        """
        Duplicate from the main order Approach: Duplicate then change the contact
        LIMS-6222
        """
        self.info('get random main order data')
        orders, payload = self.orders_api.get_all_orders(limit=50)
        self.assertEqual(orders['status'], 1)
        main_order = random.choice(orders['orders'])
        self.info("duplicate order No {}".format(main_order['orderNo']))
        self.order_page.search(main_order['orderNo'])
        self.order_page.duplicate_main_order_from_order_option()
        new_contact = self.order_page.set_contact(contact='', remove_old=True)
        duplicted_order_no = self.order_page.get_no()
        self.order_page.save(save_btn='order:save')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicted_order_no)
        order = self.orders_page.get_the_latest_row_data()
        self.assertEqual(new_contact[0], order['Contact Name'])

    def test036_duplicate_main_order_with_multiple_contacts(self):
        """
        Orders: Duplicate suborder: Multiple contacts Approach: : All contacts are correct in case
        I duplicate from the main order or from the suborder
        LIMS-5816
        """
        self.info('create order with multiple contacts')
        response, payload = self.orders_api.create_order_with_multiple_contacts()
        self.assertEqual(response['status'], 1)
        contacts = [contact['text'] for contact in payload[0]['contact']]
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])

        self.info("duplicate the order {} from order's options".format(payload[0]['orderNo']))
        self.orders_page.duplicate_main_order_from_order_option()
        duplicated_order_no = self.order_page.get_no()
        self.order_page.save(save_btn='order:save')
        self.info("navigate to orders' active table and check that duplicated suborder found")
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicated_order_no)
        duplicated_order_data = self.orders_page.get_the_latest_row_data()
        duplicated_contacts = duplicated_order_data['Contact Name'].split(',\n')
        self.assertCountEqual(duplicated_contacts, contacts)

    def test037_duplicate_sub_order_with_multiple_contacts(self):
        """
        Orders: Duplicate suborder: Multiple contacts Approach: : All contacts are correct in case
        I duplicate from the main order or from the suborder
        LIMS-5816
        """
        self.info('create order with multiple contacts')
        response, payload = self.orders_api.create_order_with_multiple_contacts()
        self.assertEqual(response['status'], 1, response)
        contacts = [contact['text'] for contact in payload[0]['contact']]
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])

        self.order_page.get_child_table_data()
        self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
        self.orders_page.duplicate_sub_order_from_table_overview(number_of_copies=4)
        self.base_selenium.refresh()
        self.orders_page.wait_until_page_is_loaded()
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])

        duplicated_order_data = self.orders_page.get_the_latest_row_data()
        duplicated_contacts = duplicated_order_data['Contact Name'].split(',\n')
        self.assertCountEqual(duplicated_contacts, contacts)

        duplicated_suborders = self.orders_page.get_child_table_data()
        self.assertEqual(len(duplicated_suborders), 5)
        analyses_numbers = [suborder['Analysis No.'] for suborder in duplicated_suborders]
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.open_filter_menu()
        for analysis in analyses_numbers:
            self.analyses_page.filter_by(
                filter_element='analysis_page:analysis_no_filter', filter_text=analysis, field_type='text')
            self.analyses_page.filter_apply()
            analysis_data = self.analyses_page.get_the_latest_row_data()
            duplicated_contacts_in_analyses = analysis_data['Contact Name'].split(', ')
            self.assertEqual(len(duplicated_contacts_in_analyses), 3)
            self.assertCountEqual(duplicated_contacts, contacts)

    def test036_delete_multiple_orders(self):
        """
        Orders: Make sure that you can't delete multiple orders records at the same time
        LIMS-6854
        """
        self.info("navigate to archived items' table")
        self.orders_page.get_archived_items()
        self.orders_page.select_random_multiple_table_rows()
        self.orders_page.delete_selected_item(confirm_pop_up=False)
        confirm_edit = self.base_selenium.check_element_is_exist(element="general:cant_delete_message")
        confirm_edit_message = self.base_selenium.get_text(element="general:confirmation_pop_up")
        self.assertTrue(confirm_edit)
        self.assertIn('You cannot do this action on more than one record', confirm_edit_message)

    def test037_update_sub_order_with_multiple_testplans_only_delete_approach(self):
        """
        Orders: Test plans: In case I have order record with multiple test plans and I updated them,
        this update should reflect on the same analysis record without creating new one.
        LIMS-4134 case 1
        """
        self.info('create order with two testplans only')
        response, payload = self.orders_api.create_order_with_double_test_plans(only_test_plans=True)
        self.assertEqual(response['status'], 1)
        test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
        self.info("created order has test plans {} and {} ".format(test_plans[0], test_plans[1]))
        test_units = [TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']),
                      TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number'])]
        self.info("Edit order {}".format(payload[0]['orderNo']))
        self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
        suborder_before_edit = self.order_page.get_suborder_data()
        self.info('Assert that selected order has one analysis record')
        self.assertEqual(len(suborder_before_edit['suborders']), 1)
        analysis_no = suborder_before_edit['suborders'][0]['analysis_no']
        self.order_page.open_suborder_edit(sub_order_index=0)
        self.info("remove only one test plan")
        self.base_selenium.clear_items_in_drop_down(element='order:test_plan', one_item_only=True)
        self.info("confirm pop_up")
        self.order_page.confirm_popup()
        self.order_page.save(save_btn='order:save_btn', sleep=True)
        self.info("navigate to analysis' active table and check that pld analysis edited without creating new analysis")
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_order_no(payload[0]['orderNo'])
        self.assertEqual(len(self.analyses_page.result_table()) - 1, 1)
        analysis_data = self.analyses_page.get_the_latest_row_data()
        found_test_plans = analysis_data['Test Plans'].split(', ')
        self.info("assert that only one test plan found and analysis no not changed")
        self.assertEqual(len(found_test_plans), 1)
        self.assertEqual(analysis_data['Analysis No.'], analysis_no)
        suborder_data = self.analyses_page.get_child_table_data()
        self.assertEqual(len(suborder_data), 1)
        for test_plan in test_plans:
            for test_unit in test_units:
                if found_test_plans == test_plan:
                    self.info("assert that test unit related to deleted test plan removed from analysis")
                    self.assertEqual(test_unit, suborder_data['Test Unit'])

    def test038_update_sub_order_with_multiple_testplans_only_add_approach(self):
        """
        Orders: Test plans: In case I have order record with multiple test plans and I updated them,
        this update should reflect on the same analysis record without creating new one.
        LIMS-4134
        """
        self.info('create order with two testplans only')
        response, payload = self.orders_api.create_order_with_double_test_plans(only_test_plans=True)
        self.assertEqual(response['status'], 1)
        test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
        self.info("created order has test plans {} and {} ".format(test_plans[0], test_plans[1]))
        test_units = [TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']),
                      TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number'])]

        article_no = ArticleAPI().get_article_form_data(id=payload[0]['article']['id'])[0]['article']['No']
        self.info("get new completed test plan with article {} No: {} and material_type {}".format(
            payload[0]['article']['text'], article_no, payload[0]['materialType']['text']))

        completed_test_plans = TestPlanAPI().get_completed_testplans_with_material_and_same_article(
            material_type=payload[0]['materialType']['text'], article=payload[0]['article']['text'],
            articleNo=article_no)
        completed_test_plans_without_old = [testplan for testplan in completed_test_plans
                                            if testplan['testPlanName'] not in test_plans]

        if completed_test_plans_without_old:
            test_plan_data = random.choice(completed_test_plans_without_old)
            test_plan = test_plan_data['testPlanName']
            test_unit_data = TestPlanAPI().get_testunits_in_testplan(id=test_plan_data['id'])
            test_unit = test_unit_data[0]['name']
        else:
            self.info("There is no completed test plan so create it ")
            formatted_article = {'id': payload[0]['article']['id'], 'text': payload[0]['article']['text']}
            new_test_plan = TestPlanAPI().create_completed_testplan(
                material_type=payload[0]['materialType']['text'], formatted_article=formatted_article)
            test_plan = new_test_plan['testPlanEntity']['name']
            test_unit = new_test_plan['specifications'][0]['name']
            self.info("completed test plan created with name {} and test unit {}".format(test_plan, test_unit))

        test_plans.append(test_plan)
        test_units.append(test_unit)

        self.info("edit the sub order of order {}".format(payload[0]['orderNo']))
        self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
        suborder_before_edit = self.order_page.get_suborder_data()
        self.info('Assert that selected order has one analysis record')
        self.assertEqual(len(suborder_before_edit['suborders']), 1)
        analysis_no = suborder_before_edit['suborders'][0]['analysis_no']
        self.order_page.update_suborder(test_plans=[test_plan])
        self.order_page.save(save_btn='order:save_btn')
        self.info("navigate to orders' active table and check that duplicated suborder found")
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_order_no(payload[0]['orderNo'])
        self.assertEqual(len(self.analyses_page.result_table()) - 1, 1)
        analysis_data = self.analyses_page.get_the_latest_row_data()
        found_test_plans = analysis_data['Test Plans'].split(', ')
        self.assertEqual(len(found_test_plans), 3)
        self.assertEqual(analysis_data['Analysis No.'], analysis_no)
        suborder_data = self.analyses_page.get_child_table_data()
        found_test_units = [testunit['Test Unit'] for testunit in suborder_data]
        self.assertEqual(len(found_test_units), 3)
        self.assertCountEqual(test_plans, found_test_plans)
        self.assertCountEqual(test_units, found_test_units)

    def test042_Duplicate_sub_order_with_multiple_testplans_and_testunits_add_approach(self):
        """
        Duplicate suborder Approach: Duplicate any sub order then add test unit & test plan

        LIMS-6232
        """
        self.info('create order data multiple testplans and test units')
        response, payload = self.orders_api.create_order_with_double_test_plans()
        self.assertEqual(response['status'], 1, payload)
        test_plans = [payload[0]['testPlans'][0]['testPlanName'], payload[0]['testPlans'][1]['testPlanName']]
        test_units = [payload[0]['testUnits'][0]['name'], payload[0]['testUnits'][1]['name']]
        self.info("get new completed test plan with article {} and material_type {}".format(
            payload[0]['article']['text'], payload[0]['materialType']['text']))

        test_plan, test_unit = TestPlanAPI().get_order_valid_testplan_and_test_unit(
            material_type=payload[0]['materialType']['text'],
            used_test_plan=test_plans,
            used_test_unit=test_units,
            article_id=payload[0]['article']['id'], article=payload[0]['article']['text'])

        test_plans.append(test_plan)
        test_units.append(test_unit)

        self.orders_page.search(payload[0]['orderNo'])
        self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
        self.orders_page.get_child_table_data()
        self.orders_page.duplicate_sub_order_from_table_overview()
        self.order_page.set_test_plan(test_plan)
        self.order_page.set_test_unit(test_unit)
        self.order_page.save(save_btn='order:save', sleep=True)
        analysis_no = self.order_page.get_suborder_data()['suborders'][1]['analysis_no']
        self.info("navigate to orders' active table and check that duplicated suborder found")
        self.order_page.get_orders_page()
        self.orders_page.filter_by_analysis_number(analysis_no)
        child_data = self.order_page.get_child_table_data()
        duplicated_suborder_data = child_data[0]
        self.assertEqual(len(child_data), 2)
        self.assertEqual(duplicated_suborder_data['Article Name'].replace(' ', ''),
                         payload[0]['article']['text'].replace(' ', ''))
        self.assertEqual(duplicated_suborder_data['Material Type'], payload[0]['materialType']['text'])
        duplicated_suborder_test_units = duplicated_suborder_data['Test Units'].split(',\n') or []
        duplicated_suborder_test_plans = duplicated_suborder_data['Test Plans'].split(',\n') or []
        self.assertCountEqual(duplicated_suborder_test_units, test_units)
        self.assertCountEqual(duplicated_suborder_test_plans, test_plans)

    def test040_user_can_edit_multiple_columns(self):
        """
        user can edit multiple columns at the same time
        LIMS-5221
        """
        self.info('get random order with multiple suborders edit page')
        order = self.orders_api.get_order_with_multiple_sub_orders()
        subororder_data = self.orders_api.get_order_by_id(order['orderId'])[0]
        self.assertEqual(subororder_data['status'], 1)
        self.info(' edit order no {}'.format(order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(order['orderId'])
        self.info('click on first row and update it')
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row[0].click()
        first_department = self.order_page.set_departments('')
        self.info('Department updated to {}'.format(first_department))
        first_Shipment_date = self.order_page.set_shipment_date(row_id=0)
        self.info('Shipment_date updated to {}'.format(first_Shipment_date))
        first_test_date = self.order_page.set_test_date(row_id=0)
        self.info('test_date updated to {}'.format(first_test_date))
        self.info('save changes')
        self.order_page.save(save_btn='order:save')
        self.info('edit second suborder row')
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row[1].click()
        self.order_page.set_departments('')
        self.order_page.set_shipment_date(row_id=1)
        self.order_page.set_test_date(row_id=1)
        self.info('press on cancel button')
        self.order_page.cancel()
        self.info('get suborders data to assert that second suborder not update updated ')
        result_suborder_data = self.orders_api.get_order_by_id(order['orderId'])[0]
        self.assertEqual(result_suborder_data['status'], 1)
        self.assertEqual(subororder_data['orders'][1]['shipmentDate'], result_suborder_data['orders'][1]['shipmentDate'])
        self.assertEqual(subororder_data['orders'][1]['testDate'], result_suborder_data['orders'][1]['testDate'])
        self.info('assert first suborder updated successfully')
        first_suborder = result_suborder_data['orders'][0]
        if first_department:
            first_suborder_department = [dep['name'] for dep in first_suborder['departments']]
            self.assertCountEqual(first_department, first_suborder_department)
        result_Shipment_date = first_suborder['shipmentDate'].split('T')[0].split('-')
        result_Shipment_date.reverse()
        Shipment_date = "{}.{}.{}".format(result_Shipment_date[0], result_Shipment_date[1], result_Shipment_date[2])
        self.assertEqual(first_Shipment_date, Shipment_date)
        result_test_date = first_suborder['testDate'].split('T')[0].split('-')
        result_test_date.reverse()
        test_date = "{}.{}.{}".format(result_test_date[0], result_test_date[1], result_test_date[2])
        self.assertEqual(first_test_date, test_date)

    #@skip('https://modeso.atlassian.net/browse/LIMS-7722')
    def test042_duplicate_main_order_with_testPlans_and_testUnits(self):
        """
        Duplicate main order Approach: duplicate order with test plan & test units
        LIMS-4353
        """
        self.info('create order with multiple test plans and test units')
        response, payload = self.orders_api.create_order_with_double_test_plans()
        self.assertEqual(response['status'], 1, payload)
        test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
        test_units = [testunit['name'] for testunit in payload[0]['selectedTestUnits']]
        test_units.extend(TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']))
        test_units.extend(TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number']))
        self.info("created order has test plans {} ".format(test_plans))
        self.info("created order has test units {} ".format(test_units))
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        self.info("duplicate order no {}".format(payload[0]['orderNo']))
        self.orders_page.duplicate_main_order_from_order_option()
        self.order_page.save(save_btn='order:save', sleep=True)
        duplicated_order_no = self.order_page.get_no()
        self.assertNotEqual(duplicated_order_no, payload[0]['orderNo'])
        self.info("navigate to analysis page  and make sure duplicated order created with same data")
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.assertTrue(self.orders_page.is_order_in_table(duplicated_order_no))
        self.analyses_page.search(duplicated_order_no)
        duplicated_test_plans = self.analyses_page.get_the_latest_row_data()['Test Plans'].split(', ')
        self.assertCountEqual(duplicated_test_plans, test_plans)
        duplicated_suborder_data = self.order_page.get_child_table_data()
        duplicated_test_units = [testunit['Test Unit'] for testunit in duplicated_suborder_data]
        self.assertCountEqual(test_units, duplicated_test_units)

    def test042_table_with_add_edit_single_row(self):
        """
        Orders: Table with add: In case I have two suborders and I update the first one
        then press on the second one the first one should updated according to that
        LIMS-5204
        """
        self.info("create new test unit edit the suborder by it ( because the test unit name is not a unique ")
        re, payload1 = self.test_unit_api.create_qualitative_testunit()

        order, payload = self.orders_api.create_new_order()
        self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])

        self.info(" Duplicate it to make sure we have two suborders to edit in one and press on the other to save data in the first one ")
        self.order_page.duplicate_from_table_view(index_to_duplicate_from=0)

        testunit_before_edit_row = self.order_page.get_suborder_data()['suborders'][0]['testunits']
        self.info("test unit before I update the first row {}".format(testunit_before_edit_row))

        # update the first suborder to update the test unit one it
        self.order_page.update_suborder(test_units=[payload1['name']], sub_order_index=0)
        # press on the second row because I want to save data in the first one
        self.order_page.update_suborder(sub_order_index=1)

        testunit_after_edit_row = self.order_page.get_sub_order_data_first_row()['suborders'][0]['testunits']
        self.info("test unit after I press on the second row to make sure it saved in the first one {}".format(testunit_after_edit_row))

        self.info('Assert that the test unit not equal ')
        self.assertNotEqual(testunit_before_edit_row, testunit_after_edit_row)











