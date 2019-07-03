
import re
from unittest import skip

from parameterized import parameterized

from ui_testing.pages.analyses_page import Analyses
from ui_testing.pages.article_page import Article
from ui_testing.pages.login_page import Login
from ui_testing.pages.order_page import Order
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.testcases.base_test import BaseTest


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.order_page = Order()
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.analyses_page = Analyses()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.order_page.get_orders_page()

    @parameterized.expand(['save', 'cancel'])
    @skip('https://modeso.atlassian.net/browse/LIMS-4768')
    def test001_cancel_button_edit_no(self, save):
        """
        New: Orders: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-5241
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        current_no = self.order_page.get_no()
        new_no = self.generate_random_string()
        self.order_page.set_no(new_no)
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        order_no = self.order_page.get_no()
        if 'save' == save:
            self.base_selenium.LOGGER.info(' + Assert {} (new_no) == {} (order_no)'.format(new_no, order_no))
            self.assertEqual(new_no, order_no)
        else:
            self.base_selenium.LOGGER.info(' + Assert {} (current_no) == {} (order_no)'.format(current_no, order_no))
            self.assertEqual(current_no, order_no)

    @parameterized.expand(['save', 'cancel'])
    def test002_cancel_button_edit_contact(self, save):
        """
        Orders: In case I update the contact then press on cancel button, a pop up should display with ( ok & cancel )
        buttons and when I press on cancel button, this update shouldn't submit

        LIMS-4764
        LIMS-4764
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        self.order_page.sleep_tiny()
        current_contact = self.order_page.get_contact()
        self.order_page.set_contact()
        new_contact = self.order_page.get_contact()
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        order_contact = self.order_page.get_contact()
        if 'save' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_contact) == {} (order_contact)'.format(new_contact, order_contact))
            self.assertEqual(new_contact, order_contact)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_contact) == {} (order_contact)'.format(current_contact, order_contact))
            self.assertEqual(current_contact, order_contact)

    @parameterized.expand(['save', 'cancel'])
    def test003_cancel_button_edit_departments(self, save):
        """
        Orders: department Approach: In case I update the department then press on save button ( the department updated successfully) &
        when I press on cancel button ( this department not updated )

        LIMS-4765
        LIMS-4765
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + order_url : {}'.format(order_url))
        self.order_page.sleep_tiny()
        current_departments = self.order_page.get_departments()
        self.order_page.set_departments()
        new_departments = self.order_page.get_departments()
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        order_departments = self.order_page.get_departments()
        if 'save' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_departments) == {} (order_departments)'.format(new_departments, order_departments))
            self.assertEqual(new_departments, order_departments)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_departments) == {} (order_departments)'.format(current_departments,
                                                                                      order_departments))
            self.assertEqual(current_departments, order_departments)

    def test01_archive_order(self):
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
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=order_row)
        analysis_numbers_list = order_data['Analysis No.'].split(',')
        self.base_selenium.LOGGER.info(' + Try to archive order with number : {}'.format(order_data['Order No.']))
        order_deleted = self.order_page.archive_selected_orders(check_pop_up=True)
        self.base_selenium.LOGGER.info(' + {} '.format(order_deleted))

        if order_deleted:
            self.base_selenium.LOGGER.info(' + Order number : {} deleted successfully'.format(order_data['Order No.']))
            self.analyses_page.get_analyses_page()
            self.base_selenium.LOGGER.info(
                ' + Assert analysis numbers : {} is not active'.format(analysis_numbers_list))
            has_active_analysis = self.analyses_page.search_if_analysis_exist(analysis_numbers_list)
            self.base_selenium.LOGGER.info(' + Has activated analysis? : {}.'.format(has_active_analysis))
            self.assertFalse(has_active_analysis)
        else:
            self.analyses_page.get_analyses_page()
            self.base_selenium.LOGGER.info(' + Archive Analysis with numbers : {}'.format(analysis_numbers_list))
            self.analyses_page.search_by_number_and_archive(analysis_numbers_list)
            self.order_page.get_orders_page()
            rows = self.order_page.search(analysis_numbers_list[0])
            self.order_page.click_check_box(source=rows[0])
            self.base_selenium.LOGGER.info(
                ' + archive order has analysis number =  {}'.format(analysis_numbers_list[0]))
            self.order_page.archive_selected_orders()
            rows = self.order_page.result_table()
            self.assertEqual(len(rows), 1)

    def test03_restore_archived_orders(self):
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
            self.assertTrue(self.order_page.is_order_exist(value=selected_order_data['Analysis No.']))

    def test04_deleted_archived_order(self):
        """
        New: Order without/with article: Deleting of orders
        The user can hard delete any archived order
        LIMS-3257
        """
        self.order_page.get_archived_items()
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)

        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=order_row)
        analysis_numbers_list = order_data['Analysis No.'].split(',')

        self.base_selenium.LOGGER.info(' + Delete order has number = {}'.format(order_data['Order No.']))
        self.order_page.delete_selected_item()
        self.assertFalse(self.order_page.confirm_popup())

        self.analyses_page.get_analyses_page()
        self.analyses_page.get_archived_items()
        self.base_selenium.LOGGER.info(' + Is analysis number {} deleted successfully?'.format(analysis_numbers_list))
        has_active_analysis = self.analyses_page.search_if_analysis_exist(analysis_numbers_list)
        self.base_selenium.LOGGER.info(' + {} '.format(has_active_analysis))
        self.assertFalse(has_active_analysis)

    @parameterized.expand(['True', 'False'])
    def test05_order_search(self, small_letters):
        """
        New: Orders: Search Approach: User can search by any field & each field should display with yellow color

        LIMS-3492
        LIMS-3061
        :return:
        """
        row = self.order_page.get_last_order_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            search_by = row_data[column].split(',')[0]
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[
                column] == '' or column == 'Time Difference' or row_data[column] == '-':
                continue
            elif column == 'Analysis Results':
                search_by = row_data[column].split(' (')[0]

            row_data[column] = row_data[column].split(',')[0]
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            if small_letters == 'True':
                search_results = self.order_page.search(search_by)
            else:
                search_results = self.order_page.search(search_by.upper())

            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column].replace("'", '').split(',')[0] == row_data[column].replace("'", '').split(',')[
                    0]:
                    break
            self.assertEqual(row_data[column].replace("'", '').split(',')[0],
                             search_data[column].replace("'", '').split(',')[0])

    @skip('https://modeso.atlassian.net/browse/LIMS-4766')
    def test06_duplicate_order_one_copy(self):
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
        order_row_from_form_list.append(self.order_page.get_shimpment_date())
        order_row_from_form_list.append(self.order_page.get_test_date())
        order_row_from_form_list.append(
            self.order_page.get_test_plan(first_only=False))
        order_row_from_form_list.append(self.order_page.get_departments())
        self.base_selenium.LOGGER.info(
            ' + compare if data from table : {} is equal data in form {} '.format(order_row_from_table_list,
                                                                                  order_row_from_form_list))
        self.assertListEqual(order_row_from_form_list,
                             order_row_from_table_list)

