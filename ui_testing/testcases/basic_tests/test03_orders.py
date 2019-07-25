import re
from unittest import skip
from parameterized import parameterized
from ui_testing.testcases.base_test import BaseTest
from random import randint
import time


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.order_page.get_orders_page()

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
    def test002_cancel_button_edit_contact(self, save):
        """
        Orders: In case I update the contact then press on cancel button, a pop up should display with ( ok & cancel )
        buttons and when I press on cancel button, this update shouldn't submit

        LIMS-4764
        LIMS-4764
        :return:
        """
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        self.order_page.sleep_tiny()
        current_contact = self.order_page.get_contact()
        self.order_page.set_contact()
        new_contact = self.order_page.get_contact()
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        order_contact = self.order_page.get_contact()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_contact) == {} (order_contact)'.format(new_contact, order_contact))
            self.assertEqual(new_contact, order_contact)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_contact) == {} (order_contact)'.format(current_contact, order_contact))
            self.assertEqual(current_contact, order_contact)

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
        self.base_selenium.LOGGER.info(' + Get Archived orders ')
        self.order_page.get_archived_items()
        self.base_selenium.LOGGER.info(' + Select Rows ')
        selected_orders_data, _ = self.order_page.select_random_multiple_table_rows()

        self.base_selenium.LOGGER.info(' + Restore Selected Rows ')
        self.order_page.restore_selected_items()
        self.base_selenium.LOGGER.info(' + Get Active orders')
        self.order_page.get_active_items()
        for selected_order_data in selected_orders_data:
            self.base_selenium.LOGGER.info(' + Order with analysis number =  {} restored successfully?'.format(
                selected_order_data['Analysis No.']))
            self.assertTrue(self.order_page.is_order_exist(
                value=selected_order_data['Analysis No.']))

    def test006_deleted_archived_order(self):
        """
        New: Order without/with article: Deleting of orders
        The user can hard delete any archived order
        LIMS-3257
        """
        self.order_page.get_archived_items()
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)

        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        analysis_numbers_list = order_data['Analysis No.'].split(',')

        self.base_selenium.LOGGER.info(
            ' + Delete order has number = {}'.format(order_data['Order No.']))
        self.order_page.delete_selected_item()
        self.assertFalse(self.order_page.confirm_popup())

        self.analyses_page.get_analyses_page()
        self.analyses_page.get_archived_items()
        self.base_selenium.LOGGER.info(
            ' + Is analysis number {} deleted successfully?'.format(analysis_numbers_list))
        has_active_analysis = self.analyses_page.search_if_analysis_exist(
            analysis_numbers_list)
        self.base_selenium.LOGGER.info(' + {} '.format(has_active_analysis))
        self.assertFalse(has_active_analysis)

    @parameterized.expand(['True', 'False'])
    def test007_order_search(self, small_letters):
        """
        New: Orders: Search Approach: User can search by any field & each field should display with yellow color

        LIMS-3492
        LIMS-3061
        :return:
        """
        row = self.order_page.get_last_order_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=row)
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

    @skip('https://modeso.atlassian.net/browse/LIMS-4766')
    def test008_duplicate_order_one_copy(self):
        """
        New: Orders with test units: Duplicate an order with test unit 1 copy

        LIMS-3270
        :return:
        """
        order_row_from_table_list = []
        order_row_from_form_list = []
        selected_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=selected_row)

        # add order number
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Order No.').replace("'", ''))
        # contact
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Contact Name').replace('...', ''))
        # material type
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Material Type').replace('...', ''))
        # article name
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Article Name').replace('...', ''))
        # article number
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Article No.').replace('...',
                                                                                                        '').replace(
                "'", ''))

        # #shipment date
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Shipment Date'))
        # #test Date
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Test Date'))
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Test Plans').replace('...', ''))
        order_row_from_table_list.append(
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Departments'))

        self.order_page.duplicate_order_from_table_overview(1)
        order_row_from_form_list.extend(
            [self.order_page.get_order_number().replace("'", ''), self.order_page.get_contact(),
             self.order_page.get_material_type()])
        order_row_from_form_list.append(
            self.order_page.get_article().split(' No')[0][0:30])
        order_row_from_form_list.append(self.order_page.get_article().split('No:')[
            1].replace("'", '')[0:30])
        order_row_from_form_list.append(self.order_page.get_shipment_date())
        order_row_from_form_list.append(self.order_page.get_test_date())
        order_row_from_form_list.append(self.order_page.get_test_plan())
        order_row_from_form_list.append(self.order_page.get_departments())
        self.base_selenium.LOGGER.info(
            ' + compare if data from table : {} is equal data in form {} '.format(order_row_from_table_list,
                                                                                  order_row_from_form_list))
        self.assertListEqual(order_row_from_form_list,
                             order_row_from_table_list)

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

        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            ' + Assert There is an analysis for this new suborder.')
        orders_analyess = self.analyses_page.search(order_data['Order No.'])
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
            orders_duplicate_data_after[0]['Analysis No.'], latest_order_data['Analysis No.'])

    def test011_analysis_number_filter_and_export(self):
        """
        New: Orders: Analysis number should appear in the table view column
        LIMS-2622
        :return:
        """
        self.base_selenium.LOGGER.info(' Select Random Order')
        order_row = self.order_page.get_random_order_row()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=order_row)
        analysis_number = order_data['Analysis No.'].split(',')[0]
        analysis_filter_field = self.order_page.order_filters_element(
            'Analysis No.')
        self.order_page.open_filter_menu()
        self.order_page.filter('Analysis No.', analysis_filter_field['element'], analysis_number,
                               analysis_filter_field['type'])
        last_rows = self.order_page.get_last_order_row()
        order_data_after_filter = self.base_selenium.get_row_cells_dict_related_to_header(
            row=last_rows)
        analysis_number_filter = order_data_after_filter['Analysis No.'].split(',')[
            0]
        self.base_selenium.LOGGER.info(
            ' * Compare search result if last row has  analysis number = {}  '.format(analysis_number))
        self.assertEqual(analysis_number_filter, analysis_number)
        self.order_page.click_check_box(source=last_rows)
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.order_page.download_xslx_sheet()
        sheet_values = self.order_page.sheet.iloc[0].values
        self.base_selenium.LOGGER.info(
            'Check if export of order has analyis number = {}  '.format(analysis_number))
        self.assertIn(analysis_number, sheet_values)

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
        order_no_created = self.order_page.create_new_order(material_type='r', article='a', contact='a', test_plans=['a'],
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

        # filtering by the new order no to get the count and making sure it is a match
        self.orders_page.get_orders_page()
        self.orders_page.search(new_order_no)
        self.base_selenium.LOGGER.info(
            ' + filter_by_new_order_no : {}'.format(new_order_no))
        new_orders_count = self.order_page.get_table_records()
        self.base_selenium.LOGGER.info(
            ' + count_of_the_updated_orders : {}'.format(new_orders_count))
        self.assertEqual(orders_count, new_orders_count,
                         ' new orders count should be equal orders count')

        # filtering by the old order no to make sure that the orders no has been replaced not added to the system
        self.orders_page.search(order_no_created)
        self.base_selenium.LOGGER.info(
            ' + filter_by_old_order_no_after_update : {}'.format(order_no_created))
        orders_before_update_count = self.order_page.get_table_records()
        self.base_selenium.LOGGER.info(
            ' + count_of_the_old_order_no_suborders : {}'.format(orders_before_update_count))
        self.assertEqual(orders_before_update_count, 0)

        # transfering to analysis page
        self.analyses_page.get_analyses_page()

        # filter in analysis using new order number, count should be equal to the records count in order
        self.analyses_page.search(new_order_no)
        self.base_selenium.LOGGER.info(
            ' + filter_by_order_no_after_update_in_analysis : {}'.format(new_order_no))
        records_in_analysis_after_update_count = self.analyses_page.get_table_records()

        # by filtering with the new random generated order number, if the count of the orders remained the same,
        # that's mean that all orders with the same number have been successfully updated.
        self.assertEqual(new_orders_count,
                         records_in_analysis_after_update_count)

    def test014_update_order_material_type(self, save):
        """
        New: Orders: Edit material type: Make sure that user able to change material type and related test plan &
        article.

        New: Orders: Materiel type Approach: In case then material type updated then press on cancel button,
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
        order_material_type = self.order_page.get_material_type()
        self.order_page.set_material_type(
            material_type=test_plan_dict['Material Type'])
        self.order_page.confirm_popup(force=True)
        self.order_page.set_article(
            article_name=test_plan_dict['Article Name'])
        self.order_page.set_test_plan(
            test_plan=test_plan_dict['Test Plan Name'])
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True, cancel_btn='order:cancel_btn')

        self.base_selenium.get(url=order_url, sleep=5)
        current_material_type = self.order_page.get_material_type()

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
    def test018_update_test_date(self, save):
        """
        New: Orders: Test Date: I can update test date successfully with cancel/save buttons
        LIMS-4780
        LIMS-4780
        :return:
        """
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        order_test_date = self.order_page.get_test_date()
        test_date = self.order_page.set_test_date()
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)
        current_test_date = self.order_page.get_test_date()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_test_date) == {} (new_test_date)'.format(current_test_date, test_date))
            self.assertEqual(test_date, current_test_date)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_test_date) == {} (order_test_date)'.format(current_test_date, order_test_date))
            self.assertEqual(current_test_date, order_test_date)

    @parameterized.expand(['save_btn', 'cancel'])
    def test017_update_shipment_date(self, save):
        """
        New: Orders: Shipment date Approach: I can update shipment date successfully with save/cancel button
        LIMS-4779
        LIMS-4779
        :return:
        """
        self.order_page.get_random_order()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        order_shipment_date = self.order_page.get_shipment_date()
        shipment_date = self.order_page.set_shipment_date()
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)
        current_shipment_date = self.order_page.get_shipment_date()

        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_shipment_date) == {} (new_shipment_date)'.format(current_shipment_date,
                                                                                        shipment_date))
            self.assertEqual(shipment_date, current_shipment_date)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_shipment_date) == {} (order_shipment-date)'.format(current_shipment_date,
                                                                                          order_shipment_date))
            self.assertEqual(current_shipment_date, order_shipment_date)

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
        self.base_selenium.LOGGER.info('Running test case to create a new order with test units')
        test_units_list = []
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Quantitative')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Quantitative Mibi')
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
            row_with_headers=self.base_selenium.get_row_cells_dict_related_to_header(row=row, table_element='general:table_child')
            testunit_name = row_with_headers['Test Unit']
            self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
            self.assertIn(testunit_name, test_units_list)
        
    
    def test021_create_existing_order_with_test_units(self):
        """
        New: Orders: Create an existing order with test units

        LIMS-3268
        """
        self.base_selenium.LOGGER.info('Running test case to create an existing order with test units')
        test_units_list = []
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Quantitative')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Quantitative Mibi')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        
        self.order_page.get_orders_page()    
        created_order = self.order_page.create_existing_order(no='' , material_type='r', article='a', contact='a',
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
            row_with_headers=self.base_selenium.get_row_cells_dict_related_to_header(row=row, table_element='general:table_child')
            testunit_name = row_with_headers['Test Unit']
            self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
            self.assertIn(testunit_name, test_units_list)
        
    
    def test022_create_existing_order_with_test_units_and_change_material_type(self):
        """
        New: Orders with test units: Create a new order from an existing order with test units but change the material type

        LIMS-3269
        """
        self.base_selenium.LOGGER.info('Running test case to create an existing order with test units and change material type')
        test_units_list = []
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        
        self.order_page.get_orders_page()    
        created_order = self.order_page.create_new_order(material_type='r', article='a', contact='a',
                                         test_units=test_units_list)
           
        created_existing_order = self.order_page.create_existing_order_with_auto_fill(no=created_order.replace("'", ""))
        self.order_page.sleep_tiny()
        self.order_page.set_material_type(material_type='Subassembely')
        self.order_page.sleep_medium()
        self.base_selenium.LOGGER.info('Check If article and test units are empty')
        article = self.order_page.get_article()
        self.assertEqual('Search', article)
        test_unit = self.order_page.get_test_unit()
        self.assertEqual('Search', article)
        self.order_page.set_article(article='a')
        self.order_page.set_test_unit(test_unit=test_unit_dict['Test Unit Name'])
        
        article = self.order_page.get_article()
        self.order_page.save(save_btn='order:save_btn')
        self.base_selenium.LOGGER.info(' + Order created with no : {} '.format(created_existing_order))
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Assert There is an analysis for this new order.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
           created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        self.assertEqual(
           article.split(' No:')[0], latest_order_data['Article Name'])
        self.assertEqual(
           'Subassembely', latest_order_data['Material Type'])

    def test023_create_existing_order_with_test_units_and_change_article(self):
        """
        New: Orders with test units: Create a new order from an existing order with test units but change the article

        LIMS-3269
        """
        self.base_selenium.LOGGER.info('Running test case to create an existing order with test units and change article')
        test_units_list = []
        test_unit_dict = self.get_active_test_unit_with_material_type(search='Qualitative', material_type='All')
        if test_unit_dict:
            self.base_selenium.LOGGER.info('Retrieved test unit ' + test_unit_dict['Test Unit Name'])
            test_units_list.append(test_unit_dict['Test Unit Name'])
        
        self.order_page.get_orders_page()    
        created_order = self.order_page.create_new_order(material_type='r', article='a', contact='a',
                                         test_units=test_units_list)
           
        created_existing_order = self.order_page.create_existing_order_with_auto_fill(no=created_order.replace("'", ""))
        self.order_page.sleep_tiny()
        self.order_page.set_article(article='r')
        self.order_page.sleep_medium()
        self.base_selenium.LOGGER.info('Check test units are still the same')
        test_unit = self.order_page.get_test_unit()
        self.assertEqual(test_unit[0].split(' No:')[0], test_unit_dict['Test Unit Name'])
        self.order_page.set_article(article='r')
        
        article = self.order_page.get_article()
        self.order_page.save(save_btn='order:save_btn')
        self.base_selenium.LOGGER.info(' + Order created with no : {} '.format(created_existing_order))
        self.analyses_page.get_analyses_page()
        self.base_selenium.LOGGER.info(
            'Assert There is an analysis for this new order.')
        orders_analyess = self.analyses_page.search(created_order)
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=orders_analyess[0])
        self.assertEqual(
           created_order.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        self.assertEqual(
           article.split(' No:')[0], latest_order_data['Article Name']) 
        
        self.analyses_page.open_child_table(source=orders_analyess[0])
        rows_with_childtable = self.analyses_page.result_table(element='general:table_child')
        for row in rows_with_childtable[:-1]:          
            row_with_headers=self.base_selenium.get_row_cells_dict_related_to_header(row=row, table_element='general:table_child')
            testunit_name = row_with_headers['Test Unit']
            self.base_selenium.LOGGER.info(" + Test unit : {}".format(testunit_name))
            self.assertIn(testunit_name, test_units_list)
     
        
    def test024_archive_sub_order(self):
        """
        New: Orders: Table:  Suborder /Archive Approach: : User can archive any suborder successfully 
        LIMS-3739
        """

        # create order with multiple suborders to keep track of which order to be archived
        self.base_selenium.LOGGER.info(' Create order with 3 suborders')
        order_no_created = self.order_page.create_new_order(multiple_suborders=2, material_type='Raw Material', test_units=[''])

        # filter by order no to get the orders data 
        self.base_selenium.LOGGER.info(' Filter by order No: {}'.format(order_no_created))
        self.orders_page.filter_by_order_no(filter_text=order_no_created)

        rows = self.orders_page.result_table()
        self.base_selenium.LOGGER.info('number of the filtered rows by this order no = {}'.format(len(rows)))

        # get the 3rd suborder data
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[1])
        analysis_no = order_data['Analysis No.'].split(',')

        self.base_selenium.LOGGER.info(' 3rd suborder analysis no is:: {}'.format(analysis_no))

        # open first suborder to keep the orders in the same sequence (first order in the list is the last created order)
        self.order_page.get_random_x(row=rows[0])
        self.base_selenium.LOGGER.info('Open first order in the filtered list of orders (first order in the list is the last created order)')

        # set suborder index to be archived
        suborder_index_to_archive = 2

        # getting order's table view to check archiving the 3rd suborder (subbopse to get a message that it can't be archived)
        self.order_page.archive_suborder(index=suborder_index_to_archive, check_pop_up=True)

        # get count of suborders after trying to delete order to make it is not deleted before archiving the analysis.
        rows_count = self.base_selenium.get_table_rows(element='order:suborder_table')

        self.base_selenium.LOGGER.info('+ Number of suborders = {}'.format(len(rows_count)))
        self.base_selenium.LOGGER.info('+ Assert  before clicking archive suborders count {}, after clicking archive suborders count {}'.format(3, len(rows_count)))
        self.assertEqual(len(rows_count), 3)

        # get the analysis page to filter the analysis corresponding to the required order
        self.analyses_page.get_analyses_page()

        # archive the required analysis
        self.base_selenium.LOGGER.info('archiving the analysis that belongs to the required order to be archived')
        self.analyses_page.search_by_number_and_archive(analysis_numbers_list=analysis_no)

        self.order_page.get_orders_page()

        # filtering by order no again to get the order that will have the archiving operation be performed on.
        self.orders_page.filter_by_order_no(filter_text=order_no_created)
        rows = self.orders_page.result_table()
        self.order_page.get_random_x(row=rows[0])

        # open table with add and archive the suborder with specific index
        self.base_selenium.LOGGER.info('Press archive on suborder no #{}'.format(suborder_index_to_archive+1))
        self.order_page.archive_suborder(index=suborder_index_to_archive, check_pop_up=False)
        rows_count = self.base_selenium.get_table_rows(element='order:suborder_table')

        self.base_selenium.LOGGER.info('+ Number of suborders = {}'.format(len(rows_count)))
        self.base_selenium.LOGGER.info('+ Assert  before clicking archive suborders count {}, after clicking archive suborders count {}'.format(3, len(rows_count)))
        self.assertEqual(len(rows_count), 3)

        # self.base_selenium.refresh()
        order_url = self.base_selenium.get_url()
        self.base_selenium.get(
            url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        self.order_page.archive_suborder(index=suborder_index_to_archive, check_pop_up=True)

        self.base_selenium.get(
            url=order_url, sleep=self.base_selenium.TIME_MEDIUM)
        self.order_page.get_suborder_table()
        rows_count = self.base_selenium.get_table_rows(element='order:suborder_table')

        self.base_selenium.LOGGER.info('+ Number of suborders = {}'.format(len(rows_count)))
        self.base_selenium.LOGGER.info('+ Assert  before archiving suborders count {}, after archiving suborders count {}'.format(3, len(rows_count)))
        self.assertEqual(len(rows_count), 2)

        self.order_page.get_orders_page()

        # going to archived orders page to make sure that the order is archived
        self.order_page.get_archived_items()

        self.order_page.open_filter_menu()
        self.orders_page.filter_by_analysis_number(filter_text=analysis_no)
        
        rows_count = self.order_page.result_table()
        self.base_selenium.LOGGER.info('+ Assert count archived orders with a specific analysis number: {}'.format(len(rows_count)))

        self.assertEqual(len(rows_count)-1,1)

    def test025_update_suborder_testplan(self):
        """
        New: Orders: Test plans/Merge Approach: 
        In case I have order record with multiple test plans and I updated them,
        this update should reflect on the same analysis record without creating new one.

        case: updating the 2nd suborder
        """


        # create order with 2 suborders to make sure that update in the suborder is working
        """
        reason for choosing specific test plan and specific material type is,
        i want also to test that when test plan is updated it is updated in the active table correctly
        and if the test plan name is long, it will appear as .... which won't indicate that test plan has been updated correctly or not
        """

        self.base_selenium.LOGGER.info('Creating new order with 2 suborders')
        order_no=self.order_page.create_new_order(multiple_suborders=1, test_plans=['tp1'], material_type='Raw Material')
        self.base_selenium.LOGGER.info('Created new order with no #{}, and test plan {}'.format(order_no, 'tp1'))
        
        # getting data of the created orders to make sure that everything created correctly
        rows = self.order_page.result_table()
        selected_order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
        analysis_no = selected_order_data['Analysis No.']

        self.order_page.get_random_x(row=rows[1])
        self.order_page.update_suborder(sub_order_index=1, test_plans=True, tp_value='tp2')
        self.base_selenium.LOGGER.info('Update order with test plans: {}'.format('tp2'))
        sub_order_data = self.order_page.get_suborder_data(sub_order_index=1, test_plan=True)
        suborder_testplans = sub_order_data['test_plan']
        suborder_testplans = suborder_testplans.split('|')
        self.base_selenium.LOGGER.info('order update and has test plans: {}'.format(suborder_testplans))

        # getting the length of the table, should be 2
        self.base_selenium.LOGGER.info('Get analysis page to filter with order no to make sure that new test plan did not trigger new analysis')
        self.analyses_page.get_analyses_page()
        self.analyses_page.open_filter_menu()
        self.analyses_page.filter_by(filter_element='orders:filter_order_no', filter_text=order_no.replace("'",''), field_type='drop_down')
        self.analyses_page.filter_apply()
        self.base_selenium.LOGGER.info('Filter analysis page with order no: #{}'.format(order_no))

        analysis_records=self.analyses_page.result_table()
        analysis_count = len(analysis_records) -1
        self.base_selenium.LOGGER.info('comparing count of analysis triggered with this order after adding new test plan')
        self.base_selenium.LOGGER.info('analysis triggered count: {}, and it should be 2'.format(analysis_count))
        self.assertEqual(2, analysis_count)

        # get analysis data to make sure that the newly added test plan is added to analysis
        self.base_selenium.LOGGER.info('Check the test plans in analysis from active table compared with selected test plans in order')
        selected_analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(row=analysis_records[0])
        analysis_test_plans = selected_analysis_data['Test Plans'].split(',')

        self.base_selenium.LOGGER.info('+ Comapring test plans in analysis and order')
        self.base_selenium.LOGGER.info('+ Assert order\'s testplans are: {}, analysis test plans are: {}'.format(suborder_testplans, analysis_test_plans))
        self.assertEqual(set(analysis_test_plans) == set(suborder_testplans), True)

        self.base_selenium.LOGGER.info('C omparing analysis status')
        # making sure that the status remained open after adding new test plan
        analysis_status = selected_analysis_data['Status']
        analysis_no_from_analysis_table = selected_analysis_data['Analysis No.']
        self.base_selenium.LOGGER.info('Analysis with no #{}, has status: {}'.format(analysis_no_from_analysis_table, analysis_status))
        self.base_selenium.LOGGER.info('+ Assert analysis has status: {}, and it should be: {}'.format(analysis_status, 'Open'))
        self.assertEqual(analysis_status, 'Open')

        # get order data to be updated
        self.base_selenium.LOGGER.info('Get order data to remove a test plan from the order')
        self.order_page.get_orders_page()
        rows = self.order_page.result_table()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
        order_testplans = order_data['Test Plans'].split(',')
        self.base_selenium.LOGGER.info('Get order with order no #{}, and analysis no #{}'.format(order_data['Order No.'], order_data['Analysis No.']))
        
        self.base_selenium.LOGGER.info('+ Comapring test plans in order active table')
        self.base_selenium.LOGGER.info('+ Assert order\'s testplans are: {}, added test plans are: {}'.format(suborder_testplans, order_testplans))
        self.assertEqual(set(order_testplans) == set(suborder_testplans), True)
        
        self.base_selenium.LOGGER.info('Openning order data to remove test plan and check its effect')
        self.order_page.get_random_x(row=rows[1])
        self.order_page.get_suborder_table()
        sub_order_data_before_refresh = self.order_page.get_suborder_data(sub_order_index=1, test_plan=True)
        suborder_testplans = sub_order_data_before_refresh['test_plan']
        suborder_testplans = suborder_testplans.split('|')

        # making sure that test plan is not removed by pressing cancel
        self.base_selenium.LOGGER.info('Remove Test Plan with name: {} from the order'.format(suborder_testplans[0]))
        self.order_page.remove_testplan_by_name(index=1, testplan_name=suborder_testplans[0])
        self.base_selenium.click(element='order:confirm_cancel')
        self.base_selenium.LOGGER.info('Pressing cancel to the pop up')
        self.order_page.sleep_tiny()
        self.order_page.save(save_btn="order:save_btn")
        
        self.base_selenium.LOGGER.info('Refresh to make sure that the test plan is not removed after pressing cancel')
        self.base_selenium.refresh()

        self.base_selenium.LOGGER.info('Getting suborders data to check the test plan is not removed')
        self.order_page.sleep_tiny()
        self.order_page.get_suborder_table()
        sub_order_data = self.order_page.get_suborder_data(sub_order_index=1, test_plan=True)
        suborder_testplans = sub_order_data['test_plan']
        suborder_testplans = suborder_testplans.split('|')

        # count of test plans should be 2
        count_of_testplans = len(suborder_testplans)
        self.base_selenium.LOGGER.info('+ Assert count of test plan is: {}, and it should be {}'.format(2, count_of_testplans) )
        self.assertEquals(2, count_of_testplans)

        self.base_selenium.LOGGER.info('Remove test plan from the order and press confirm to the pop up')
        self.order_page.remove_testplan_by_name(index=1, testplan_name=suborder_testplans[0])
        self.base_selenium.click(element='order:confirm_pop')
        self.order_page.sleep_tiny()
        self.order_page.save(save_btn="order:save_btn")
        
        self.base_selenium.LOGGER.info('Get orders page to make sure that test plan has been removed')
        self.order_page.get_orders_page()
        rows = self.order_page.result_table()
        selected_order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])

        testplan_after_update = selected_order_data['Test Plans']

        # making sure that test plans updated successfully and affected the table.
        self.base_selenium.LOGGER.info('+ Assert order test plans are: {}, and it should be: {}'.format(testplan_after_update, suborder_testplans[1]))
        self.assertEquals(suborder_testplans[1], testplan_after_update)

        # after update checking for analysis data
        # getting the length of the table, should be 2
        self.base_selenium.LOGGER.info('Get analysis page to make sure that removing test plan did not delete the triggered analysis')
        self.analyses_page.get_analyses_page()
        self.analyses_page.open_filter_menu()
        self.analyses_page.filter_by(filter_element='orders:filter_order_no', filter_text=order_no.replace("'",''), field_type='drop_down')
        self.analyses_page.filter_apply()
        self.base_selenium.LOGGER.info('Filter by order no to make sure that the analysis was not deleted')
        
        analysis_records=self.analyses_page.result_table()
        analysis_count = len(analysis_records) -1

        self.base_selenium.LOGGER.info('+ Assert count of analysis is: {}, and it should be {}'.format(analysis_count, 2))
        self.assertEqual(2, analysis_count)


        # making sure that the new test unit is added to the order's analysis no with the same analysis no not new number
        selected_analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(row=analysis_records[0])
        analysis_no_from_analysis_table_after_update = selected_analysis_data['Analysis No.']
        self.base_selenium.LOGGER.info('Making sure that when test plan is deleted, analysis number did not change')
        self.base_selenium.LOGGER.info('+ Assert analysis no before update is: {}, and analysis number after update is: {}'.format(analysis_no_from_analysis_table_after_update, analysis_no))
        self.assertEqual(analysis_no_from_analysis_table_after_update, analysis_no)

        
        # making sure that the status remained open after adding new test unit
        self.base_selenium.LOGGER.info('Getting analysis status after removing test plan to make sure that it is Open')
        analysis_status_after_update = selected_analysis_data['Status']

        self.base_selenium.LOGGER.info('+ Assert analysis status is {}, and it should be {}'.format(analysis_status_after_update, 'Open'))
        self.assertEqual(analysis_status_after_update, 'Open')

        # getting tezt plan value to make sure that it is equal to the one form order's
        analysis_test_plan_after_update = selected_analysis_data['Test Plans']
        self.base_selenium.LOGGER.info('Getting test plan from analysis to make sure test plans have been removed')
        self.base_selenium.LOGGER.info('+ Assert test plan is: {}, and it should be {}'.format(analysis_test_plan_after_update, suborder_testplans[1]))
        self.assertEqual(analysis_test_plan_after_update, suborder_testplans[1])

    def update_suborder_article(self):
        """
        In case you update the article then press on ok button ( In pop-up) test plans should be removed
        &
        when you press on cancel button nothing updated
        """

        testplan_list = self.get_multiple_active_article_with_tst_plan()
        self.base_selenium.LOGGER.info(testplan_list)



