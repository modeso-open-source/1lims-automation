from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.order_page import Order
from ui_testing.pages.analyses_page import Analyses
from parameterized import parameterized
import re
from unittest import skip

class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.article_page = Article()
        self.test_plan = TstPlan()
        self.order_page = Order()
        self.analyses_page = Analyses()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.order_page.get_orders_page()

    def test01_archive_order(self):
        """
            New: Orders: Archive
            The user cannot archive an order unless all corresponding analysis are archived
            LIMS-3425
        :return:
        """
        self.order_page.sleep_medium()
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        analysis_number_value = self.base_selenium.get_row_cell_text_related_to_header(
            order_row, 'Analysis No.')
        analysis_numbers_list = analysis_number_value.split(',')
        order_deleted = self.order_page.archive_selected_orders(
            check_pop_up=True)

        if order_deleted:
            self.analyses_page.get_analyses_page()
            self.order_page.sleep_medium()
            has_active_analysis = self.analyses_page.search_if_analysis_exist(
                analysis_numbers_list)
            self.assertEqual(has_active_analysis, False)

    def test02_archiveOrder_has_active_analysis(self):
        """
            New: Archive order has active analysis
            The user cannot archive an order unless all corresponding analysis are archived
            LIMS-4329
        :return:
        """
        self.order_page.sleep_medium()
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        analysis_number_value = self.base_selenium.get_row_cell_text_related_to_header(
            order_row, 'Analysis No.')
        analysis_numbers_list = analysis_number_value.split(',')
        self.base_selenium.LOGGER.info(
            ' + try to archive order with number : {}'.format(self.base_selenium.get_row_cell_text_related_to_header(
                order_row, 'Order No.')))
        order_deleted = self.order_page.archive_selected_orders(
            check_pop_up=True)

        if not order_deleted:
            self.analyses_page.get_analyses_page()
            self.order_page.sleep_medium()
            self.base_selenium.LOGGER.info(
                ' + Archive Analysis with numbers : {}'.format(analysis_numbers_list))
            self.analyses_page.search_by_number_and_archive(
                analysis_numbers_list)
            self.order_page.get_orders_page()
            self.order_page.sleep_medium()
            rows = self.order_page.search(analysis_numbers_list[0])
            self.order_page.click_check_box(source=rows[0])
            self.base_selenium.LOGGER.info(
                ' + archive order has analysis number =  {}'.format(analysis_numbers_list[0]))
            self.order_page.archive_selected_orders()
            rows = self.order_page.result_table()
            self.assertEqual(len(rows), 1)

    def test03_restore(self):
        """
        Restore Order
        I can restore any order successfully
        LIMS-4374
        """
        analysis_numbers = []
        self.order_page.sleep_medium()
        self.order_page.get_archived_items()
        self.order_page.sleep_medium()
        selected_orders, selected_rows = self.order_page.select_random_multiple_table_rows()
        for order in selected_rows:
            analysis_numbers.extend(self.base_selenium.get_row_cell_text_related_to_header(row=order,
                                                                                        column_value='Analysis No.').split(
                ','))
        self.order_page.restore_selected_items()
        self.order_page.get_active_items()
        for analysis_number in analysis_numbers:
            self.assertTrue(self.order_page.is_order_exist(
                value=analysis_number))

    def test04_deleted_archived_order(self):
        """
        New: Order without/with article: Deleting of orders
        The user can hard delete any archived order
        LIMS-3257
        """
        self.order_page.sleep_medium()
        self.order_page.get_archived_items()
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)
        analysis_numbers_list = self.base_selenium.get_row_cell_text_related_to_header(
            order_row, 'Analysis No.').split(',')
        self.base_selenium.LOGGER.info(
            ' + delete order has number = {}'.format(self.base_selenium.get_row_cell_text_related_to_header(
                order_row, 'Order No.')))
        self.order_page.delete_selected_item()
        self.assertFalse(self.order_page.confirm_popup())
        self.analyses_page.get_analyses_page()
        self.analyses_page.get_archived_items()
        self.base_selenium.LOGGER.info(
            ' + check that analysis numbers {} is deleted successfully'.format(analysis_numbers_list))
        has_active_analysis = self.analyses_page.search_if_analysis_exist(
            analysis_numbers_list)
        self.assertFalse(has_active_analysis, True)

    @skip('https://modeso.atlassian.net/browse/LIMS-4466')
    @parameterized.expand(['True', 'False'])
    def test05_order_search(self, small_letters):
        """
        New: Orders: Search Approach: User can search by any field & each field should display with yellow color

        LIMS-3492
        LIMS-3061
        :return:
        """
        self.order_page.sleep_medium()
        row = self.order_page.get_last_order_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=row)
        for column in row_data:
            search_by = row_data[column]
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
                if search_data[column].split(',')[0] == row_data[column].split(',')[0]:
                    break
            self.assertEqual(row_data[column].split(
                ',')[0], search_data[column].split(',')[0])

    @skip('https://modeso.atlassian.net/browse/LIMS-4766')
    def test06_duplicate_order_one_copy(self):
        """
        New: Orders with test units: Duplicate an order with test unit 1 copy

        LIMS-3270
        :return:
        """
        order_row_from_table_list = []
        order_row_from_form_list = []
        self.order_page.sleep_medium()
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
            self.base_selenium.get_row_cell_text_related_to_header(selected_row, 'Article No.').replace('...', '').replace(
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
        order_row_from_form_list.append(self.order_page.get_shimpment_date())
        order_row_from_form_list.append(self.order_page.get_test_date())
        order_row_from_form_list.append(
            self.order_page.get_test_plan(first_only=False))
        order_row_from_form_list.append(self.order_page.get_departments())

        self.assertListEqual(order_row_from_form_list,
                             order_row_from_table_list)
