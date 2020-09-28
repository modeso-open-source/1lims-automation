from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.contacts_page import Contacts
from ui_testing.pages.login_page import Login
from ui_testing.pages.testunits_page import TstUnits
from ui_testing.pages.testunit_page import TstUnit
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from ui_testing.pages.analysis_page import SingleAnalysisPage
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from parameterized import parameterized
from random import randint
from unittest import skip
from datetime import date
import random, re
from nose.plugins.attrib import attr


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.order_page.get_orders_page()
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()

    @parameterized.expand(['save_btn', 'cancel'])
    def test001_edit_order_number_with_save_cancel_btn(self, save):
        """
        New: Orders: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-7200
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        self.info('edit order with No {}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        order_url = self.base_selenium.get_url()
        self.info('order_url : {}'.format(order_url))
        old_number = self.order_page.get_no().replace("'", "")
        new_number = self.generate_random_string()
        self.order_page.set_no(new_number)
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.sleep_medium()
            self.order_page.cancel(force=True)
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_SMALL)

        current_number = self.order_page.get_no().replace("'", "")
        if save == 'save_btn':
            self.info('Assert {} (current_number) == {} (new_number)'.format(current_number, new_number))
            self.assertEqual(current_number, new_number)
        else:
            self.info('Assert {} (current_number) == {} (old_number)'.format(current_number, old_number))
            self.assertEqual(current_number, old_number)

    @parameterized.expand(['save_btn', 'cancel'])
    def test002_update_contact_with_save_cancel_btn(self, save):
        """
        Orders: In case I update the contact then press on cancel button, a pop up should display with
        (ok & cancel) buttons and when I press on cancel button, this update shouldn't submit

        LIMS-4764
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        self.info('edit order with No {}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        order_url = self.base_selenium.get_url()
        self.info('order_url : {}'.format(order_url))
        old_contact = self.order_page.get_contact()
        new_contact = self.order_page.set_contact(remove_old=True)
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.sleep_medium()
            self.order_page.cancel(force=True)
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_SMALL)
        current_contact = self.order_page.get_contact()
        if 'save_btn' == save:
            self.info('Assert {} (current_contact) == {} (new_contact)'.format(current_contact, new_contact))
            self.assertEqual(current_contact, new_contact)
        else:
            self.info('Assert {} (current_contact) == {} (old_contact)'.format(current_contact, old_contact))
            self.assertEqual(current_contact, old_contact)

    @parameterized.expand(['save_btn', 'cancel'])
    def test003_cancel_button_edit_departments(self, save):
        """
        Orders: department Approach: In case I update the department then press on save button
        (the department updated successfully) & when I press on cancel button ( this department not updated )

        LIMS-4765
        """
        self.info('create contact with multiple departments')
        response, payload = self.contacts_api.create_contact_with_multiple_departments()
        self.assertEqual(response['status'], 1, "contact with {} Not created".format(payload))
        self.info('create order with contact {} and first department {}'.
                  format(response['company']['name'], payload['departments'][0]['text']))
        order_response, order_payload = \
            self.orders_api.create_order_with_department_by_contact_id(
                response['company']['companyId'])
        self.assertEqual(order_response['status'], 1, "order with {} Not created".format(order_payload))
        self.info('edit order with No {}'.format(order_payload[0]['orderNo']))
        self.orders_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        order_url = self.base_selenium.get_url()
        self.info('order_url : {}'.format(order_url))
        self.order_page.open_suborder_edit()
        order_department = self.order_page.get_departments()
        new_department = payload['departments'][1]['text']
        self.info("update department to {}".format(new_department))
        self.order_page.set_departments(departments=new_department, remove_old=True)
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_SMALL)
        self.order_page.open_suborder_edit()
        current_department = self.order_page.get_departments()
        if 'save_btn' == save:
            self.info('Assert {} (current_department) == {} (new_department)'.
                      format(current_department, new_department))
            self.assertCountEqual(current_department, [new_department])
        else:
            self.info('Assert {} (current_department) == {} (order_departments)'.
                      format(current_department, order_department))
            self.assertCountEqual(current_department, order_department)

    def test004_archive_main_order(self):
        """"
        User can archive a main order

        LIMS-6516
        """
        self.info('choosing a random order table row')
        selected_order = self.orders_page.select_random_table_row()
        self.assertTrue(selected_order)
        self.info('selected order : {}'.format(selected_order))
        order_number = selected_order['Order No.'].replace("'", "")
        self.info('Archive the selected item and navigating to the archived items table')
        self.orders_page.archive_selected_items()
        self.orders_page.get_archived_items()
        archived_row = self.orders_page.search(order_number)
        self.info('Checking if order number: {} is archived correctly'.format(order_number))
        self.assertIn(order_number, archived_row[0].text)
        self.info('Order number: {} is archived correctly'.format(order_number))

    @parameterized.expand(['main_order', 'suborder'])
    def test005_restore_archived_orders(self, order_type):
        """
        I can restore any sub order successfully
        LIMS-4374

        Orders: Restore Approach: User can restore any order from the archived table
        LIMS-5361 (added the main order part)
        """
        self.info("create order with multiple suborders using api")
        response, payload = self.orders_api.create_order_with_multiple_suborders()
        self.assertEqual(response['status'], 1)
        order_no = response['order']['orderNo']
        order_id = response['order']['mainOrderId']
        suborders = self.orders_api.get_suborder_by_order_id(order_id)[0]['orders']
        number_of_suborders = len(suborders)
        analysis_numbers = [suborder['analysis'][0] for suborder in suborders]
        self.info("archive order no {} using api".format(order_no))
        archive_response, _ = self.orders_api.archive_main_order(order_id)
        self.assertEqual(archive_response['message'], 'archive_success')
        self.info("Navigate to archived orders table")
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_order_no(order_no)
        if order_type == 'suborder':
            random_index = randint(0, len(suborders)-1)
            suborders_data = self.order_page.get_child_table_data()
            self.info("Restore suborder with analysis No {}".format(suborders_data[random_index]['Analysis No.']))
            self.order_page.restore_table_suborder(index=random_index)
        else:
            self.info("restore order no {}".format(order_no))
            row = self.orders_page.result_table()[0]
            self.orders_page.click_check_box(row)
            self.orders_page.restore_selected_items()

        self.info('Navigate to orders active table')
        self.orders_page.sleep_tiny()
        self.orders_page.get_active_items()
        self.orders_page.filter_by_order_no(order_no)
        if order_type == 'suborder':
            self.info('assert that only one suborder restored')
            child_data = self.orders_page.get_child_table_data(open_child=False)
            self.assertEqual(len(child_data), 1)
            self.assertEqual(suborders_data[random_index]['Analysis No.'].replace("'", ""),
                             child_data[0]['Analysis No.'].replace("'", ""))
        else:
            self.info('assert that all suborders restored')
            child_data = self.orders_page.get_child_table_data(open_child=True)
            restored_analysis_numbers = [item['Analysis No.'].replace("'", "") for item in child_data]
            self.assertEqual(len(child_data), number_of_suborders)
            self.info('asserting restored suborders are correct')
            self.assertCountEqual(analysis_numbers, restored_analysis_numbers)

    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test006_delete_main_order(self):
        """
        New: Order without/with article: Deleting of orders
        The user can hard delete any archived order

        LIMS-3257
        """
        response, payload = self.orders_api.get_all_orders(deleted=1)
        self.assertEqual(response['status'], 1, 'No archived orders')
        random_order = random.choice(response['orders'])
        suborders_response, _ = self.orders_api.get_suborder_of_archived_order(random_order['id'])
        self.assertEqual(suborders_response['status'], 1)
        suborders_data = suborders_response['orders']
        analysis_no_list = [suborder['analysis'][0] for suborder in suborders_data]
        self.info('Navigate to archived table')
        self.orders_page.get_archived_items()
        self.info('Delete order with data {}'.format(random_order['orderNo']))
        self.orders_page.filter_by_order_no(random_order['orderNo'])
        row = self.orders_page.result_table()[0]
        self.orders_page.click_check_box(row)
        self.order_page.delete_selected_item()
        self.orders_page.confirm_popup()
        self.info('filter by order no {} to make sure no result found'.format(random_order['orderNo']))
        self.orders_page.filter_by_order_no(random_order['orderNo'])
        deleted_order = self.orders_page.result_table()[0]
        self.assertTrue(deleted_order.get_attribute("textContent"), 'No data available in table')
        self.info('Navigate analysis page and assert analysis no {} not found'.format(analysis_no_list))
        self.orders_page.navigate_to_analysis_active_table()
        for analysis in analysis_no_list:
            self.analyses_page.filter_by_analysis_number(analysis)
            self.analyses_page.close_filter_menu()
            deleted_analysis = self.analyses_page.result_table()[0]
            self.assertTrue(deleted_analysis.get_attribute("textContent"), 'No data available in table')

    @parameterized.expand(['True', 'False'])
    @skip('https://modeso.atlassian.net/browse/LIMSA-267')
    def test007_order_search(self, small_letters):
        """
        New: Orders: Search Approach: User can search by any field & each field should display with yellow color

        LIMS-3492
        LIMS-3061
        """
        response, payload = self.orders_api.get_all_orders(limit=5)
        self.assertEqual(response['status'], 1)
        random_order = random.choice(response['orders'])
        self.info('{}'.format(random_order['orderNo']))
        rows = self.orders_page.search(random_order['orderNo'])[0]
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows)
        for column in row_data:
            search_by = row_data[column].split(',')[0]
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '' \
                    or column == 'Time Difference' or row_data[column] == '-':
                continue
            elif column == 'Analysis Results':
                search_by = row_data[column].split(' (')[0]

            row_data[column] = row_data[column].split(',')[0]
            self.info('search for {} : {}'.format(column, row_data[column]))
            if small_letters == 'True':
                search_results = self.order_page.search(search_by)
            else:
                search_results = self.order_page.search(search_by.upper())

            self.assertGreater(
                len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(
                    search_result)
                if search_data[column].replace("'", '').split(',')[0] == \
                        row_data[column].replace("'", '').split(',')[0]:
                    break
            self.assertEqual(row_data[column].replace("'", '').split(',')[0],
                             search_data[column].replace("'", '').split(',')[0])

    def test008_duplicate_main_order(self):
        """
        New: Orders with test units: Duplicate an order with test unit 1 copy

        LIMS-3270
        """
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1, payload)
        order_no = payload[0]['orderNo']
        self.info('duplicate order No {}'.format(payload[0]['orderNo']))
        self.order_page.filter_by_order_no(order_no)
        row = self.order_page.get_last_order_row()
        self.order_page.click_check_box(source=row)
        self.order_page.duplicate_main_order_from_table_overview()
        self.orders_page.sleep_small()
        # make sure that its the duplication page
        self.assertTrue('duplicateMainOrder' in self.base_selenium.get_url())
        after_duplicate_order = self.order_page.get_suborder_data()
        self.info('duplicated order no {}'.format(after_duplicate_order['orderNo']))
        self.assertNotEqual(payload[0]['orderNo'], after_duplicate_order['orderNo'])
        # compare the contacts
        self.assertEqual(len(after_duplicate_order['contacts']), 1)
        self.assertEqual(payload[0]['contact'][0]['text'].replace(" ", ""),
                         after_duplicate_order['contacts'][0].replace(" ", ""))

        # save the duplicated order
        self.orders_page.sleep_medium()
        self.order_page.save(save_btn='orders:save_order')
        self.info('go back to the orders active')
        self.order_page.get_orders_page()
        self.info('assert that duplicated order found')
        self.order_page.filter_by_order_no(after_duplicate_order['orderNo'])
        results = self.order_page.result_table()[0].text
        self.assertIn(after_duplicate_order['orderNo'].replace("'", ""), results.replace("'", ""))

    def test009_duplicate_suborder_multiple_copies(self):
        """
        Make sure that the user can duplicate suborder with multiple copies ( record with test units )
        Make sure that the user can duplicate suborder with multiple copies ( record with test plans )

        LIMS-4285
        LIMS-6224
        """
        no_of_copies = randint(2, 5)
        orders, payload = self.orders_api.get_all_orders()
        order_no = random.choice(orders['orders'])['orderNo']
        self.info('filter by order no {}'.format(order_no))
        self.order_page.filter_by_order_no(order_no)
        data_before_duplicate_sub_order = self.order_page.get_child_table_data()[0]
        self.info("duplicate suborder with analysis no {}  {} times".format(
            data_before_duplicate_sub_order['Analysis No.'], no_of_copies))
        self.orders_page.duplicate_sub_order_from_table_overview(number_of_copies=no_of_copies)

        table_rows = self.order_page.result_table(element='general:table_child')
        self.info('Make sure that created sub-orders has same data of the original order')
        for index in range(no_of_copies):
            data_after_duplicate_sub_order = self.base_selenium.get_row_cells_dict_related_to_header(
                row=table_rows[index], table_element='general:table_child')
            self.info('Check if sub order created number: {} with analysis No'.format(index + 1))
            self.assertTrue(data_after_duplicate_sub_order['Analysis No.'])
            self.assertNotEqual(data_after_duplicate_sub_order['Analysis No.'],
                                data_before_duplicate_sub_order['Analysis No.'])
            self.info('Check if sub order {} created number has Material Type = {} '.
                      format(index + 1, data_before_duplicate_sub_order['Material Type']))
            self.assertEqual(data_before_duplicate_sub_order['Material Type'],
                             data_after_duplicate_sub_order['Material Type'])
            self.info('Check if order created number: {} has Article Name = {}'.
                      format(index + 1, data_before_duplicate_sub_order['Article Name']))
            self.assertEqual(data_before_duplicate_sub_order['Article Name'],
                             data_after_duplicate_sub_order['Article Name'])
            self.info('Check if order created number: {} has Article Number = {}'.
                      format(index + 1, data_before_duplicate_sub_order['Article No.']))
            self.assertEqual(data_before_duplicate_sub_order['Article No.'],
                             data_after_duplicate_sub_order['Article No.'])
            self.info('Check if order created number:  {} has Test Date = {} '.
                      format(index + 1, data_before_duplicate_sub_order['Test Date']))
            self.assertEqual(data_before_duplicate_sub_order['Test Date'],
                             data_after_duplicate_sub_order['Test Date'])
            self.info('Check if order created number:  {} has Test Plan = {} '.
                      format(index + 1, data_before_duplicate_sub_order['Test Plans']))
            self.assertEqual(data_before_duplicate_sub_order['Test Plans'],
                             data_after_duplicate_sub_order['Test Plans'])

            self.info('Check if order created number:  {} has Test unit = {} '.
                      format(index + 1, data_before_duplicate_sub_order['Test Units']))
            self.assertEqual(data_before_duplicate_sub_order['Test Units'],
                             data_after_duplicate_sub_order['Test Units'])

    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test010_user_can_add_suborder(self):
        """
        New: Orders: Table view: Suborder Approach: User can add suborder from the main order

        LIMS-3817
        """
        self.info("create completed test plan")
        test_plan = TestPlanAPI().create_completed_testplan_random_data()
        self.assertIsNotNone(test_plan)
        self.info("get random order")
        orders, api = self.orders_api.get_all_orders(limit=50)
        order = random.choice(orders['orders'])
        self.info('edit order no {}'.format(order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(order['id'])
        self.info("add new suborder with {} material, {} article and {} test_plan".
                  format(test_plan['materialType'][0]['text'],
                         test_plan['selectedArticles'][0]['text'],
                         test_plan['testPlan']['text']))

        suborder_data = self.order_page.create_new_suborder(
            material_type=test_plan['materialType'][0]['text'],
            article_name=test_plan['selectedArticles'][0]['text'],
            test_plans=[test_plan['testPlan']['text']], test_units=[],
            add_new_suborder_btn='order:add_another_suborder')

        self.assertEqual(suborder_data['orderNo'].replace("'", ""), order['orderNo'])
        self.order_page.save(save_btn='order:save_btn')

        self.order_page.get_orders_page()
        self.orders_page.sleep_small()
        self.orders_page.filter_by_order_no(order['orderNo'])
        suborders_data_after = self.orders_page.get_child_table_data()[0]
        self.assertEqual(suborders_data_after['Material Type'], test_plan['materialType'][0]['text'])
        self.assertEqual(suborders_data_after['Article Name'], test_plan['selectedArticles'][0]['text'])
        self.assertEqual(suborders_data_after['Test Plans'], test_plan['testPlan']['text'])
        self.assertIn(suborders_data_after['Test Units'], suborder_data['suborders'][-1]['testunits'][0]['name'])

        self.order_page.navigate_to_analysis_active_table()
        self.info('Assert There is an analysis for this new suborder')
        self.analyses_page.filter_by_order_no(order['orderNo'])
        self.assertEqual(len(self.orders_page.result_table()) - 1, order['analysisCount'] + 1)
        latest_order_data = self.orders_page.get_the_latest_row_data()
        self.assertEqual(suborders_data_after['Analysis No.'], latest_order_data['Analysis No.'])

    def test011_update_suborder_materialtype_cancel_button(self):
        """
        New: Orders: Edit material type: Make sure that user can cancel any update successfully
        New: Orders: Materiel type Approach: In case then material type of the second suborder
        updated then press on cancel button, Nothing update when I enter one more time

        LIMS-4281
        LIMS-4282
        """
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1, "no new order created")
        material_type = random.choice(GeneralUtilitiesAPI().
                                      get_material_types_without_duplicate(payload[0]['materialType']['text']))
        self.info("update material type of first suborder to {}".format(material_type))
        self.orders_page.get_order_edit_page_by_id(id=response['order']['mainOrderId'])
        self.orders_page.sleep_small()
        suborders_data_before_update = self.order_page.get_suborder_data()
        self.order_page.update_suborder(material_type=material_type)
        self.orders_page.sleep_small()
        self.info("check pop up mssg that all analysis will be deleted")
        self.assertTrue(self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'))
        pop_up_mssg = self.base_selenium.get_text(element='general:confirmation_pop_up')
        self.assertIn("All analysis created with this order and test plan will be deleted", pop_up_mssg)
        self.orders_page.confirm_popup()
        self.info("press on cancel button to cancel changes")
        self.orders_page.cancel()
        self.info("Navigate to order edit page and make sure suborder data not changed")
        self.orders_page.get_order_edit_page_by_id(id=response['order']['mainOrderId'])
        suborders_data_after_update = self.order_page.get_suborder_data()
        self.assertCountEqual(suborders_data_after_update, suborders_data_before_update)

    def test012_update_suborder_materialtype(self):
        """
        New: Orders: Material type Approach: I can update the material type
        filed with test units records successfully

        LIMS-4833
        """
        order, payload = self.orders_api.create_new_order(testPlans=[])
        self.assertEqual(order['status'], 1)
        old_material = payload[0]['materialType']['text']
        self.info("selected order has material type {}".format(old_material))
        new_article = random.choice(ArticleAPI().get_article_with_different_material(old_material))
        new_material = new_article['materialType']
        self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
        self.info("Duplicate it to make sure that I have two suborders to update the second one ")
        self.order_page.duplicate_from_table_view()
        self.order_page.save(save_btn='order:save_btn')
        self.orders_page.sleep_small()
        suborders_data_before_update = self.order_page.get_suborder_data()
        material_type_before_update = suborders_data_before_update['suborders'][1]['material_type']
        article_before_update = suborders_data_before_update['suborders'][1]['article']['name']
        testunit_before_update = suborders_data_before_update['suborders'][1]['testunits'][0]['name']
        self.info("update material type to {}".format(new_material))
        self.order_page.update_suborder(sub_order_index=1,
                                        material_type=new_material,
                                        articles=[new_article['name']],
                                        test_units=[''], confirm_pop_up=True)
        self.order_page.save(save_btn='order:save_btn')
        self.orders_page.sleep_small()
        suborders_data_after_update = self.order_page.get_suborder_data()
        material_type_after_update = suborders_data_after_update['suborders'][1]['material_type']
        article_after_update = suborders_data_after_update['suborders'][1]['article']['name']
        testunit_after_update = suborders_data_after_update['suborders'][1]['testunits'][0]['name']
        self.assertNotEqual(material_type_before_update, material_type_after_update)
        self.assertNotEqual(article_before_update, article_after_update)
        self.assertNotEqual(testunit_before_update, testunit_after_update)

    @parameterized.expand(['materialType', 'article', 'testPlans',
                           'testUnit'])
    def test013_filter_by_any_fields(self, key):
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
        self.base_selenium.scroll()
        self.orders_page.close_filter_menu()
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            results = self.order_page.result_table()
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if filter_value in suborder[filter_element['result_key']].split(',\n'):
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.close_child_table(source=results[i])

    def test014_filter_by_analysis_no(self):
        """
        New: Orders: Filter Approach: I can filter by analysis No

        LIMS-3495
        """
        self.info('select random order using api')
        order, suborder = self.orders_api.get_order_with_testunit_testplans()
        order_data = suborder[0]
        filter_element = self.order_page.order_filters_element(key='analysis')
        filter_value = order_data['analysis'][0]
        self.info('filter by analysis No {}'.format(filter_value))
        self.orders_page.filter_by_analysis_number(filter_value)
        self.base_selenium.scroll()
        self.orders_page.close_filter_menu()
        self.assertEqual(len(self.order_page.result_table()), 2)
        self.orders_page.sleep_tiny()
        suborders = self.orders_page.get_child_table_data()
        key_found = False
        for suborder in suborders:
            if filter_value == suborder[filter_element['result_key']].replace("'", ""):
                key_found = True
                break
        self.assertTrue(key_found)

    def test015_filter_by_order_No(self):
        """
        I can filter by any order No.

        LIMS-3495

        Filter: Order number format: In case the order number displayed with full year, I can filter by it

        LIMS-7426
        """
        self.info('select random order using api')
        orders, _ = self.orders_api.get_all_orders()
        order = random.choice(orders['orders'])
        self.assertIn('-2020', order['orderNo'], 'selected order with format {}'.format(order['orderNo']))
        self.info('filter by order No. {}'.format(order['orderNo']))
        self.orders_page.filter_by_order_no(order['orderNo'])
        result_order = self.orders_page.result_table()
        self.assertEqual(len(self.order_page.result_table()), 2)
        self.assertIn(order['orderNo'], result_order[0].text.replace("'", ""))
        self.assertIn('-2020', result_order[0].text.replace("'", ""))

    def test016_filter_by_status(self):
        """
        I can filter by status

        LIMS-3495
        """
        self.info("filter by status: Open")
        self.orders_page.apply_filter_scenario(filter_element='orders:status_filter',
                                               filter_text='Open', field_type='drop_down')

        self.info('get random suborder from result table to check that filter works')
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        suborders = self.orders_page.get_child_table_data(index=randint(0, len(results) - 1))
        filter_key_found = False
        for suborder in suborders:
            if suborder['Status'] == 'Open':
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)

    def test017_filter_by_analysis_result(self):
        """
        I can filter by Analysis result

        LIMS-3495
        """
        self.info("filter by analysis_result: Conform")
        self.orders_page.apply_filter_scenario(filter_element='orders:analysis_result_filter',
                                               filter_text='Not Recieved', field_type='drop_down')
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        self.info('get random suborder from result table to check that filter works')
        suborders = self.orders_page.get_child_table_data(index=randint(0, len(results) - 1))
        filter_key_found = False
        for suborder in suborders:
            if suborder['Analysis Results'].split(' (')[0] == 'Not Recieved':
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)

    def test018_filter_by_contact(self):
        """
        New: Orders: Filter Approach: I can filter by contact

        LIMS-3495
        """
        self.info('get contact of random order')
        contact = self.orders_api.get_random_contact_in_order()
        self.info('filter by contact {}'.format(contact))
        self.orders_page.apply_filter_scenario(filter_element='orders:contact_filter',
                                               filter_text=contact, field_type='drop_down')
        self.orders_page.sleep_tiny()
        results = self.orders_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for result in results:
            if result.text:
                self.assertIn(contact, result.text)

    def test019_filter_by_department(self):
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

        results = self.order_page.result_table()
        self.assertGreater(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if department in suborder['Departments'].split(',\n'):
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.open_child_table(source=results[i])

    @parameterized.expand(['testDate', 'shipmentDate', 'createdAt'])
    @skip("https://modeso.atlassian.net/browse/LIMSA-279")
    def test020_filter_by_date(self, key):
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
        self.assertGreater(len(self.order_page.result_table()), 1)
        suborders = self.orders_page.get_child_table_data()
        filter_key_found = False
        for suborder in suborders:
            if suborder[filter_element['result_key']] == filter_value:
                filter_key_found = True
                break
        self.assertTrue(filter_key_found)

    def test021_validate_order_test_unit_test_plan(self):
        """
        New: orders Test plan /test unit validation

        LIMS-4349
        """
        self.info(' Running test case to make sure from the validation of the test plan & test unit ')

        self.order_page.create_new_order(material_type='r', article='', contact='a', test_plans=[],
                                         test_units=[], multiple_suborders=0)
        self.info('waiting to validation message appear when I did not enter test plan & test unit')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.info('Assert the error message to make sure that validation of the test plan & test units fields ? {}'
                  .format(validation_result))
        self.assertTrue(validation_result)

    def test022_validate_order_test_unit_test_plan_edit_mode(self):
        """
        New: orders Test plan /test unit validation in edit mode

        LIMS-4826
        """
        self.info(' Running test case to check that '
                  'at least test unit or test plan is mandatory in order')
        # Get random order
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1, "order not created ")
        self.orders_page.get_order_edit_page_by_id(id=response['order']['mainOrderId'])
        # edit suborder
        self.info(' Remove all selected test plans and test units')
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[0]
        suborder_row.click()
        # delete test plan and test unit
        if self.order_page.get_test_plan():
            self.order_page.clear_test_plan()
            self.order_page.confirm_popup(force=True)

        if self.order_page.get_test_unit():
            self.order_page.clear_test_unit()

        self.order_page.save(save_btn='order:save_btn')
        # the red border will display on the test unit only because one of them should be mandatory
        test_unit_class_name = self.base_selenium.get_attribute(element="order:test_unit", attribute='class')
        self.assertIn('has-error', test_unit_class_name)

    @parameterized.expand(['save_btn', 'cancel'])
    def test023_update_test_date(self, save):
        """
        New: Orders: Test Date: I can update test date successfully with cancel/save buttons

        LIMS-4780
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
        new_test_date = self.order_page.update_suborder(sub_order_index=row_id, test_date=True, articles='')

        # save or cancel
        if 'save_btn' == save:
            self.order_page.sleep_medium()
            self.order_page.save(save_btn='order:save_btn')
            self.order_page.sleep_medium()
        else:
            self.order_page.sleep_medium()
            self.order_page.cancel(force=True)

        # refresh the page
        self.info('reopen the edited order page')
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        # get the saved test_date
        saved_test_date = self.order_page.get_suborder_data()['suborders'][row_id]['test_date']

        # check if the test date changed or not
        if 'cancel' == save:
            self.info('Assert {} (current_test_date) != {} (new_test_date)'.
                      format(new_test_date, saved_test_date))
            self.assertNotEqual(saved_test_date, new_test_date)
        else:
            self.info('Assert {} (current_test_date) == {} (new_test_date)'.
                      format(new_test_date, saved_test_date))
            self.assertEqual(saved_test_date, new_test_date)

    @parameterized.expand(['save_btn', 'cancel'])
    def test024_update_shipment_date(self, save):
        """
        New: Orders: Shipment date Approach: I can update shipment date successfully with save/cancel button

        LIMS-4779
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
        new_shipment_date = self.order_page.update_suborder(sub_order_index=row_id, shipment_date=True, articles='')

        # save or cancel
        if 'save_btn' == save:
            self.order_page.save(save_btn='order:save_btn')
            self.order_page.sleep_medium()
        else:
            self.order_page.sleep_medium()
            self.order_page.cancel(force=True)

        # refresh the page
        self.info('reopen the edited order page')
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        # get the saved shipment date
        saved_shipment_date = self.order_page.get_suborder_data()['suborders'][row_id]['shipment_date']

        # check if the shipment date changed or not
        if 'cancel' == save:
            self.info('Assert {} (current_shipment_date) != {} (new_shipment_date)'.
                      format(new_shipment_date, saved_shipment_date))
            self.assertNotEqual(saved_shipment_date, new_shipment_date)
        else:
            self.info('Assert {} (current_shipment_date) == {} (new_shipment_date)'.
                      format(new_shipment_date, saved_shipment_date))
            self.assertEqual(saved_shipment_date, new_shipment_date)

    def test025_validate_order_no_exists(self):
        """
        New: Orders: Create new order and change the autogenerated number

        LIMS-3406
        """
        orders, payload = self.orders_api.get_all_orders(limit=40)
        random_order = random.choice(orders['orders'])['orderNo'].replace("'", "")
        self.info('selected active order no {}'.format(random_order))
        archived_orders, _ = self.orders_api.get_all_orders(deleted=1)
        archived_order = random.choice(archived_orders['orders'])['orderNo'].replace("'", "")
        archived_order_to_deleted = random.choice(archived_orders['orders'])
        response, _ = self.orders_api.delete_main_order(archived_order_to_deleted['orderId'])
        self.assertEqual(response['message'], 'delete_success')
        self.info('create new order with order no {}'.format(random_order))
        self.order_page.create_new_order(order_no=random_order, material_type='Raw Material')
        self.info('waiting fo validation message appear when I enter number already exists')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert the error message to make sure that validation when '
                  'I enter number already exists? {}'.format(validation_result))
        self.assertTrue(validation_result)
        self.assertTrue(self.base_selenium.wait_element(element='order:error_in_number_mssg'))
        error_mssg = self.base_selenium.find_element(element='order:error_in_number_mssg')
        self.assertEqual('No. already exist', error_mssg.text)
        self.order_page.set_no(archived_order)
        self.orders_page.sleep_tiny()
        self.info('waiting fo validation message appear when I enter number archived')
        validation_result1 = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert the error message to make sure that validation when '
                  'I enter number archived? {}'.format(validation_result1))
        self.assertTrue(validation_result1)
        self.assertTrue(self.base_selenium.wait_element(element='order:error_in_number_mssg'))
        error_mssg2 = self.base_selenium.find_element(element='order:error_in_number_mssg')
        self.assertIn('Item already exists in archived', error_mssg2.text)
        self.order_page.set_no(archived_order_to_deleted['orderNo'])
        self.orders_page.sleep_tiny()
        self.assertFalse(self.base_selenium.check_element_is_exist(element='general:oh_snap_msg'))
        self.orders_page.save_and_wait('order:save_btn')
        number = self.order_page.get_no().replace("'", "")
        self.assertEqual(number, archived_order_to_deleted['orderNo'])

    @parameterized.expand(['new', 'existing'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test026_create_order_with_test_units(self, order):
        """
        New: Orders: Create a new order with test units

        LIMS-3267

        New: Orders: Create an existing order with test units

        LIMS-3268
        """
        response, payload = TestUnitAPI().create_qualitative_testunit()
        self.assertEqual(response['status'], 1)
        self.orders_page.sleep_small()
        self.info("create order with test unit {}".format(payload['name']))
        if order == 'new':
            created_order_no = self.order_page.create_new_order(material_type='Raw Material',
                                                                test_plans=[],
                                                                test_units=[payload['name']])
        else:
            created_order_no = self.order_page.create_existing_order(no='', material_type='Raw Material',
                                                                     test_units=[payload['name']])

        self.order_page.get_orders_page()
        self.orders_page.navigate_to_analysis_active_table()
        self.info('Assert There is an analysis for this new order.')
        self.analyses_page.filter_by_order_no(created_order_no)
        orders_analyess = self.orders_page.result_table()
        latest_order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=orders_analyess[0])
        self.assertEqual(created_order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        child_data = self.analyses_page.get_child_table_data()
        self.assertEqual(len(child_data), 1)
        self.assertEqual(child_data[0]['Test Unit'], payload['name'])

    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test028_create_existing_order_with_test_units_and_change_material_type(self):
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

        self.orders_page.sleep_small()
        article = self.order_page.set_article()
        test_unit = self.order_page.set_test_unit()
        self.order_page.save(save_btn='order:save_btn', sleep=True)

        self.order_page.get_orders_page()
        self.orders_page.navigate_to_analysis_active_table()

        self.info('Assert There is an analysis for this new order.')
        self.analyses_page.apply_filter_scenario(
            filter_element='orders:filter_order_no', filter_text=order_no, field_type='drop_down')
        latest_order_data = \
            self.base_selenium.get_row_cells_dict_related_to_header(row=self.analyses_page.result_table()[0])
        self.assertEqual(order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        self.assertEqual(article.split(' No:')[0], latest_order_data['Article Name'])
        self.assertEqual(test_unit[0], self.analyses_page.get_child_table_data()[0]['Test Unit'])
        self.assertEqual('Subassembely', latest_order_data['Material Type'])

    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test029_create_existing_order_with_test_units_and_change_article(self):
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

        if self.order_page.get_test_unit() == [] and self.order_page.get_test_plan() == []:
            test_unit = self.order_page.set_test_unit()
        self.order_page.sleep_small()
        self.assertEqual(self.order_page.get_test_unit(), test_unit)
        self.assertEqual(self.order_page.get_material_type(), material_type)

        self.order_page.save(save_btn='order:save_btn')
        self.order_page.get_orders_page()
        self.orders_page.navigate_to_analysis_active_table()
        self.info('Assert There is an analysis for this new order.')
        self.analyses_page.apply_filter_scenario(
            filter_element='orders:filter_order_no', filter_text=order_no, field_type='drop_down')

        latest_order_data = \
            self.base_selenium.get_row_cells_dict_related_to_header(row=self.analyses_page.result_table()[0])
        self.assertEqual(order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))
        self.assertEqual(article.split(' No:')[0], latest_order_data['Article Name'])
        self.assertEqual(test_unit, self.analyses_page.get_child_table_data()[0]['Test Unit'])
        self.assertEqual(material_type, latest_order_data['Material Type'])

    @skip("https://modeso.atlassian.net/browse/LIMSA-281")
    @skip("https://modeso.atlassian.net/browse/LIMSA-280")
    def test030_archive_sub_order(self):
        """
        orders :Make sure that by clicking on Archive from Suborder options a confirmation popup will appear
        and user can Archive this suborder with its corresponding analysis
        LIMS-3739
        LIMS-5369
        """
        self.info('select random order')
        random_row = self.orders_page.get_random_table_row(table_element='general:table')
        self.info('open child table')
        self.orders_page.open_child_table(source=random_row)
        self.info('archive suborder from orders active table')
        child_table_records = self.orders_page.result_table(element='general:table_child')
        sub_orders = self.orders_page.get_table_data(table_element='general:table_child')
        selected_sub_order = randint(0, len(sub_orders) - 1)
        analysis_no = sub_orders[selected_sub_order]['Analysis No.']
        self.orders_page.open_row_options(row=child_table_records[selected_sub_order])
        self.base_selenium.click(element='orders:suborder_archive')
        self.assertTrue(self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'))
        self.orders_page.confirm_popup()
        self.orders_page.get_archived_items()
        self.info('make sure that suborder is archived')
        self.orders_page.filter_by_analysis_number(analysis_no)
        self.orders_page.open_child_table(source=self.orders_page.result_table()[0])
        results = self.order_page.result_table(element='general:table_child')[0].text
        self.assertIn(analysis_no.replace("'", ""), results.replace("'", ""))

    # @parameterized.expand(['testPlans', 'testUnit'])
    # def test030_update_material_type(self, case):
    #     """
    #     -When user update the materiel type from table view once I delete it message will appear
    #     (All analysis created with this order and test plan/ test unit will be deleted )
    #     -Once you press on OK button, the material type & article & test pan/ test unit will delete
    #     -You can update it by choose another one and choose corresponding article & test plan/ test unit
    #     LIMS-4264 ( order with test plan )
    #     LIMS-4267 (order with test unit )
    #     """
    #     self.test_plan_api = TestPlanAPI()
    #     self.info('create new order')
    #     response, order_payload = self.orders_api.create_new_order()
    #     self.assertEqual(response['status'], 1, order_payload)
    #     self.info('get random completed test plan with different material type')
    #     test_plan = \
    #         self.test_plan_api.get_completed_testplans_with_material_and_same_article(material_type='Raw Material',
    #                                                                                   article='', articleNo='')[0]
    #
    #     test_unit = self.test_plan_api.get_testunits_in_testplan(test_plan['id'])[0]
    #     self.info('update material type of order from {} to {}'.format(
    #         order_payload[0]['materialType']['text'], test_plan['materialType']))
    #
    #     self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
    #     suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[0]
    #     suborder_row.click()
    #     self.order_page.set_material_type(test_plan['materialType'])
    #     self.order_page.sleep_small()
    #     self.assertTrue(self.base_selenium.check_element_is_exist(element="general:confirmation_pop_up"))
    #     self.info('confirm pop_up')
    #     self.orders_page.confirm_popup()
    #     self.info('assert article and test plan/ test unit  are empty')
    #     self.assertFalse(self.order_page.get_article())
    #     self.assertFalse(self.order_page.get_test_plan())
    #     self.assertFalse(self.order_page.get_test_unit())
    #     if test_plan['article'][0] == 'all':
    #         article = self.order_page.set_article('')
    #         self.order_page.sleep_small()
    #     else:
    #         self.order_page.set_article(test_plan['article'][0])
    #         article = test_plan['article'][0]
    #
    #     if case == 'testPlans':
    #         self.info("set article to {} and test plan to {}".
    #                   format(test_plan['article'][0], test_plan['testPlanName']))
    #         self.order_page.set_test_plan(test_plan['testPlanName'])
    #         self.order_page.sleep_small()
    #     else:
    #         self.info("set article to {} and test unit to {}".format(test_plan['article'][0],
    #                                                                  test_unit['name']))
    #         self.order_page.set_test_unit(test_unit['name'])
    #         self.order_page.sleep_small()
    #
    #     self.order_page.save_and_wait(save_btn='order:save_btn')
    #     self.info('get order data after edit and refresh')
    #     suborder_after_refresh = self.orders_api.get_order_by_id(response['order']['mainOrderId'])[0]['orders'][0]
    #     self.info('navigate to analysis page to make sure analysis corresponding to suborder updated')
    #     self.order_page.get_orders_page()
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.filter_by_analysis_number(suborder_after_refresh['analysisNos'][0]['analysisNo'])
    #     analyses = self.analyses_page.get_the_latest_row_data()
    #     self.assertEqual(test_plan['materialType'], analyses['Material Type'])
    #     self.assertEqual(article.replace(" ", ""), analyses['Article Name'].replace(" ", ""))
    #     if case == 'testPlans':
    #         self.assertEqual(test_plan['testPlanName'], analyses['Test Plans'])
    #     else:
    #         child_table_data = self.analyses_page.get_child_table_data()[0]
    #         self.assertEqual(test_unit['name'], child_table_data['Test Unit'])
    #
    # def test031_update_suborder_testunits(self):
    #     """
    #     -When I delete test unit to update it message will appear
    #     ( This Test Unit will be removed from the corresponding analysis )
    #     -Make sure the corresponding analysis records created according to this update in test unit.
    #     LIMS-4269 case 2
    #     """
    #     self.info(" get random order with one test unit")
    #     order, sub_order, sub_order_index = self.orders_api.get_order_with_field_name(field='testUnit', no_of_field=1)
    #     self.info("get new test unit with material_type {}".format(sub_order[sub_order_index]['materialType']))
    #
    #     new_test_unit_name = TestUnitAPI().get_test_unit_name_with_value_with_material_type(
    #         material_type=sub_order[sub_order_index]['materialType'], avoid_duplicate=True,
    #         duplicated_test_unit=sub_order[sub_order_index]['testUnit'][0]['testUnit']['name'])['name']
    #
    #     self.info("Edit sub-order {} in order no. {} with test_unit {}".format(
    #         len(sub_order) - 1 - sub_order_index, order['orderNo'], new_test_unit_name))
    #     self.info("open order edit page")
    #     self.orders_page.get_order_edit_page_by_id(order['orderId'])
    #     self.order_page.update_suborder(sub_order_index=int(len(sub_order) - 1 - sub_order_index),
    #                                     test_units=[new_test_unit_name], remove_old=True, confirm_pop_up=True, articles='')
    #     # checking that when adding new test unit, the newly added test unit is added to the
    #     # order's analysis instead of creating new analysis
    #     self.order_page.save_and_wait(save_btn='order:save_btn')
    #     self.info('Get suborder data to check it')
    #     suborder_testunits_after_edit = self.orders_api.get_suborder_by_order_id(
    #         order['orderId'])[0]['orders'][sub_order_index]['testUnit']
    #     testunits_after_edit = [testunit['testUnit']['name'] for testunit in suborder_testunits_after_edit]
    #     self.assertEqual(len(testunits_after_edit), 1)
    #     self.info('Assert Test units: test units are: {}, and should be: {}'.
    #               format(testunits_after_edit, new_test_unit_name))
    #     self.assertEqual(testunits_after_edit[0], new_test_unit_name)
    #
    #     self.info('Getting analysis page to check the data in this child table')
    #     self.order_page.get_orders_page()
    #     self.orders_page.filter_by_analysis_number(sub_order[sub_order_index]['analysis'])
    #     sub_order_data = self.orders_page.get_child_table_data()[0]
    #     self.assertEqual(sub_order_data['Test Units'], new_test_unit_name)
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
    #                                              filter_text=sub_order[sub_order_index]['analysis'],
    #                                              field_type='text')
    #     analysis_records = self.analyses_page.get_child_table_data()
    #     test_units = [analysis_record['Test Unit'] for analysis_record in analysis_records]
    #     self.assertIn(new_test_unit_name, test_units)
    #
    # def test032_update_order_article(self):
    #     """
    #     New: Orders: Edit Approach: I can update the article successfully and press on ok button
    #     then press on cancel button, Nothing updated
    #     LIMS-4297 - save case
    #     New: Orders: Edit Approach: I can update the article filed successfully with save button
    #     LIMS-3423
    #     """
    #     self.info('get random order')
    #     orders, _ = self.orders_api.get_all_orders(limit=50)
    #     order = random.choice(orders['orders'])
    #     suborders, _ = self.orders_api.get_suborder_by_order_id(order['id'])
    #     suborder = suborders['orders'][0]
    #     suborder_update_index = len(suborders['orders']) - 1
    #     test_units = [test_unit['testUnit']['name'] for test_unit in suborder['testUnit']]
    #
    #     self.info('get random completed test plan with different article')
    #     test_plans = TestPlanAPI().get_completed_testplans()
    #     test_plans_with_different_article = [test_plan for test_plan in test_plans if
    #                                          test_plan['materialType'] == suborder['materialType'] and
    #                                          suborder['article'] != test_plan['article'][0]]
    #     if test_plans_with_different_article:
    #         test_plan_data = random.choice(test_plans_with_different_article)
    #         test_plan = test_plan_data['testPlanName']
    #         article = test_plan_data['article'][0]
    #     else:
    #         article_data = ArticleAPI().get_article_with_material_type(suborder['materialType'])
    #         article = article_data['name']
    #         formatted_article = {'id': article_data['id'], 'text': article}
    #         new_test_plan = TestPlanAPI().create_completed_testplan(
    #             material_type=suborder['materialType'], formatted_article=formatted_article)
    #         test_plan = new_test_plan['testPlanEntity']['name']
    #
    #     test_plans = [test_plan]
    #     self.info('update order {} with article {}'.format(order['orderNo'], article))
    #     self.orders_page.get_order_edit_page_by_id(order['id'])
    #     if article == 'all':
    #         self.order_page.update_suborder(sub_order_index=suborder_update_index, articles='')
    #         article = self.order_page.get_article()
    #     else:
    #         self.order_page.update_suborder(sub_order_index=suborder_update_index, articles=article)
    #
    #     self.info('assert test plan is empty')
    #     self.assertFalse(self.order_page.get_test_plan())
    #     if test_units:
    #         self.assertCountEqual(self.order_page.get_test_unit(), test_units)
    #     else:
    #         self.assertFalse(self.order_page.get_test_unit())
    #
    #     self.order_page.set_test_plan(test_plan)
    #     self.info('save the changes then refresh')
    #     self.order_page.save(save_btn='order:save_btn')
    #     self.order_page.get_orders_page()
    #
    #     self.info('navigate to analysis page to make sure analysis corresponding to suborder updated')
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.filter_by_analysis_number(suborder['analysis'])
    #     analyses = self.analyses_page.get_the_latest_row_data()
    #     analyses_test_plans = analyses['Test Plans'].replace("'", '').split(", ")
    #     self.info('assert that article and test plan changed but test unit still the same')
    #     self.assertEqual(article.replace(' ', ''), analyses['Article Name'].replace(' ', ''))
    #     self.assertCountEqual(test_plans, analyses_test_plans)
    #     child_data = self.analyses_page.get_child_table_data()
    #     result_test_units = [test_unit['Test Unit'] for test_unit in child_data]
    #     for testunit in test_units:
    #         self.assertIn(testunit, result_test_units)
    #
    # def test033_update_order_article_cancel_approach(self):
    #     """
    #     New: Orders: Edit Approach: I can update the article successfully and press on ok button
    #     then press on cancel button, Nothing updated
    #     LIMS-4297 - cancel case
    #     """
    #     self.info('get random order')
    #     orders, _ = self.orders_api.get_all_orders(limit=50)
    #     order = random.choice(orders['orders'])
    #     suborders, _ = self.orders_api.get_suborder_by_order_id(order['id'])
    #     suborder = suborders['orders'][0]
    #     suborder_update_index = len(suborders['orders']) - 1
    #     test_units = [test_unit['testUnit']['name'] for test_unit in suborder['testUnit']]
    #
    #     self.info('update order {} with random article'.format(order['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(order['orderId'])
    #     self.order_page.update_suborder(sub_order_index=suborder_update_index, articles='a', confirm_pop_up=True, remove_old=True)
    #     self.info('assert test plan is empty')
    #     self.assertFalse(self.order_page.get_test_plan())
    #     if test_units:
    #         self.assertCountEqual(self.order_page.get_test_unit(), test_units)
    #     else:
    #         self.assertCountEqual(self.order_page.get_test_unit(), ['Search'])
    #     self.order_page.cancel()
    #     self.info('navigate to analysis page to make sure analysis corresponding to suborder updated')
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.filter_by_analysis_number(suborder['analysis'])
    #     analyses = self.analyses_page.get_the_latest_row_data()
    #     analyses_test_plans = analyses['Test Plans'].replace("'", '').split(", ")
    #     self.info('assert that article, test plan and test unit still the same')
    #     self.assertEqual(suborder['article'].replace(' ', ''), analyses['Article Name'].replace(' ', ''))
    #     if suborder['testPlans']:
    #         self.assertCountEqual(suborder['testPlans'], analyses_test_plans)
    #     else:
    #         self.assertCountEqual(['-'], analyses_test_plans)
    #     child_data = self.analyses_page.get_child_table_data()
    #     result_test_units = [test_unit['Test Unit'] for test_unit in child_data]
    #     for testunit in test_units:
    #         self.assertIn(testunit, result_test_units[0])
    #
    # def test034_create_new_suborder_with_testunit(self):
    #     """
    #     New: Orders: Create Approach: I can create suborder with test unit successfully,
    #     make sure the record created successfully in the analysis section.
    #     LIMS-4255
    #     """
    #     self.single_analysis_page = SingleAnalysisPage()
    #     article, article_data = ArticleAPI().create_article()
    #     random_testunit, payload = TestUnitAPI().get_all_test_units(filter='{"materialTypes":"all"}')
    #     testunit_record = random.choice(random_testunit['testUnits'])
    #     orders, payload = self.orders_api.get_all_orders(limit=20)
    #     order = random.choice(orders['orders'])
    #     self.info(
    #         '{}'.format(order['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(order['id'])
    #     self.info('getting analysis tab to check out the count of the analysis')
    #     self.order_page.navigate_to_analysis_tab()
    #     analysis_count_before_adding = self.single_analysis_page.get_analysis_count()
    #
    #     self.info('get back to order tab')
    #     self.single_analysis_page.navigate_to_order_tab()
    #     order_data_before_adding_new_suborder = self.order_page.get_suborder_data()
    #     suborder_count_before_adding = len(order_data_before_adding_new_suborder['suborders'])
    #     self.info('count of analysis equals: ' + str(analysis_count_before_adding) +
    #               "\t count of suborders equals: " + str(suborder_count_before_adding))
    #
    #     self.info('create new suborder with materialType {}, and article {}, and testUnit {}'.format(
    #         article_data['materialType']['text'], article['article']['name'], testunit_record['name']))
    #
    #     self.order_page.create_new_suborder_with_test_units(
    #         material_type=article_data['materialType']['text'],
    #         article_name=article['article']['name'], test_unit=testunit_record['name'])
    #     self.order_page.save(save_btn='order:save_btn', sleep=True)
    #     self.base_selenium.refresh()
    #     self.order_page.sleep_tiny()
    #
    #     order_data_after_adding_new_suborder = self.order_page.get_suborder_data()
    #     self.assertEqual(suborder_count_before_adding + 1,
    #                      len(order_data_after_adding_new_suborder['suborders']))
    #
    #     self.info('navigate to analysis page to make sure that only one analysis is added')
    #     self.order_page.navigate_to_analysis_tab()
    #     analysis_count = self.single_analysis_page.get_analysis_count()
    #
    #     self.info('check analysis count\t' + str(analysis_count) + "\tequals\t" + str(analysis_count_before_adding + 1))
    #     self.assertGreaterEqual(analysis_count, analysis_count_before_adding + 1)
    #
    #     analysis_record = self.single_analysis_page.open_accordion_for_analysis_index(analysis_count - 1)
    #     testunit_in_analysis = self.single_analysis_page.get_testunits_in_analysis(source=analysis_record)
    #     self.assertEqual(len(testunit_in_analysis), 1)
    #     testunit_name = testunit_in_analysis[0]['']
    #     self.assertIn(testunit_record['name'], testunit_name)
    #
    # @parameterized.expand(['save_btn', 'cancel_btn'])
    # def test035_update_departments_in_second_suborder(self, action):
    #     """
    #      Orders: department Approach: In case I update the department then press on save button
    #      (the department updated successfully) & when I press on cancel button (this department
    #      not updated) (this will apply from the second order)
    #      LIMS-6523
    #     """
    #     self.info('create contact')
    #     response, payload = ContactsAPI().create_contact()
    #     contact, contact_id = payload, response['company']['companyId']
    #
    #     orders, payload = self.orders_api.get_all_orders(limit=20)
    #     order = random.choice(orders['orders'])
    #     self.info(
    #         '{}'.format(order['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(order['id'])
    #     order_data = self.order_page.get_suborder_data()
    #     if len(order_data['suborders']) <= 1:
    #         self.order_page.duplicate_from_table_view()
    #         self.order_page.save(save_btn='order:save_btn')
    #
    #     self.order_page.set_contact(contact=contact['name'])
    #     self.order_page.sleep_small()
    #     self.order_page.save(save_btn='order:save_btn', sleep=True)
    #     self.base_selenium.refresh()
    #
    #     selected_suborder_data = self.order_page.get_suborder_data()
    #     self.order_page.update_suborder(sub_order_index=1, departments=contact['departments'][0]['text'], articles='')
    #     self.order_page.save(save_btn='order:' + action)
    #     if action == 'save_btn':
    #         self.base_selenium.refresh()
    #         suborder_data_after_update = self.order_page.get_suborder_data()
    #         self.assertIn(contact['departments'][0]['text'], suborder_data_after_update['suborders'][1]['departments'])
    #     else:
    #         self.order_page.confirm_popup()
    #         self.orders_page.get_order_edit_page_by_id(order['id'])
    #         suborder_data_after_cancel = self.order_page.get_suborder_data()
    #         self.assertEqual(suborder_data_after_cancel['suborders'][1], selected_suborder_data['suborders'][1])
    #
    # def test036_update_order_no_should_reflect_all_suborders_and_analysis(self):
    #     """
    #     In case I update the order number of record that has multiple suborders inside it
    #     all those suborders numbers updated according to that and (this will effect in the
    #     analysis records also that mean all order number of those records will updated
    #     according to that in the active table )
    #     LIMS-4270
    #     """
    #     self.info('generate new order number to use it for update')
    #     new_order_no = str(self.orders_api.get_auto_generated_order_no()[0]['id'])
    #     year_value = str(self.order_page.get_current_year()[2:])
    #     formated_order_no = new_order_no + '-' + year_value
    #     self.info('newly generated order number = {}'.format(formated_order_no))
    #     response, _ = self.orders_api.get_all_orders(limit=20)
    #     order = random.choice(response['orders'])
    #     self.orders_page.get_order_edit_page_by_id(id=order['orderId'])
    #     self.order_page.set_no(no=formated_order_no)
    #     self.order_page.sleep_small()
    #     self.order_page.save_and_wait(save_btn='order:save_btn')
    #     order_no_after_update = self.order_page.get_no()
    #     self.info('order no is {}, and it should be {}'.format(order_no_after_update, formated_order_no))
    #     self.assertEqual(order_no_after_update.replace("'", ""), formated_order_no)
    #     self.info('navigate to analysis tab to make sure that order no updated correctly')
    #     self.orders_page.get_orders_page()
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.search(formated_order_no )
    #     analysis_record = SingleAnalysisPage().get_the_latest_row_data()
    #     self.info('checking order no of each analysis')
    #     self.assertEqual(analysis_record['Order No.'], formated_order_no)
    #
    # def test037_Duplicate_main_order_and_cahange_materiel_type(self):
    #     """
    #     duplicate the main order then change the materiel type
    #     LIMS-6219
    #     """
    #     self.info('get random main order data')
    #     orders, payload = self.orders_api.create_new_order()
    #     self.order_page.search(payload[0]['orderNo'])
    #     self.info('duplicate the main order')
    #     self.order_page.duplicate_main_order_from_order_option()
    #     self.order_page.wait_until_page_is_loaded()
    #     duplicated_order_number = self.order_page.get_no()
    #     self.info('order to be duplicated is {}, new order no is {}'.
    #               format(payload[0]['orderNo'], duplicated_order_number))
    #     self.assertNotEqual(payload[0]['orderNo'], duplicated_order_number)
    #     self.info('get completed test plan with different material type')
    #     selected_test_plan = TestPlanAPI().get_completed_testplans_with_material_and_same_article(material_type='Raw Material',
    #                                                                                   article='', articleNo='')[0]
    #
    #     self.info('change material type of first suborder')
    #     self.order_page.set_material_type_of_first_suborder(material_type=selected_test_plan['materialType'])
    #     self.info('Make sure that article, test unit, and test plan are empty')
    #     self.assertEqual(self.base_selenium.get_value(element='order:article'), None)
    #     self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
    #     self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
    #     self.info('select random article, test unit and test plan')
    #     # we need to select random article because we can't update the article by ALL article in the order section
    #     selected_article = self.order_page.set_article(article='')
    #     self.order_page.set_test_plan(test_plan=selected_test_plan['testPlanName'])
    #     test_unit = self.order_page.set_test_unit()
    #     self.info('duplicated order material is {}, article {}, test_unit {} and test_plan {}'.
    #               format(selected_test_plan['materialType'], selected_test_plan['article'][0],
    #                      test_unit, selected_test_plan['testPlanName']))
    #     self.order_page.save(save_btn='order:save_btn', sleep=True)
    #     self.info("navigate to orders' page to make sure that order duplicated correctly with selected data")
    #     self.order_page.get_orders_page()
    #     self.order_page.search(duplicated_order_number)
    #     child_data = self.order_page.get_child_table_data()
    #     if len(child_data) > 1:
    #         suborder_data = child_data[-1]
    #     else:
    #         suborder_data = child_data[0]
    #
    #     self.info('Make sure that suborder data is correct')
    #     self.assertEqual(suborder_data['Material Type'], selected_test_plan['materialType'])
    #     self.assertEqual(suborder_data['Article Name'].replace("'", ""), selected_article)
    #     self.assertEqual(suborder_data['Test Units'], test_unit[0])
    #     self.assertEqual(suborder_data['Test Plans'], selected_test_plan['testPlanName'])
    #
    # def test038_archived_test_unit_shoudnt_display_in_the_order_drop_down_list(self):
    #     """
    #     Orders: Archived Test unit: Archive Approach: Archived test units shouldn't appear in orders in the drop down
    #     list
    #     LIMS-3710
    #     :return:
    #     """
    #     self.test_unit_api = TestUnitAPI()
    #     re, payload = TestUnitAPI().create_qualitative_testunit()
    #     self.test_unit_api.archive_testunits(ids=[str(re['testUnit']['testUnitId'])])
    #     self.base_selenium.click(element='orders:new_order')
    #     self.order_page.set_new_order()
    #     self.order_page.sleep_small()
    #     self.order_page.set_material_type_of_first_suborder(material_type='r', sub_order_index=0)
    #
    #     self.info('Asset test unit is not existing in the list')
    #     self.assertFalse(self.order_page.is_testunit_existing(
    #         test_unit=payload['name']))
    #
    def test039_duplicate_sub_order_table_with_add(self):
        """
         Orders: User can duplicate any suborder from the order form ( table with add )

         LIMS-3738

         [Orders][Active Table]Make sure that every record should display the main order
         and when user click on it suborders will be expanded

         LIMS-5356
         
         [Orders][Archive Table]Make sure that every record should display the main order
         and when user click on it will display suborders under order record
         
         LIMS-5357
        """
        self.info('select random record')
        random_order = random.choice(self.orders_api.get_all_orders_json())
        suborders = self.orders_api.get_suborder_by_order_id(random_order['orderId'])[0]['orders']
        contacts = [contact['name'] for contact in random_order['company']]
        self.orders_page.filter_by_order_no(random_order['orderNo'])
        row = self.orders_page.result_table()[0]
        self.info('assert that child table arrow exist')
        childtable_arrow = self.base_selenium.find_element_in_element(
            destination_element='general:child_table_arrow', source=row)
        self.assertTrue(childtable_arrow)
        childtable_arrow.click()
        self.orders_page.sleep_tiny()
        self.info("assert when click in child table arrow, all suborders appears")
        suborders_data = self.orders_page.get_table_data()
        self.assertEqual(len(suborders), len(suborders_data))
        for i in range(len(suborders)):
            self.assertEqual(suborders_data[i]['Analysis No.'].replace("'", ""), suborders[i]['analysis'][0])
        self.info("open order edit page")
        self.orders_page.open_edit_page_by_css_selector(row)
        self.orders_page.sleep_small()
        self.info("Duplicate first suborder from table view")
        self.order_page.duplicate_from_table_view(index_to_duplicate_from=0)
        after_duplicate_order = self.order_page.get_suborder_data()
        self.info("make sure that the new order has same order No and contact")
        self.assertEqual(random_order['orderNo'], after_duplicate_order['orderNo'].replace("'", ""))
        self.assertCountEqual(contacts, after_duplicate_order['contacts'])
        self.info("save the duplicated order")
        self.order_page.save(save_btn='orders:save_order')
        self.info("go back to the table view, and assert that duplicated suborder added to child table")
        self.order_page.get_orders_page()
        self.order_page.filter_by_order_no(random_order['orderNo'])
        suborder_data = self.order_page.get_child_table_data()
        self.assertTrue(len(suborder_data), len(suborders)+1)
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_analysis_number(suborder_data[0]['Analysis No.'])
        analysis_result = self.analyses_page.get_the_latest_row_data()['Analysis No.'].replace("'", "")
        self.assertEqual(suborder_data[0]['Analysis No.'].replace("'", ""), analysis_result)

    # def test040_Duplicate_sub_order_and_cahange_materiel_type(self):
    #     """
    #     duplicate sub-order of any order then change the materiel type
    #     LIMS-6227
    #     """
    #     self.info('get random main order data')
    #     orders, payload = self.orders_api.create_new_order()
    #     self.order_page.search(payload[0]['orderNo'])
    #     self.order_page.get_child_table_data()
    #     self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
    #     self.order_page.duplicate_sub_order_from_table_overview()
    #     self.info('get completed test plan with different material type')
    #     selected_test_plan = TestPlanAPI().get_completed_testplans_with_material_and_same_article(
    #                                                                                        material_type='Raw Material',
    #                                                                                        article='',
    #                                                                                        articleNo='')[0]
    #     self.order_page.set_material_type_of_first_suborder(material_type=selected_test_plan['materialType'])
    #     self.info('Make sure that article, test unit, and test plan are empty')
    #     self.assertEqual(self.base_selenium.get_value(element='order:article'), None)
    #     self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
    #     self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
    #     self.info('set suborder new data')
    #     # we need to select random article because we can't update the article by ALL article in the order section
    #     selected_article = self.order_page.set_article(article='')
    #     test_unit = self.order_page.set_test_unit()
    #     self.order_page.set_test_plan(test_plan=selected_test_plan['testPlanName'])
    #     self.info('duplicated sub order material is {}, article {}, test_unit {} and test_plan {}'.
    #               format(selected_test_plan['materialType'], selected_test_plan['article'][0],
    #                      test_unit, selected_test_plan['testPlanName']))
    #     self.order_page.save(save_btn='order:save_btn', sleep=True)
    #
    #     self.info("navigate to orders' active table and check that duplicated suborder found")
    #     self.order_page.get_orders_page()
    #     self.order_page.search(payload[0]['orderNo'])
    #     child_data = self.order_page.get_child_table_data()
    #     duplicated_suborder_data = child_data[0]
    #     self.assertEqual(duplicated_suborder_data['Material Type'], selected_test_plan['materialType'])
    #     self.assertEqual(duplicated_suborder_data['Article Name'], selected_article)
    #     self.assertEqual(duplicated_suborder_data['Test Units'], test_unit[0])
    #     self.assertEqual(duplicated_suborder_data['Test Plans'], selected_test_plan['testPlanName'])
    #
    # def test041_delete_suborder(self):
    #     """
    #      Delete sub order Approach: In case I have main order with multiple sub orders,
    #      make sure you can delete one of them
    #      LIMS-6853
    #     """
    #     self.info('get random order with multiple suborders')
    #     order = self.orders_api.get_order_with_multiple_sub_orders()
    #     self.order_page.search(order['orderNo'])
    #     self.info('archive first suborder')
    #     suborder_data = self.order_page.get_child_table_data()[0]
    #     self.order_page.archive_sub_order_from_active_table()
    #     self.orders_page.delete_sub_order(analysis_no=suborder_data['Analysis No.'])
    #
    #     self.info('Navigate to order page to make sure that suborder is deleted and main order still active')
    #     self.order_page.get_orders_page()
    #     self.order_page.search(order['orderNo'])
    #     suborders_after_delete = self.order_page.get_child_table_data()
    #     self.assertNotIn(suborder_data['Analysis No.'], suborders_after_delete)
    #     self.assertGreater(len(suborder_data), 0)
    #
    #     self.info('Navigate to Analysis page to make sure that analysis related to deleted suborder not found')
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
    #                                              filter_text=suborder_data['Analysis No.'], field_type='text')
    #     self.assertEqual(len(self.order_page.result_table()), 1)
    #
    # def test042_archive_new_order_and_analysis(self):
    #     """
    #     New: Orders Form: Archive main order: Make sure when the user archive main order,
    #     the analysis corresponding to it will be archived also
    #     LIMS-6873
    #     """
    #     self.info("select random order to archive")
    #     orders, api = self.orders_api.get_all_orders(limit=20)
    #     order = random.choice(orders['orders'])
    #     self.info(
    #         '{}'.format(order['orderNo']))
    #     suborder_data, api = self.orders_api.get_suborder_by_order_id(order['id'])
    #     suborders = suborder_data['orders']
    #     analysis_no_list = []
    #     for suborder in suborders:
    #         analysis_no_list.append(suborder['analysis'])
    #
    #     self.info(" Archive order with number : {}".format(order['orderNo']))
    #     order_row = self.order_page.search(order['orderNo'])
    #     self.order_page.click_check_box(source=order_row[0])
    #     self.order_page.archive_selected_orders(check_pop_up=True)
    #     self.info("Navigate to archived orders' table and filter by analysis no")
    #     self.orders_page.get_archived_items()
    #     self.orders_page.filter_by_analysis_number(analysis_no_list[0])
    #     self.assertTrue(self.orders_page.is_order_in_table(value=order['orderNo']))
    #     child_data = self.orders_page.get_child_table_data()
    #     result_analysis = []
    #     for suborder in child_data:
    #         result_analysis.append(suborder['Analysis No.'].replace("'", ""))
    #     self.assertCountEqual(result_analysis, analysis_no_list)
    #
    # def test043_Duplicate_sub_order_with_multiple_testplans_and_testunits_delet_approach(self):
    #     """
    #     Duplicate suborder Approach: Duplicate any sub order then delete the units & test plans
    #     LIMS-6852
    #     """
    #     self.info('create order data multiple testplans and test units')
    #     response, payload = self.orders_api.create_order_with_double_test_plans()
    #     self.orders_page.filter_by_order_no(payload[0]['orderNo'])
    #     suborder_data_before_duplicate = self.orders_page.get_child_table_data()
    #     test_plans = [suborder_data_before_duplicate[0]['Test Plans'].split(',\n')[0],
    #                   suborder_data_before_duplicate[0]['Test Plans'].split(',\n')[1]]
    #     test_units = [suborder_data_before_duplicate[0]['Test Units'].split(',\n')[0],
    #                   suborder_data_before_duplicate[0]['Test Units'].split(',\n')[1]]
    #     self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
    #     self.orders_page.duplicate_sub_order_from_table_overview()
    #     self.base_selenium.clear_items_in_drop_down(element='order:test_plan', one_item_only=True)
    #     self.base_selenium.clear_items_in_drop_down(element='order:test_unit', one_item_only=True)
    #     self.order_page.save(save_btn='order:save')
    #     self.order_page.wait_until_page_is_loaded()
    #     self.info("navigate to orders' active table and check that duplicated suborder found")
    #     self.order_page.get_orders_page()
    #     self.orders_page.filter_by_order_no(payload[0]['orderNo'])
    #     child_data = self.order_page.get_child_table_data()
    #     duplicated_suborder_data = child_data[0]
    #     self.assertEqual(len(child_data), 2)
    #     self.assertEqual(duplicated_suborder_data['Article Name'], suborder_data_before_duplicate[0]['Article Name'])
    #     self.assertEqual(duplicated_suborder_data['Material Type'], suborder_data_before_duplicate[0]['Material Type'])
    #     self.assertIn(duplicated_suborder_data['Test Units'], test_units)
    #     self.assertIn(duplicated_suborder_data['Test Plans'], test_plans)
    #
    # def test044_duplicate_main_order_change_contact(self):
    #     """
    #     Duplicate from the main order Approach: Duplicate then change the contact
    #     LIMS-6222
    #     """
    #     self.info('get random main order data')
    #     orders, payload = self.orders_api.get_all_orders(limit=20)
    #     self.assertEqual(orders['status'], 1)
    #     main_order = random.choice(orders['orders'])
    #     self.info(
    #         '{}'.format(main_order['orderNo']))
    #     self.info("duplicate order No {}".format(main_order['orderNo']))
    #     self.order_page.search(main_order['orderNo'])
    #     self.order_page.duplicate_main_order_from_order_option()
    #     new_contact = self.order_page.set_contact(contact='', remove_old=True)
    #     duplicted_order_no = self.order_page.get_no()
    #     self.order_page.save(save_btn='order:save')
    #     self.orders_page.get_orders_page()
    #     self.orders_page.filter_by_order_no(duplicted_order_no)
    #     order = self.orders_page.get_the_latest_row_data()
    #     self.assertEqual(new_contact[0], order['Contact Name'])
    #
    # def test045_duplicate_main_order_with_multiple_contacts(self):
    #     """
    #     Orders: Duplicate suborder: Multiple contacts Approach: : All contacts are correct in case
    #     I duplicate from the main order or from the suborder
    #     LIMS-5816
    #     """
    #     self.info('create order with multiple contacts')
    #     response, payload = self.orders_api.create_order_with_multiple_contacts()
    #     self.assertEqual(response['status'], 1)
    #     contacts = [contact['text'] for contact in payload[0]['contact']]
    #     self.orders_page.filter_by_order_no(payload[0]['orderNo'])
    #
    #     self.info("duplicate the order {} from order's options".format(payload[0]['orderNo']))
    #     self.orders_page.duplicate_main_order_from_order_option()
    #     duplicated_order_no = self.order_page.get_no()
    #     self.order_page.save(save_btn='order:save')
    #     self.info("navigate to orders' active table and check that duplicated suborder found")
    #     self.order_page.get_orders_page()
    #
    #     self.orders_page.filter_by_order_no(duplicated_order_no)
    #     duplicated_order_data = self.orders_page.get_the_latest_row_data()
    #     duplicated_contacts = duplicated_order_data['Contact Name'].split(',\n')
    #     self.assertCountEqual(duplicated_contacts, contacts)
    #
    # def test046_duplicate_sub_order_with_multiple_contacts(self):
    #     """
    #     Orders: Duplicate suborder: Multiple contacts Approach: : All contacts are correct in case
    #     I duplicate from the main order or from the suborder
    #     LIMS-5816
    #     """
    #     self.info('create order with multiple contacts')
    #     response, payload = self.orders_api.create_order_with_multiple_contacts()
    #     self.assertEqual(response['status'], 1, response)
    #     contacts = [contact['text'] for contact in payload[0]['contact']]
    #     self.orders_page.filter_by_order_no(payload[0]['orderNo'])
    #
    #     self.order_page.get_child_table_data()
    #     self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
    #     self.orders_page.duplicate_sub_order_from_table_overview(number_of_copies=4)
    #     self.base_selenium.refresh()
    #     self.orders_page.wait_until_page_is_loaded()
    #     self.orders_page.filter_by_order_no(payload[0]['orderNo'])
    #
    #     duplicated_order_data = self.orders_page.get_the_latest_row_data()
    #     duplicated_contacts = duplicated_order_data['Contact Name'].split(',\n')
    #     self.assertCountEqual(duplicated_contacts, contacts)
    #
    #     duplicated_suborders = self.orders_page.get_child_table_data()
    #     self.assertEqual(len(duplicated_suborders), 5)
    #     analyses_numbers = [suborder['Analysis No.'] for suborder in duplicated_suborders]
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.open_filter_menu()
    #     for analysis in analyses_numbers:
    #         self.analyses_page.filter_by(
    #             filter_element='analysis_page:analysis_no_filter', filter_text=analysis, field_type='text')
    #         self.analyses_page.filter_apply()
    #         analysis_data = self.analyses_page.get_the_latest_row_data()
    #         duplicated_contacts_in_analyses = analysis_data['Contact Name'].split(', ')
    #         self.assertEqual(len(duplicated_contacts_in_analyses), 3)
    #         self.assertCountEqual(duplicated_contacts, contacts)
    #
    # def test047_delete_multiple_orders(self):
    #     """
    #     Orders: Make sure that you can't delete multiple orders records at the same time
    #     LIMS-6854
    #     """
    #     self.info("navigate to archived items' table")
    #     self.orders_page.get_archived_items()
    #     self.orders_page.select_random_multiple_table_rows()
    #     self.orders_page.delete_selected_item(confirm_pop_up=False)
    #     confirm_edit = self.base_selenium.check_element_is_exist(element="general:cant_delete_message")
    #     confirm_edit_message = self.base_selenium.get_text(element="general:confirmation_pop_up")
    #     self.assertTrue(confirm_edit)
    #     self.assertIn('You cannot do this action on more than one record', confirm_edit_message)
    #
    # def test048_update_sub_order_with_multiple_testplans_only_delete_approach(self):
    #     """
    #     Orders: Test plans: In case I have order record with multiple test plans and I updated them,
    #     this update should reflect on the same analysis record without creating new one.
    #     LIMS-4134 case 1
    #     """
    #     self.info('create order with two testplans only')
    #     response, payload = self.orders_api.create_order_with_double_test_plans(only_test_plans=True)
    #     self.assertEqual(response['status'], 1)
    #     test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
    #     self.info("created order has test plans {} and {} ".format(test_plans[0], test_plans[1]))
    #     test_units = [TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']),
    #                   TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number'])]
    #     self.info("Edit order {}".format(payload[0]['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
    #     suborder_before_edit = self.order_page.get_suborder_data()
    #     self.info('Assert that selected order has one analysis record')
    #     self.assertEqual(len(suborder_before_edit['suborders']), 1)
    #     analysis_no = suborder_before_edit['suborders'][0]['analysis_no']
    #     self.order_page.open_suborder_edit(sub_order_index=0)
    #     self.info("remove only one test plan")
    #     self.base_selenium.clear_items_in_drop_down(element='order:test_plan', one_item_only=True)
    #     self.info("confirm pop_up")
    #     self.order_page.confirm_popup()
    #     self.order_page.save(save_btn='order:save_btn', sleep=True)
    #     self.info("navigate to analysis' active table and check that pld analysis edited without creating new analysis")
    #     self.order_page.get_orders_page()
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.filter_by_order_no(payload[0]['orderNo'])
    #     self.assertEqual(len(self.analyses_page.result_table()) - 1, 1)
    #     analysis_data = self.analyses_page.get_the_latest_row_data()
    #     found_test_plans = analysis_data['Test Plans'].split(', ')
    #     self.info("assert that only one test plan found and analysis no not changed")
    #     self.assertEqual(len(found_test_plans), 1)
    #     self.assertEqual(analysis_data['Analysis No.'], analysis_no)
    #     suborder_data = self.analyses_page.get_child_table_data()
    #     for test_plan in test_plans:
    #         for test_unit in test_units:
    #             if found_test_plans == test_plan:
    #                 self.info("assert that test unit related to deleted test plan removed from analysis")
    #                 self.assertEqual(test_unit, suborder_data['Test Unit'])
    #
    # def test049_update_sub_order_with_multiple_testplans_only_add_approach(self):
    #     """
    #     Orders: Test plans: In case I have order record with multiple test plans and I updated them,
    #     this update should reflect on the same analysis record without creating new one.
    #     LIMS-4134
    #     """
    #     self.info('create order with two testplans only')
    #     response, payload = self.orders_api.create_order_with_double_test_plans(only_test_plans=True)
    #     self.assertEqual(response['status'], 1)
    #     test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
    #     self.info("created order has test plans {} and {} ".format(test_plans[0], test_plans[1]))
    #     test_units = [TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']),
    #                   TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number'])]
    #
    #     article_no = ArticleAPI().get_article_form_data(id=payload[0]['article']['id'])[0]['article']['No']
    #     self.info("get new completed test plan with article {} No: {} and material_type {}".format(
    #         payload[0]['article']['text'], article_no, payload[0]['materialType']['text']))
    #
    #     completed_test_plans = TestPlanAPI().get_completed_testplans_with_material_and_same_article(
    #         material_type=payload[0]['materialType']['text'], article=payload[0]['article']['text'],
    #         articleNo=article_no)
    #     completed_test_plans_without_old = [testplan for testplan in completed_test_plans
    #                                         if testplan['testPlanName'] not in test_plans]
    #
    #     if completed_test_plans_without_old:
    #         test_plan_data = random.choice(completed_test_plans_without_old)
    #         test_plan = test_plan_data['testPlanName']
    #         test_unit_data = TestPlanAPI().get_testunits_in_testplan(id=test_plan_data['id'])
    #         test_unit = test_unit_data[0]['name']
    #     else:
    #         self.info("There is no completed test plan so create it ")
    #         formatted_article = {'id': payload[0]['article']['id'], 'text': payload[0]['article']['text']}
    #         new_test_plan = TestPlanAPI().create_completed_testplan(
    #             material_type=payload[0]['materialType']['text'], formatted_article=formatted_article)
    #         test_plan = new_test_plan['testPlanEntity']['name']
    #         test_unit = new_test_plan['specifications'][0]['name']
    #         self.info("completed test plan created with name {} and test unit {}".format(test_plan, test_unit))
    #
    #     test_plans.append(test_plan)
    #     test_units.append(test_unit)
    #
    #     self.info("edit the sub order of order {}".format(payload[0]['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
    #     suborder_before_edit = self.order_page.get_suborder_data()
    #     self.info('Assert that selected order has one analysis record')
    #     self.assertEqual(len(suborder_before_edit['suborders']), 1)
    #     analysis_no = suborder_before_edit['suborders'][0]['analysis_no']
    #     self.order_page.update_suborder(test_plans=[test_plan], articles='')
    #     self.order_page.save(save_btn='order:save_btn')
    #     self.info("navigate to orders' active table and check that duplicated suborder found")
    #     self.order_page.get_orders_page()
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.filter_by_order_no(payload[0]['orderNo'])
    #     self.assertEqual(len(self.analyses_page.result_table()) - 1, 1)
    #     analysis_data = self.analyses_page.get_the_latest_row_data()
    #     found_test_plans = analysis_data['Test Plans'].split(', ')
    #     self.assertEqual(len(found_test_plans), 3)
    #     self.assertEqual(analysis_data['Analysis No.'], analysis_no)
    #     suborder_data = self.analyses_page.get_child_table_data()
    #     found_test_units = [testunit['Test Unit'] for testunit in suborder_data]
    #     self.assertCountEqual(test_plans, found_test_plans)
    #     self.assertNotEqual(test_units, found_test_units)
    #
    # @parameterized.expand(['change', 'add'])
    # def test050_duplicate_main_order_with_testPlan_and_testUnit_edit_both(self, case):
    #     """
    #     Duplicate from the main order Approach: Duplicate then change the test units & test plans
    #     LIMS-6221
    #     Duplicate from the main order Approach: Duplicate then update test unit/plan by deleting
    #     any test plan & test unit
    #     LIMS-6841
    #     Duplicate from the main order Approach: Duplicate by adding test unit & plan
    #     LIMS-6231
    #     """
    #     self.info('create order with test plan and test unit')
    #     response, payload = self.orders_api.create_new_order()
    #     self.assertEqual(response['status'], 1, response)
    #     self.info('order created with payload {}'.format(payload))
    #     self.info('get valid test plan and test unit to edit suborder data')
    #     new_test_plan, new_test_unit = TestPlanAPI().get_order_valid_testplan_and_test_unit(
    #         material_type=payload[0]['materialType']['text'],
    #         used_test_plan=payload[0]['testPlans'][0]['name'],
    #         used_test_unit=payload[0]['testUnits'][0]['name'],
    #         article_id=payload[0]['article']['id'], article=payload[0]['article']['text'])
    #
    #     self.info("duplicate order No {} ".format(payload[0]['orderNo']))
    #     self.orders_page.search(payload[0]['orderNo'])
    #     self.info("duplicate main order")
    #     self.orders_page.duplicate_main_order_from_order_option()
    #     self.assertIn("duplicateMainOrder", self.base_selenium.get_url())
    #     self.order_page.sleep_medium()
    #     duplicated_order_No = self.order_page.get_no()
    #     self.info("duplicated order No is {}".format(duplicated_order_No))
    #     self.assertNotEqual(duplicated_order_No, payload[0]['orderNo'])
    #     if case == 'add':
    #         self.info("add test plan {} and test unit {} to duplicated order".format(new_test_plan, new_test_unit))
    #         self.order_page.update_suborder(test_plans=[new_test_plan], test_units=[new_test_unit], articles='')
    #     else:
    #         self.info("update test plan to {} and test unit to {}".format(new_test_plan, new_test_unit))
    #         self.order_page.update_suborder(test_plans=[new_test_plan], test_units=[new_test_unit], remove_old=True, articles='')
    #
    #     self.order_page.save(save_btn='order:save')
    #     self.info("navigate to active table")
    #     self.order_page.get_orders_page()
    #     self.assertTrue(self.orders_page.search(duplicated_order_No))
    #     duplicated_suborder_data = self.order_page.get_child_table_data()[0]
    #     if case == 'change':
    #         self.info("assert that test unit updated to {}, test plan {}".format(
    #             new_test_unit, new_test_plan))
    #         self.assertEqual(duplicated_suborder_data['Test Units'], new_test_unit)
    #         self.assertEqual(duplicated_suborder_data['Test Plans'], new_test_plan)
    #     else:
    #         self.info("assert that test unit {}, test plan {} added to duplicated order".format(
    #             new_test_unit, new_test_plan))
    #         self.assertIn(new_test_unit, duplicated_suborder_data['Test Units'])
    #         self.assertIn(new_test_plan, duplicated_suborder_data['Test Plans'])
    #
    #     self.info("navigate to analysis page")
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.assertTrue(self.analyses_page.search(duplicated_order_No))
    #     analyses = self.analyses_page.get_the_latest_row_data()
    #     if case == 'add':
    #         self.assertIn(new_test_plan, analyses['Test Plans'].replace("'", ""))
    #     else:
    #         self.assertEqual(new_test_plan, analyses['Test Plans'].replace("'", ""))
    #     child_data = self.analyses_page.get_child_table_data()
    #     test_units = [test_unit['Test Unit'] for test_unit in child_data]
    #     self.assertIn(new_test_unit, test_units)
    #
    # def test051_duplicate_sub_order_with_testPlan_and_testUnit_change_both(self):
    #     """
    #     Duplicate suborder Approach: Duplicate any sub order then change the units & test plans
    #     (remove them and put another ones )
    #
    #     LIMS-6229
    #     """
    #     self.info('create order with test plan and test unit')
    #     response, payload = self.orders_api.create_new_order()
    #     self.assertEqual(response['status'], 1)
    #     self.info('order created with payload {}'.format(payload))
    #     self.info('get valid test plan and test unit to edit suborder data')
    #     new_test_plan, new_test_unit = TestPlanAPI().get_order_valid_testplan_and_test_unit(
    #         material_type=payload[0]['materialType']['text'],
    #         used_test_plan=payload[0]['testPlans'][0]['name'],
    #         used_test_unit=payload[0]['testUnits'][0]['name'],
    #         article_id=payload[0]['article']['id'], article=payload[0]['article']['text']
    #     )
    #
    #     self.info("duplicate order No {} ".format(payload[0]['orderNo']))
    #     self.orders_page.search(payload[0]['orderNo'])
    #     self.info("duplicate sub order with one copy only")
    #     self.orders_page.open_child_table(source=self.orders_page.result_table()[0])
    #     self.orders_page.duplicate_sub_order_from_table_overview()
    #     self.info("update test plan to {} and test unit to {}".format(new_test_plan, new_test_unit))
    #     self.order_page.update_suborder(test_plans=[new_test_plan], test_units=[new_test_unit], remove_old=True, articles='')
    #     self.order_page.save(save_btn='order:save')
    #
    #     self.info("navigate to analysis page")
    #     self.order_page.get_orders_page()
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.analyses_page.search(payload[0]['orderNo'])
    #     analyses = self.analyses_page.get_the_latest_row_data()
    #     self.assertEqual(new_test_plan, analyses['Test Plans'].replace("'", ""))
    #     child_data = self.analyses_page.get_child_table_data()
    #     test_units = [test_unit['Test Unit'] for test_unit in child_data]
    #     self.assertIn(new_test_unit, test_units)
    #
    # def test052_Duplicate_sub_order_with_multiple_testplans_and_testunits_add_approach(self):
    #     """
    #     Duplicate suborder Approach: Duplicate any sub order then add test unit & test plan
    #
    #     LIMS-6232
    #     """
    #     self.info('create order data multiple testplans and test units')
    #     response, payload = self.orders_api.create_order_with_double_test_plans()
    #     self.assertEqual(response['status'], 1, payload)
    #     test_plans = [payload[0]['testPlans'][0]['testPlanName'], payload[0]['testPlans'][1]['testPlanName']]
    #     test_units = [payload[0]['testUnits'][0]['name'], payload[0]['testUnits'][1]['name']]
    #     self.info("get new completed test plan with article {} and material_type {}".format(
    #         payload[0]['article']['text'], payload[0]['materialType']['text']))
    #
    #     test_plan, test_unit = TestPlanAPI().get_order_valid_testplan_and_test_unit(
    #         material_type=payload[0]['materialType']['text'],
    #         used_test_plan=test_plans,
    #         used_test_unit=test_units,
    #         article_id=payload[0]['article']['id'], article=payload[0]['article']['text'])
    #
    #     test_plans.append(test_plan)
    #     test_units.append(test_unit)
    #
    #     self.orders_page.search(payload[0]['orderNo'])
    #     self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
    #     self.orders_page.get_child_table_data()
    #     self.orders_page.duplicate_sub_order_from_table_overview()
    #     self.order_page.set_test_plan(test_plan)
    #     self.order_page.set_test_unit(test_unit)
    #     self.order_page.save(save_btn='order:save', sleep=True)
    #     self.orders_page.sleep_small()
    #     analysis_no = self.order_page.get_suborder_data()['suborders'][1]['analysis_no']
    #     self.info("navigate to orders' active table and check that duplicated suborder found")
    #     self.order_page.get_orders_page()
    #     self.orders_page.filter_by_analysis_number(analysis_no)
    #     child_data = self.order_page.get_child_table_data()
    #     duplicated_suborder_data = child_data[0]
    #     self.assertEqual(len(child_data), 2)
    #     self.assertEqual(duplicated_suborder_data['Article Name'].replace(' ', ''),
    #                      payload[0]['article']['text'].replace(' ', ''))
    #     self.assertEqual(duplicated_suborder_data['Material Type'], payload[0]['materialType']['text'])
    #     duplicated_suborder_test_units = duplicated_suborder_data['Test Units'].split(',\n') or []
    #     duplicated_suborder_test_plans = duplicated_suborder_data['Test Plans'].split(',\n') or []
    #     self.assertCountEqual(duplicated_suborder_test_units, test_units)
    #     self.assertCountEqual(duplicated_suborder_test_plans, test_plans)
    #
    # def test053_user_can_edit_multiple_columns(self):
    #     """
    #     user can edit multiple columns at the same time
    #     LIMS-5221
    #     """
    #     self.info('get random order with multiple suborders edit page')
    #     order = self.orders_api.get_order_with_multiple_sub_orders()
    #     subororder_data = self.orders_api.get_order_by_id(order['orderId'])[0]
    #     self.assertEqual(subororder_data['status'], 1)
    #     self.info(' edit order no {}'.format(order['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(order['orderId'])
    #     self.info('click on first row and update it')
    #     suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')
    #     suborder_row[0].click()
    #     first_department = self.order_page.set_departments('')
    #     self.info('Department updated to {}'.format(first_department))
    #     first_Shipment_date = self.order_page.set_shipment_date(row_id=0)
    #     self.info('Shipment_date updated to {}'.format(first_Shipment_date))
    #     first_test_date = self.order_page.set_test_date(row_id=0)
    #     self.info('test_date updated to {}'.format(first_test_date))
    #     self.info('save changes')
    #     self.order_page.save(save_btn='order:save')
    #     self.info('edit second suborder row')
    #     suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')
    #     suborder_row[1].click()
    #     self.order_page.set_departments('')
    #     self.order_page.set_shipment_date(row_id=1)
    #     self.order_page.set_test_date(row_id=1)
    #     self.info('press on cancel button')
    #     self.order_page.cancel()
    #     self.info('get suborders data to assert that second suborder not update updated ')
    #     result_suborder_data = self.orders_api.get_order_by_id(order['orderId'])[0]
    #     self.assertEqual(result_suborder_data['status'], 1)
    #     self.assertEqual(subororder_data['orders'][1]['shipmentDate'],
    #                      result_suborder_data['orders'][1]['shipmentDate'])
    #     self.assertEqual(subororder_data['orders'][1]['testDate'], result_suborder_data['orders'][1]['testDate'])
    #     self.info('assert first suborder updated successfully')
    #     first_suborder = result_suborder_data['orders'][0]
    #     if first_department:
    #         first_suborder_department = [dep['name'] for dep in first_suborder['departments']]
    #         self.assertCountEqual(first_department, first_suborder_department)
    #     result_Shipment_date = first_suborder['shipmentDate'].split('T')[0].split('-')
    #     result_Shipment_date.reverse()
    #     Shipment_date = "{}.{}.{}".format(result_Shipment_date[0], result_Shipment_date[1], result_Shipment_date[2])
    #     self.assertEqual(first_Shipment_date, Shipment_date)
    #     result_test_date = first_suborder['testDate'].split('T')[0].split('-')
    #     result_test_date.reverse()
    #     test_date = "{}.{}.{}".format(result_test_date[0], result_test_date[1], result_test_date[2])
    #     self.assertEqual(first_test_date, test_date)
    #
    # def test054_duplicate_main_order_with_testPlans_and_testUnits(self):
    #     """
    #     Duplicate main order Approach: duplicate order with test plan & test units
    #     LIMS-4353
    #     """
    #     self.info('create order with multiple test plans and test units')
    #     response, payload = self.orders_api.create_order_with_double_test_plans()
    #     self.assertEqual(response['status'], 1, payload)
    #     test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
    #     test_units = [testunit['name'] for testunit in payload[0]['selectedTestUnits']]
    #     test_units.extend(TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']))
    #     test_units.extend(TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number']))
    #     self.info("created order has test plans {} ".format(test_plans))
    #     self.info("created order has test units {} ".format(test_units))
    #     self.orders_page.filter_by_order_no(payload[0]['orderNo'])
    #     self.info("duplicate order no {}".format(payload[0]['orderNo']))
    #     self.orders_page.duplicate_main_order_from_order_option()
    #     self.orders_page.sleep_small()
    #     self.order_page.save(save_btn='order:save', sleep=True)
    #     duplicated_order_no = self.order_page.get_no()
    #     self.assertNotEqual(duplicated_order_no, payload[0]['orderNo'])
    #     self.info("navigate to analysis page  and make sure duplicated order created with same data")
    #     self.order_page.get_orders_page()
    #     self.orders_page.navigate_to_analysis_active_table()
    #     self.assertTrue(self.orders_page.is_order_in_table(duplicated_order_no))
    #     self.orders_page.sleep_small()
    #     self.analyses_page.search(duplicated_order_no)
    #     duplicated_test_plans = self.analyses_page.get_the_latest_row_data()['Test Plans'].split(', ')
    #     self.assertEqual(duplicated_test_plans, test_plans)
    #     duplicated_suborder_data = self.order_page.get_child_table_data()
    #     duplicated_test_units = [testunit['Test Unit'] for testunit in duplicated_suborder_data]
    #     # we need to assert not equal because the test units in the child table included the test units
    #     # in the orders section and in the test plans it self
    #     self.assertNotEqual(test_units, duplicated_test_units)
    #
    # def test055_table_with_add_edit_single_row(self):
    #     """
    #     Orders: Table with add: In case I have two suborders and I update the first one
    #     then press on the second one the first one should updated according to that
    #
    #     LIMS-5204
    #     """
    #     self.info("create new test unit edit the suborder by it ( because the test unit name is not a unique ")
    #     re, payload1 = TestUnitAPI().create_qualitative_testunit()
    #
    #     order, payload = self.orders_api.create_new_order()
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #
    #     self.info(
    #         " Duplicate it to make sure we have two suborders to edit in one and press on the other to save data in the first one ")
    #     self.order_page.duplicate_from_table_view(index_to_duplicate_from=0)
    #
    #     testunit_before_edit_row = self.order_page.get_suborder_data()['suborders'][0]['testunits']
    #     self.info("test unit before I update the first row {}".format(testunit_before_edit_row))
    #
    #     # update the first suborder to update the test unit one it
    #     self.order_page.update_suborder(test_units=[payload1['name']], sub_order_index=0, articles='')
    #     # press on the second row because I want to save data in the first one
    #     self.order_page.update_suborder(sub_order_index=1, articles='')
    #
    #     testunit_after_edit_row = self.order_page.get_sub_order_data_first_row()['suborders'][0]['testunits']
    #     self.info("test unit after I press on the second row to make sure it saved in the first one {}".format(
    #         testunit_after_edit_row))
    #
    #     self.info('Assert that the test unit not equal ')
    #     self.assertNotEqual(testunit_before_edit_row, testunit_after_edit_row)
    #
    # @parameterized.expand(['2020', '20'])
    # def test056_search_by_year(self, search_text):
    #     """
    #     Search: Orders: Make sure that you can search by all the year format
    #     ( with year in case year after or before & without year )
    #
    #     LIMS-7427
    #     """
    #     self.order_page.filter_by_order_no(search_text)
    #     results = self.orders_page.result_table()
    #     orders = [item.text.split('\n')[0] for item in results if item.text.split('\n')[0] != '']
    #     self.assertTrue(orders)
    #     for order in orders:
    #         self.assertIn(search_text, order.replace("'", ""))
    #
    # def test057_upload_attachment(self):
    #     """
    #     I can upload any attachment successfully from the order section
    #     LIMS-8258
    #     :return:
    #     """
    #     order, payload = self.orders_api.create_new_order()
    #     print(order)
    #     print(payload)
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #     self.base_selenium.click(element='order:attachment_btn')
    #     file_name = 'logo.png'
    #     upload_file = self.order_page.upload_attachment(file_name='logo.png', drop_zone_element='order:uploader_zone',
    #                                                     save=True)
    #     self.info("assert that the upload file same as the file name ".format(upload_file, file_name))
    #     self.assertEqual(upload_file, file_name)
    #
    # #@skip('https://modeso.atlassian.net/browse/LIMS-217')
    # def test058_upload_attachment_then_remove(self):
    #     """
    #     Orders step 1: Attachment download approach: There is a link under remove link for
    #     download and you can preview it by clicking on it
    #     LIMS-6933
    #     :return:
    #     """
    #     order, payload = self.orders_api.create_new_order()
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #     self.base_selenium.click(element='order:attachment_btn')
    #     file_name = 'logo.png'
    #     upload_attachment_then_save = self.order_page.upload_attachment(file_name='logo.png',
    #                                                                     drop_zone_element='order:uploader_zone',
    #                                                                     save=True)
    #     self.info("assert that the upload file same as the file name ".format(upload_attachment_then_save, file_name))
    #     self.assertEqual(upload_attachment_then_save, file_name)
    #     self.info('open the same record in the edit mode')
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #     self.base_selenium.click(element='order:attachments_btn')
    #     self.info("remove the file and submit the record ")
    #     after_remove_attachment = self.order_page.upload_attachment(file_name='logo2.png',
    #                                                                 drop_zone_element='order:uploader_zone',
    #                                                                 remove_current_file=True, save=True)
    #
    #     self.info("assert that after I remove the file it will return none should not equal to the file name ".format(
    #         after_remove_attachment, file_name))
    #     self.assertNotEqual(after_remove_attachment, file_name)
    #
    # #@skip('https://modeso.atlassian.net/browse/LIMS-217')
    # def test059_testplans_popup(self):
    #     """
    #     Orders: Test plan pop up Approach: Make sure the test plans
    #     & units displayed on the test plans & units fields same as in the test plan pop up
    #     LIMS-4796
    #     """
    #     self.test_plan_api = TestPlanAPI()
    #     order, payload = self.orders_api.create_new_order()
    #     self.info('open the order record in the edit mode')
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #     testplan_name = payload[0]['testPlans'][0]['name']
    #     self.info("get test plan name ".format(testplan_name))
    #     testplans_testunits_names_in_popup = self.order_page.get_testplan_pop_up()
    #     self.info("get test plan & test unit name from the test plan popup".format(testplans_testunits_names_in_popup))
    #     testunit_no = self.test_plan_api.get_testplan_with_quicksearch(quickSearchText=testplan_name)[0]['number']
    #     testunit_name = self.test_plan_api.get_testunits_in_testplan_by_No(no=testunit_no)[0]
    #     self.info("get test unit name".format(testunit_name))
    #     self.info("assert that the test plan in the editmode same as the test plan in the test plan pop up".format(
    #         testplan_name, testplans_testunits_names_in_popup[0]['test_plan']))
    #     self.assertEqual(testplan_name, testplans_testunits_names_in_popup[0]['test_plan'])
    #     self.info("assert that the test unint in the edit mode same as the test unit in the test unit pop up ".format(
    #         testunit_name, testplans_testunits_names_in_popup[0]['test_units'][0]))
    #     self.assertEqual(testunit_name, testplans_testunits_names_in_popup[0]['test_units'][0])
    #
    # def test060_testplans_popup_after_edit_by_add(self):
    #     """
    #     Orders: Test plan pop up  Approach: Make sure In case you edit the test plans
    #     & add another ones this update should reflect on the test plan pop up
    #     LIMS-8256
    #     """
    #     self.test_plan_api = TestPlanAPI()
    #     self.info('Get completed test plan to upade by it with raw material type')
    #     testplan = \
    #         TestPlanAPI().get_completed_testplans_with_material_and_same_article(material_type='Raw Material',
    #                                                                                   article='', articleNo='')[0]
    #     order, payload = self.orders_api.create_new_order()
    #     self.info('open the order record in the edit mode')
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #     self.info('go to update the test plan by adding the completed one')
    #     self.order_page.update_suborder(sub_order_index=0, test_plans=[testplan['testPlanName']], articles='')
    #     self.order_page.save(save_btn='order:save')
    #     testplan_name = testplan['testPlanName']
    #     self.info("Get the test plan name that I added it in the edit mode".format(testplan_name))
    #     testplans_testunits_names_in_popup = self.order_page.get_testplan_pop_up()
    #     testunit_no = self.test_plan_api.get_testplan_with_quicksearch(quickSearchText=testplan_name)[0]['number']
    #     testunit_name = self.test_plan_api.get_testunits_in_testplan_by_No(no=testunit_no)[0]
    #     self.info("assert that the test plan I added in the test plan popup ".format(testplan_name,
    #                                                                                  testplans_testunits_names_in_popup[
    #                                                                                      1]['test_plan']))
    #     self.assertEqual(testplan_name, testplans_testunits_names_in_popup[1]['test_plan'])
    #     self.info("assert that the test plan I added in the test plan popup ".format(testplan_name,
    #                                                                                  testplans_testunits_names_in_popup[
    #                                                                                      1]['test_units'][0]))
    #     self.assertEqual(testunit_name, testplans_testunits_names_in_popup[1]['test_units'][0])
    #
    # #@skip("https://modeso.atlassian.net/browse/LIMSA-127")
    # def test061_testplans_popup_after_edit_by_replace(self):
    #     """
    #     Orders: Test plan: Test unit pop up Approach: In case I delete test plan, make sure it
    #     deleted from the pop up with it's test units and updated with another one
    #     LIMS-4802
    #     """
    #     self.test_plan_api = TestPlanAPI()
    #
    #     self.info('Get completed test plan to upade by it with raw material type')
    #     testplan = \
    #         TestPlanAPI().get_completed_testplans_with_material_and_same_article(material_type='Raw Material',
    #                                                                                   article='', articleNo='')[0]
    #     order, payload = self.orders_api.create_new_order()
    #     self.info('open the order record in the edit mode')
    #     self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
    #     self.info('go to update the test plan by adding the completed one')
    #     self.order_page.update_suborder(sub_order_index=0, remove_old=True, test_plans=[testplan['testPlanName']])
    #     self.order_page.save(save_btn='order:save')
    #     testplan_name = testplan['testPlanName']
    #     self.info("Get the test plan name that I added it in the edit mode".format(testplan_name))
    #     testplans_testunits_names_in_popup = self.order_page.get_testplan_pop_up()
    #     self.info("get test plan & test unit name from the test plan popup".format(testplans_testunits_names_in_popup))
    #     testunit_no = self.test_plan_api.get_testplan_with_quicksearch(quickSearchText=testplan_name)[0]['number']
    #     testunit_name = self.test_plan_api.get_testunits_in_testplan_by_No(no=testunit_no)[0]
    #     self.info("get test unit name".format(testunit_name))
    #     self.info("assert that the test plan in the editmode same as the test plan in the test plan pop up".format(
    #         testplan_name, testplans_testunits_names_in_popup[0]['test_plan']))
    #     self.assertEqual(testplan_name, testplans_testunits_names_in_popup[0]['test_plan'])
    #     self.info("assert that the test unint in the edit mode same as the test unit in the test unit pop up ".format(
    #         testunit_name, testplans_testunits_names_in_popup[0]['test_units'][0]))
    #     self.assertEqual(testunit_name, testplans_testunits_names_in_popup[0]['test_units'][0])
    #
    # def test062_create_order_with_multiple_contacts_then_add_department(self):
    #     """
    #     User should be able to choose more than one contact from drop down menu upon creating a new order
    #
    #     LIMS-5704 'create mode'
    #     """
    #     self.info("get 3 contacts with department contacts")
    #     self.contacts_api = ContactsAPI()
    #     contact_list = random.choices(self.contacts_api.get_contacts_with_department(), k=3)
    #     self.assertTrue(contact_list, "Can't get 3 contacts with departments")
    #     contact_names_list = [contact['name'] for contact in contact_list]
    #     self.info('selected contacts are {}'.format(contact_names_list))
    #     departments_list_with_contacts = self.contacts_api.get_department_contact_list(contact_names_list)
    #     self.info('department contacts list {}'.format(departments_list_with_contacts))
    #     self.info('create new order with selected contacts')
    #     self.order_page.create_multiple_contacts_new_order(contacts=contact_names_list)
    #     self.order_page.sleep_tiny()
    #     contacts = self.order_page.get_contact()
    #     self.info('selected contacts are {}'.format(contacts))
    #     self.assertCountEqual(contacts, contact_names_list)
    #     suggested_department_list, departments_only_list = \
    #         self.order_page.get_department_suggestion_lists(contacts=contact_names_list)
    #     self.info('suggested department list {}'.format(suggested_department_list))
    #     self.info('and it should be {}'.format(departments_list_with_contacts))
    #     index = 0
    #     for item in suggested_department_list:
    #         for element in departments_list_with_contacts:
    #             if item['contact'] == element['contact']:
    #                 self.assertCountEqual(item['departments'], element['departments'])
    #                 index = index + 1
    #
    #     self.assertEqual(index, len(contact_names_list))
    #     department = random.choice(departments_only_list)
    #     self.info('set department to {}'.format(department))
    #     self.order_page.set_departments(department)
    #     self.order_page.sleep_small()
    #     self.order_page.save_and_wait(save_btn='order:save')
    #     order_data = self.order_page.get_suborder_data()
    #     self.info('assert that new order with multiple contacts created')
    #     self.assertCountEqual(order_data['contacts'], contact_names_list)
    #     self.info('assert that department updated')
    #     self.assertEqual([department], order_data['suborders'][0]['departments'])
    #
    # def test063_edit_department_of_order_with_multiple_contacts(self):
    #     """
    #     In case I select multiple contacts the departments should be updated according to that
    #
    #     LIMS-5705 'edit mode'
    #     """
    #     self.info("create order with multiple contacts")
    #     response, payload = self.orders_api.create_order_with_multiple_contacts()
    #     self.assertEqual(response['status'], 1, response)
    #     contact_names_list = [contact['text'] for contact in payload[0]['contact']]
    #     self.info('selected contacts are {}'.format(contact_names_list))
    #     departments_list_with_contacts = ContactsAPI().get_department_contact_list(contact_names_list)
    #     self.info('department contacts list {}'.format(departments_list_with_contacts))
    #     self.info('open edit page of order no {}'.format(payload[0]['orderNo']))
    #     self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
    #     self.order_page.sleep_tiny()
    #     suggested_department_list, departments_only_list = \
    #         self.order_page.get_department_suggestion_lists(open_suborder_table=True, contacts=contact_names_list)
    #     self.info('suggested department list {}'.format(suggested_department_list))
    #     self.info('and it should be {}'.format(departments_list_with_contacts))
    #     index = 0
    #     for item in suggested_department_list:
    #         for element in departments_list_with_contacts:
    #             if item['contact'] == element['contact']:
    #                 self.assertCountEqual(item['departments'], element['departments'])
    #                 index = index + 1
    #     self.assertEqual(index, len(contact_names_list))
    #
    #     department = random.choice(departments_only_list)
    #     self.info('set department to {}'.format(department))
    #     self.order_page.set_departments(department)
    #     self.order_page.save_and_wait(save_btn='order:save')
    #     suborder_data = self.order_page.get_suborder_data()
    #     self.assertEqual([department], suborder_data['suborders'][0]['departments'])
    #
    # @skip("https://modeso.atlassian.net/browse/LIMSA-205")
    # def test064_download_suborder_sheet_for_single_order(self):
    #     """
    #     Export order child table
    #
    #     LIMS-8085- single order case
    #     """
    #     self.info('select random order')
    #     random_row = self.orders_page.get_random_table_row(table_element='general:table')
    #     self.orders_page.click_check_box(source=random_row)
    #     random_row_data = self.base_selenium.get_row_cells_dict_related_to_header(random_row)
    #     self.orders_page.open_child_table(source=random_row)
    #     child_table_data = self.order_page.get_table_data()
    #     order_data_list = []
    #     order_dict = {}
    #     for sub_order in child_table_data:
    #         order_dict.update(random_row_data)
    #         order_dict.update(sub_order)
    #         order_data_list.append(order_dict)
    #         order_dict = {}
    #
    #     formatted_orders = self.order_page.match_format_to_sheet_format(order_data_list)
    #     self.order_page.download_xslx_sheet()
    #     for index in range(len(formatted_orders)):
    #         self.info('Comparing the order no {} '.format(formatted_orders[index][0]))
    #         values = self.order_page.sheet.iloc[index].values
    #         fixed_sheet_row_data = self.reformat_data(values)
    #         self.assertCountEqual(fixed_sheet_row_data, formatted_orders[index],
    #                               f"{str(fixed_sheet_row_data)} : {str(formatted_orders[index])}")
    #         for item in formatted_orders[index]:
    #             self.assertIn(item, fixed_sheet_row_data)
    #
    # @skip('need to be re-implemented to include child table data')
    # def test065_export_order_sheet(self):
    #     """
    #     New: Orders: XSLX Approach: user can download all data in table view with the same order with table view
    #
    #     LIMS-3274
    #     """
    #     self.info(' * Download XSLX sheet')
    #     self.order_page.select_all_records()
    #     self.order_page.download_xslx_sheet()
    #     rows_data = self.order_page.get_table_rows_data()
    #     for index in range(len(rows_data) - 1):
    #         self.info(
    #             ' * Comparing the order no. {} '.format(index + 1))
    #         fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
    #         values = self.order_page.sheet.iloc[index].values
    #         fixed_sheet_row_data = self.fix_data_format(values)
    #         for item in fixed_row_data:
    #             if item != " ":
    #                 self.assertIn(item, fixed_sheet_row_data)

    def test066_create_order_then_overview(self):
        """
        Orders: Create: In case of clicking on the overview button after clicking create new order
        check it redirects to the active table

        LIMS-6204
        """
        self.order_page.click_create_order_button()
        self.order_page.sleep_tiny()
        self.order_page.click_overview()
        self.info('asserting correct redirection to orders active table ')
        self.info('Active table url is {} , current url is {}'.format(
            self.orders_page.orders_url, self.base_selenium.get_url()))
        self.assertEqual(self.orders_page.orders_url, self.base_selenium.get_url())

    @parameterized.expand(['10', '20', '25', '50', '100'])
    @attr(series=True)
    def test067_testing_table_pagination(self, pagination_limit):
        """
        Orders: Active table: Pagination Approach; Make sure that I can set the pagination
        to display 10/20/25/50/100 records in each page

        LIMS-6199
        """
        self.order_page.set_page_limit(limit=pagination_limit)
        table_info = self.order_page.get_table_info_data()
        self.info('get current table records count')
        table_records_count = str(len(self.order_page.result_table()) - 1)

        self.info('table records count is {}, and it should be {}'.
                  format(table_records_count, table_info['page_limit']))
        self.assertEqual(table_records_count, table_info['page_limit'])

        self.info('current page limit is {}, and it should be {}'.
                  format(table_info['pagination_limit'], pagination_limit))
        self.assertEqual(table_info['pagination_limit'], pagination_limit)

        if int(table_info['pagination_limit']) <= int((table_info['count']).replace(",", "")):
            self.assertEqual(table_info['pagination_limit'], table_records_count)

    def test068_archived_contact_not_retrieved(self):
        """
        Make sure that Archived contacts are n't appear in contacts drop down list

        LIMS-5829
        """
        api, payload = self.contacts_api.get_all_contacts(deleted=1)
        self.assertEqual(api['status'], 1)
        self.assertGreater(api['count'], 0)  # to make sure that there are archived contacts
        archived_contact = random.choice(api['contacts'])['name']
        self.info("Archived contact {}".format(archived_contact))
        self.base_selenium.click(element='orders:new_order')
        self.orders_page.sleep_medium()
        self.order_page.set_new_order()
        self.order_page.sleep_small()
        self.info('Asset that archived contact is not existing in the list')
        self.assertFalse(self.order_page.is_contact_existing(archived_contact))

    @parameterized.expand(['cancel_btn', 'close_btn'])
    def test069_close_testplan_popup(self, button):
        """
        Make sure the user can press on the cancel button to close the pop-up or from the ( x ) sign

        LIMS-4797
        """
        order, payload = self.orders_api.create_new_order()
        self.assertEqual(order['status'], 1)
        self.info('open the order record in the edit mode')
        self.orders_page.get_order_edit_page_by_id(id=order['order']['mainOrderId'])
        self.orders_page.sleep_small()
        self.base_selenium.click(element='order:testplan_popup_btn')
        if button == 'cancel_btn':
            self.base_selenium.wait_until_element_clickable(element='order:testplan_cancel_btn')
            self.base_selenium.click(element='order:testplan_cancel_btn')
        else:
            self.base_selenium.wait_until_element_clickable(element='order:testplan_close_btn')
            self.base_selenium.click(element='order:testplan_close_btn')

        self.assertTrue(self.base_selenium.check_element_is_not_exist(element='order:testplan_popup'))

    def test070_main_orders_only_should_be_displayed_in_the_orders_list(self):
        """
        Make sure that user sees the main orders only in the order list

        LIMS-5354
        """
        self.info('assert active table is displayed')
        table_records_count = len(self.order_page.result_table())
        self.assertGreater(table_records_count, 0)
        self.info('There is no duplications in the orders numbers')
        order = random.choice(self.orders_api.get_all_orders_json())
        order_no = order['orderNo']
        self.info('search by order No'.format(order_no))
        self.orders_page.filter_by_order_no(order_no)
        self.assertEqual(len(self.order_page.result_table()), 2)
        self.info('click on the random order from the list, Order table with add will be opened')
        self.orders_page.get_order_edit_page_by_id(order['orderId'])
        table_with_add = self.order_page.get_table_with_add()
        self.assertIsNotNone(table_with_add)
        self.info('duplicate the first suborder')
        self.order_page.duplicate_from_table_view()
        self.info('click on save button')
        self.order_page.save(save_btn='order:save_btn')
        self.info('Go back to the active table')
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(order_no)
        self.info('assert main order only displayed no duplicated rows for the suborders')
        self.assertFalse(self.order_page.check_suborders_appear())

    def test071_archive_multiple_orders(self):
        """
        Orders: Archive Approach: Make sure that you can select multiple records
        and then archive them at the same time

        LIMS-5364
        """
        self.info("select multiple orders and archive them")
        orders_data, rows = self.order_page.select_random_multiple_table_rows(element='orders:orders_table')
        self.assertTrue(self.orders_page.archive_selected_orders(check_pop_up=True))
        self.info("Navigate to archived orders table")
        self.orders_page.get_archived_items()
        for i in range(len(orders_data)):
            order_no = orders_data[i]['Order No.']
            self.info('asserting order with order number {} is successfully archived'.format(order_no))
            self.orders_page.filter_by_order_no(order_no)
            results = self.order_page.result_table()
            self.assertEqual(len(results), 2)
            self.assertIn(order_no.replace("'", ""), results[0].text.replace("'", ""))

    def test072_multiple_contacts_should_appear_in_active_table(self):
        """
        Multiple contacts should appear in active table

        LIMS-5773
        """
        response1, contact1 = self.contacts_api.create_contact()
        self.assertEqual(response1['status'], 1)
        response2, contact2 = self.contacts_api.create_contact()
        self.assertEqual(response2['status'], 1)
        contact_list = [contact1['name'], contact2['name']]
        testplan = TestPlanAPI().create_completed_testplan_random_data()
        order_no = self.order_page.create_multiple_contacts_new_order(
            contacts=contact_list,
            material_type=testplan['materialType'][0]['text'],
            article=testplan['selectedArticles'][0]['text'],
            test_plan=testplan['testPlan']['text'])
        self.orders_page.sleep_tiny()
        self.orders_page.get_orders_page()
        self.orders_page.sleep_small()
        self.order_page.filter_by_order_no(order_no)
        self.assertEqual(len(self.order_page.result_table()), 2)
        contacts = self.orders_page.get_the_latest_row_data()['Contact Name'].split(',\n')
        self.assertCountEqual(contact_list, contacts)

    def test073_create_new_existing_order_with_deleted_order_number(self):
        """
         create new order :make sure that user can't create a new order with
         existing order using a deleted order number

         LIMS-2430
        """
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1)
        order_no = payload[0]['orderNo']
        order_no_with_year = payload[0]['orderNoWithYear']
        order_id = response['order']['mainOrderId']
        self.info("checking that the order number appears in existing orders list before archive/delete")
        self.assertTrue(self.order_page.create_existing_order_check_no_in_suggestion_list(order_no_with_year))
        self.orders_api.archive_main_order(mainorder_id=order_id)
        self.info("checking that the archived order number doesn't appear in the existing order numbers list")
        self.assertFalse(self.order_page.create_existing_order_check_no_in_suggestion_list(order_no_with_year))
        self.orders_api.delete_main_order(mainorder_id=order_id)
        self.info("checking that the deleted order number doesn't appear in the existing order numbers list")
        self.assertFalse(self.order_page.create_existing_order_check_no_in_suggestion_list(order_no_with_year))
        testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.orders_page.get_orders_page()
        order_no = self.order_page.create_new_order(
            order_no=order_no_with_year,
            material_type=testplan['materialType'][0]['text'],
            article=testplan['selectedArticles'][0]['text'],
            test_plans=[testplan['testPlan']['text']])
        self.orders_page.sleep_tiny()
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(order_no_with_year)
        self.order_page.sleep_tiny()
        results = self.orders_page.result_table()
        self.assertEqual(len(results), 2)
        self.info('asserting the order with order number {} is created'.format(order_no))
        self.assertIn(order_no_with_year, results[0].text.replace("'", ""))

    # @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test074_create_existing_order_change_contact(self):
        """
         Create existing order then change the contact for this existing one,
         all old records with the same order number will update its contact.

         LIMS-4293

         LIMS-5818 - added departments assertion
        """
        self.info("create order with departments")
        res, payload = self.orders_api.create_order_with_department()
        self.assertEqual(res['status'], 1)
        order_no_with_year = payload[0]['orderNoWithYear']
        order_id = res['order']['mainOrderId']
        response, _ = self.orders_api.get_suborder_by_order_id(id=order_id)
        analysis_no = response['orders'][0]['analysis']
        self.info("create new contact with departments")
        response2, payload2 = ContactsAPI().create_contact_with_multiple_departments()
        self.assertEqual(response2['status'], 1)
        new_contact = response2['company']['name']
        new_contact_departments = [dep['text'] for dep in payload2['departments']]
        self.info("create existing order from order with No {}".format(order_no_with_year))
        self.order_page.create_existing_order_with_auto_fill(no=order_no_with_year)
        self.order_page.sleep_tiny()
        self.info("update contact to {}".format(new_contact))
        self.order_page.set_contact(contact=new_contact, remove_old=True)
        self.info('Asserting departments of selected contact are correctly displayed')
        _, departments_only_list = self.order_page.get_department_suggestion_lists(open_suborder_table=True)
        self.assertCountEqual(departments_only_list, new_contact_departments)
        self.order_page.save(save_btn='order:save_btn')
        self.orders_page.get_orders_page()
        self.order_page.sleep_tiny()
        self.order_page.navigate_to_analysis_tab()
        self.info('Asserting that contact has changed for this order')
        self.analyses_page.filter_by_analysis_number(analysis_no)
        results = self.analyses_page.get_the_latest_row_data()
        self.info('checking contact is updated to {}'.format(new_contact))
        self.assertEqual(new_contact, results['Contact Name'])
        self.info('checking old department removed{}'.format(new_contact))
        self.assertNotEqual(results['Departments'], response['orders'][0]['departments'])

    @attr(series=True)
    def test075_enter_long_method_should_be_in_multiple_lines_in_order_form(self):
        """
        In case you select the method to display and you entered long text in it,
        the method should display into multiple lines in the order form

        LIMS-6663
        """
        self.test_units_page = TstUnits()
        self.orders_page.sleep_tiny()
        self.test_units_page.get_test_units_page()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_configurations()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_testunit_name_configurations_options()
        self.test_units_page.select_option_to_view_search_with(view_search_options=['Method'])
        self.info(' create test unit with long method text ')
        api, payload = TestUnitAPI().create_test_unit_with_long_text()
        self.assertEqual(api['status'], 1, payload)
        self.info('go to orders page')
        self.order_page.get_orders_page()
        self.info('create new order with the test unit of long method text')
        self.order_page.create_new_order(save=False, material_type='Raw Material')
        self.order_page.set_test_unit(test_unit=payload['method'], remove_old=True)
        self.orders_page.save(save_btn='order:save_btn')
        self.info('assert method text appears in multiple lines')
        self.order_page.get_table_with_add()
        multiple_lines_properties = self.order_page.get_testunit_multiple_line_properties()
        self.assertEquals(multiple_lines_properties['textOverflow'], 'clip')
        self.assertEquals(multiple_lines_properties['lineBreak'], 'auto')

    # @attr(series=True)
    @parameterized.expand(['Name', 'Method', 'Unit', 'No'])
    def test076_search_with_test_unit_name_method(self, search_by):
        """
        Orders:Test unit search approach
        allow user to search with test unit name in the drop down list of the order form
        LIMS-6664
        allow user to search with test unit method in the drop down list of order form
        LIMS-6666
        allow user to search with test unit type in the drop down list of order form
        LIMS-6668
        allow user to search with test unit number in the drop down list of order form
        LIMS-6665

        """
        self.test_units_page = TstUnits()
        response, payload = TestUnitAPI().create_quantitative_testunit(unit="RandomUnit")
        self.assertEqual(response['status'], 1)
        self.test_units_page.get_test_units_page()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_configurations()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_testunit_name_configurations_options()
        self.test_units_page.select_option_to_view_search_with(view_search_options=[search_by])
        self.order_page.get_orders_page()

        if search_by == 'Name':
            testunit_search = payload['name']
        elif search_by == 'Method':
            testunit_search = payload['method']
        elif search_by == 'Unit':
            testunit_search = payload['unit']
        elif search_by == 'No':
            testunit_search = str(payload['number'])

        testunits = self.order_page.create_new_order_get_test_unit_suggetion_list(test_unit_name=testunit_search)

        self.info('checking {} field only is displayed'.format(search_by))
        self.assertGreater(len(testunits), 0)

    @parameterized.expand(['Quantitative', 'Qualitative', 'Quantitative MiBi'])
    @attr(series=True)
    def test077_test_unit_with_sub_and_super_unit_name_appears_in_unit_field_drop_down(self, type):
        """
        New: Test unit: Export: In case the unit field with sub & super,
        allow this to display in the unit field drop down list in the analysis form

        LIMS-6675
        """
        self.test_unit_api = TestUnitAPI()
        self.test_unit_api.set_name_configuration()
        if type == 'Quantitative':
            self.info('Create new Quantitative testunit')
            response, payload = self.test_unit_api.create_quantitative_testunit(unit='m[g]{o}')
        elif type == 'Qualitative':
            self.info('Create new Qualitative testunit')
            response, payload = self.test_unit_api.create_qualitative_testunit(unit='m[g]{o}')
        else:
            self.info('Create new Quantitative MiBi testunit')
            response, payload = self.test_unit_api.create_mibi_testunit(unit='m[g]{o}')

        self.assertEqual(response['status'], 1, 'test unit not created {}'.format(payload))
        self.info('go to orders page')
        self.order_page.get_orders_page()
        unit = self.order_page.create_new_order_get_test_unit_suggetion_list(
            material_type='', test_unit_name='m[g]{o}')
        self.assertIn("m[g]{o}", unit)

    @parameterized.expand(['sub_script', 'super_script'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-271")
    def test078_filter_testunit_by_scripts(self, value):
        """
         Make sure that user can filter by sub & super scripts in the filter drop down list

         LIMS-7447
         LIMS-7444
        """
        self.test_unit_api = TestUnitAPI()
        self.test_unit_api.set_name_configuration()
        if value == 'sub_script':
            api, testunit = self.test_unit_api.create_qualitative_testunit(unit='14[158]')
        else:
            api, testunit = self.test_unit_api.create_qualitative_testunit(unit='15{158}')
        self.assertEqual(api['status'], 1)
        unit = testunit['unit']
        self.orders_page.get_orders_page()
        self.order_page.sleep_small()
        self.base_selenium.scroll(False)
        self.orders_page.apply_filter_scenario(filter_element='orders:test_units_filter',
                                               filter_text=unit, field_type='drop_down')
        self.assertIsNotNone(
            self.base_selenium.is_text_included_in_drop_down_items(
                element='orders:test_units_filter', item_text=unit))

        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if unit in suborder['Test Units']:
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.open_child_table(source=results[i])

    @parameterized.expand(['order', 'sub_order'])
    def test079_order_options_icon(self, order):
        """
         orders :Make sure that when user click on options of order or suborder,
         it displays Four options: (Duplicate, COA, Mail, Archive)

            LIMS-5367
            LIMS-5360
        """
        self.info('select random order')
        random_row = self.orders_page.get_random_table_row(table_element='general:table')
        if order == 'sub_order':
            self.info('open child table')
            self.orders_page.open_child_table(source=random_row)
            self.info('get child table records')
            table_records = self.orders_page.result_table(element='general:table_child')
        else:
            table_records = self.orders_page.result_table(element='general:table')
        self.info('get values in options menu')
        values = self.orders_page.get_suborder_options(table_records[0]).split('\n')
        self.assertEqual(values, ['Duplicate', 'CoA', 'Mail', 'Archive'])

    @parameterized.expand(["duplicate", "edit"])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test080_Duplicate_or_update_order_with_test_plan_only(self, case):
        """
        Duplicate main order Approach: duplicate order with test plan

        LIMS-6849

        -When I edit order by deleting test plan message will appear
        (This Test Plan will be removed from the corresponding analysis )
        -make sure the corresponding analysis records created according to this update in test plan.

        LIMS-4269 case 1
        """
        self.info("create new order")
        response, payload = self.orders_api.create_new_order(testUnits=[])
        self.assertEqual(response['status'], 1, "order not created {}".format(payload))
        self.info("create completed test plan with article {}".format(payload[0]['article']))
        new_test_plan = TestPlanAPI().create_completed_testplan(
            material_type=payload[0]['materialType']['text'],
            formatted_article=payload[0]['article'])['testPlanEntity']['name']

        if case == 'duplicate':
            self.info("duplicate order with order no. {}".format(payload[0]['orderNo']))
            self.orders_page.filter_by_order_no(payload[0]['orderNo'])
            row = self.orders_page.result_table()[0]
            self.orders_page.click_check_box(row)
            self.orders_page.duplicate_main_order_from_table_overview()
        else:
            self.info("Edit order with order no. {}".format(payload[0]['orderNo']))
            self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])

        self.info("remove suborder test plan and update it to {}".format(new_test_plan))
        if case == 'duplicate':
            self.order_page.update_suborder(test_plans=[new_test_plan], remove_old=True)
        else:
            self.order_page.update_suborder(test_plans=[new_test_plan], remove_old=True,
                                            confirm_pop_up=True)

        self.order_page.save_and_wait(save_btn='order:save_btn')
        self.info('Get suborder data to check it updated correctly')
        suborder_after_refresh = self.order_page.get_suborder_data()['suborders'][0]
        suborder_testplan_after_refresh = suborder_after_refresh['testplans']
        self.info('Assert Test plan is: {}, and should be: {}'.format(
            suborder_testplan_after_refresh, [new_test_plan]))
        self.assertCountEqual(suborder_testplan_after_refresh, [new_test_plan])
        self.info('Getting analysis page to check the data in this child table')
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_analysis_number(suborder_after_refresh['analysis_no'])

        self.info('Assert analysis is updated with new test plan')
        analyses = self.analyses_page.get_the_latest_row_data()
        self.assertCountEqual([new_test_plan], analyses['Test Plans'].split(', '))

    @parameterized.expand(['main_order', 'sub_order'])
    def test081_Duplicate_order_and_cahange_article(self, case):
        """
        Duplicate from the main order Approach: Duplicate then change the article

        LIMS-6220

        Duplicate suborder Approach: Duplicate any sub order then change the article

        LIMS-6228
        """
        self.info('create order with test_unit and test_plan')
        api, payload = self.orders_api.create_new_order()
        self.assertEqual(api['status'], 1)
        test_unit_before_duplicate = payload[0]['testUnits'][0]['name']
        self.info('Order created with order No {}, article {}'.format(
            payload[0]['orderNo'], payload[0]['article']['text']))
        article = ArticleAPI().get_formatted_article_with_formatted_material_type(
            material_type=payload[0]['materialType'],
            avoid_article=payload[0]['article']['text'])
        self.order_page.filter_by_order_no(payload[0]['orderNo'])
        if case == 'main_order':
            self.info("duplicate main order no {}".format(payload[0]['orderNo']))
            self.order_page.duplicate_main_order_from_order_option()
        else:
            self.info("duplicate sub order of order no {}".format(payload[0]['orderNo']))
            self.orders_page.open_child_table(source=self.orders_page.result_table()[0])
            self.orders_page.duplicate_sub_order_from_table_overview()
        self.orders_page.sleep_tiny()
        self.info("update article to {}".format(article['name']))
        self.order_page.update_duplicated_order_article(article=article['name'])
        self.info("assert that test plan is empty and test unit is {}".format(
            test_unit_before_duplicate))
        self.assertFalse(self.order_page.get_test_plan())
        self.assertEqual(len([test_unit_before_duplicate]), len(self.order_page.get_test_unit()))
        self.order_page.save(save_btn='order:save')
        duplicated_order_no = self.order_page.get_no()
        self.info("navigate to active table")
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicated_order_no)
        duplicated_order_data = self.orders_page.get_child_table_data()[0]
        self.info('assert that duplicated order data is updated correctly')
        self.assertEqual(duplicated_order_data['Test Plans'], '-')
        self.assertEqual(duplicated_order_data['Article Name'].replace(" ", ""),
                         article['name'].replace(" ", ""))
        self.assertEqual(duplicated_order_data['Test Units'], test_unit_before_duplicate)

    def test082_edit_icon_of_main_order(self):
        """
         Make Sure that when user click on edit icon he will be redirect to the first step
         of the merged page that has the order data(Order Table with Add).

         LIMS-5371
        """
        self.info('choose random order and click on edit button')
        self.orders_page.sleep_tiny()
        order_data = self.orders_page.get_random_order()
        order_no = self.order_page.get_no(order_row=order_data)
        self.assertTrue(self.base_selenium.wait_element(element='orders:edit order header'))
        self.assertEqual(order_no, order_data['Order No.'])

    @skip("https://modeso.atlassian.net/browse/LIMSA-299")
    def test083_create_suborders_same_testunit(self):
        """
        Create 5 suborders with same test units ( single select ) and make sure 5 analysis
        records created successfully according to that.

        LIMS-4249
        LIMS-4251
        """
        response, payload = self.test_unit_api.get_all_test_units()
        random_testunit = random.choice(response['testUnits'])
        testunit_name = random_testunit['name']
        material_type = random_testunit['materialTypes'][0]
        if material_type == "All":
            material_type = ''
        self.order_page.create_new_order(material_type=material_type, test_units=[testunit_name],
                                         multiple_suborders=5, test_plans=[])
        order_id = self.order_page.get_order_id()
        suborders = self.orders_api.get_suborder_by_order_id(id=order_id)
        self.info('asserting api success')
        self.assertEqual(suborders[0]['status'], 1)
        analysis_numbers = [suborder['analysis'][0] for suborder in suborders[0]['orders']]
        self.info('asserting there are 5 suborders analysis triggered')
        self.assertEqual(len(analysis_numbers), 6)
        self.info('checking testunit for each suborder ')
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.open_filter_menu()
        for analysis in analysis_numbers:
            self.analyses_page.filter_by(
                filter_element='analysis_page:analysis_no_filter', filter_text=analysis, field_type='text')
            self.analyses_page.filter_apply()
            analysis_data = self.analyses_page.get_child_table_data(index=0)
            self.info('asserting testunit for suborder with analysis number {} is {}, main order testunit is {}'
                      .format(analysis, analysis_data[0]['Test Unit'], testunit_name))
            self.orders_page.open_child_table(source=self.analyses_page.result_table()[0])
            self.assertEqual(analysis_data[0]['Test Unit'], testunit_name)

    def test084_filter_by_changed_by(self):
        """
        New: Orders: Filter Approach: I can filter by changed by

        LIMS-3495
        """
        response, contact = self.contacts_api.create_contact()
        self.assertEqual(response['status'], 1)
        contact_list = [contact['name']]
        testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.orders_page.sleep_tiny()
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.info("Navigate to orders page and create new order")
        self.orders_page.get_orders_page()
        self.orders_page.sleep_small()
        order_no = self.order_page.create_multiple_contacts_new_order(
            contacts=contact_list,
            material_type=testplan['materialType'][0]['text'],
            article=testplan['selectedArticles'][0]['text'],
            test_plan=testplan['testPlan']['text'])
        self.orders_page.sleep_tiny()
        self.orders_page.get_orders_page()
        self.orders_page.sleep_small()
        self.info('filter by with user {}'.format(payload['username']))
        self.orders_page.apply_filter_scenario(
            filter_element='orders:changed_by',
            filter_text=payload['username'])

        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if payload['username'] == suborder['Changed By']:
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.close_child_table(source=results[i])

    def test085_update_contact_config_to_number_create_form(self):
        """
        Sample Management: Contact configuration approach: In case the user configures the
        contact field to display number this action should reflect on the order form step one

        LIMS-6626
        """
        self.info("set contact configuration to be searchable by number only")
        self.orders_api.set_contact_configuration_to_number_only()
        response, _ = self.contacts_api.get_all_contacts()
        self.assertEqual(response['status'], 1)
        self.assertGreaterEqual(response['count'], 1)
        random_contact = random.choice(response['contacts'])
        contact_no = random_contact['companyNo']
        contact_name = random_contact['name']
        testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.info("create new order with contact no {}".format(contact_no))
        self.order_page.create_new_order(contact=contact_no, save=False,
                                         material_type=testplan['materialType'][0]['text'],
                                         article=testplan['selectedArticles'][0]['text'],
                                         test_plans=[testplan['testPlan']['text']])
        self.info("assert that contact set to {}".format(str('No: ' + contact_no)))
        self.assertCountEqual(self.order_page.get_contact(), [str('No: ' + contact_no)])
        self.order_page.clear_contact()
        contact_name_result = self.base_selenium.get_drop_down_suggestion_list(element='order:contact',
                                                                               item_text=contact_name)
        self.info("assert that suggestion list of contact name {} is {}".format(contact_name, str('No: ' + contact_no)))

        self.assertEqual(contact_name_result[0], str('No: ' + contact_no))

    def test086_add_multiple_suborders_with_testplans_testunits(self):
        """
         New: Orders: table/create: Create 4 suborders from the table view with different
         test plans & units ( single select ) and make sure the correct corresponding analysis records.

         LIMS-4247
        """
        self.test_plan_api = TestPlanAPI()
        self.analysis_page = SingleAnalysisPage()
        testplans = []
        testunits_in_testplans = []
        for i in range(4):
            testplans.append(self.test_plan_api.create_completed_testplan_random_data())
            testunits_in_testplans.extend(self.test_plan_api.get_testunits_in_testplan_by_No(testplans[i]['number']))
        test_units = TestUnitAPI().get_testunits_with_material_type('All')
        test_units_names_only = [testunit['name'] for testunit in test_units]
        testunits = random.sample(test_units_names_only, 4)
        self.info("create new order")
        self.order_page.create_new_order(material_type=testplans[0]['materialType'][0]['text'],
                                         article=testplans[0]['selectedArticles'][0]['text'],
                                         test_plans=[testplans[0]['testPlan']['text']],
                                         test_units=[testunits[0]], save=False)

        for i in range(1, 4):
            self.info("add new suborder with test plan {} and test unit {}".
                      format(testplans[i]['testPlan']['text'], testunits[i]))
            self.order_page.create_new_suborder(material_type=testplans[i]['materialType'][0]['text'],
                                                article_name=testplans[i]['selectedArticles'][0]['text'],
                                                test_plans=[testplans[i]['testPlan']['text']],
                                                test_units=[testunits[i]])

        self.order_page.save(save_btn='order:save_btn')
        self.order_page.navigate_to_analysis_tab()
        self.assertEqual(self.analysis_page.get_analysis_count(), 4)
        for i in range(4):
            row = self.analysis_page.open_accordion_for_analysis_index(i)
            test_units = self.analysis_page.get_testunits_in_analysis(row)
            test_units_names = [name['Test Unit Name'].split(' ')[0] for name in test_units]
            self.assertEqual(len(test_units_names), 2)
            self.assertEqual(test_units_names[0], testunits_in_testplans[i])
            self.assertEqual(test_units_names[1], testunits[i])

    def test087_add_sub_order_with_multiple_testplans_only(self):
        """
        Any new suborder with multiple test plans should create one analysis record
        only with those test plans and test units that corresponding to them.

        LIMS-4276
        """
        self.info('create order with two testplans only')
        response, payload = self.orders_api.create_order_with_double_test_plans(only_test_plans=True)
        self.assertEqual(response['status'], 1)
        test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
        self.info("created order has test plans {} and {} ".format(test_plans[0], test_plans[1]))
        test_units = [TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][0]['number']),
                      TestPlanAPI().get_testunits_in_testplan_by_No(payload[0]['testPlans'][1]['number'])]

        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_order_no(payload[0]['orderNo'])
        self.assertEqual(len(self.analyses_page.result_table()) - 1, 1)
        analysis_data = self.analyses_page.get_the_latest_row_data()
        found_test_plans = analysis_data['Test Plans'].split(', ')
        self.assertEqual(len(found_test_plans), 2)
        suborder_data = self.analyses_page.get_child_table_data()
        found_test_units = [testunit['Test Unit'] for testunit in suborder_data]
        self.assertCountEqual(test_plans, found_test_plans)
        self.assertNotEqual(test_units, found_test_units)

    def test088_add_multiple_suborders_with_diff_departments(self):
        """
        Orders: table: Departments Approach: In case I created multiple suborders
        the departments should open drop down list with the options that I can
        select different departments in each one.

        LIMS-4258
        """
        self.info('create contact with multiple departments')
        response, payload = self.contacts_api.create_contact_with_multiple_departments()
        self.assertEqual(response['status'], 1, "contact with {} Not created".format(payload))
        department_list = [dep['text'] for dep in payload['departments']]
        self.info('create order with contact {} and first department {}'.
                  format(response['company']['name'], payload['departments'][0]['text']))
        order_response, order_payload = \
            self.orders_api.create_order_with_department_by_contact_id(
                response['company']['companyId'])
        self.assertEqual(order_response['status'], 1, "order with {} Not created".format(order_payload))
        self.info('edit order with No {}'.format(order_payload[0]['orderNo']))
        self.orders_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        self.order_page.sleep_tiny()
        self.order_page.create_new_suborder(material_type=order_payload[0]['materialType']['text'],
                                            article_name=order_payload[0]['article']['text'],
                                            test_plans=[order_payload[0]['testPlans'][0]['name']],
                                            test_units=[])
        self.order_page.sleep_tiny()
        self.info("get departments suggestion list for first suborder")
        _, department_suggestion_list1 = self.order_page.get_department_suggestion_lists(
            open_suborder_table=True, index=1)
        self.assertCountEqual(department_suggestion_list1, department_list)
        self.info("set department to {}".format(payload['departments'][1]['text']))
        self.order_page.set_departments(payload['departments'][1]['text'])
        self.order_page.sleep_tiny()
        self.order_page.create_new_suborder(material_type=order_payload[0]['materialType']['text'],
                                            article_name=order_payload[0]['article']['text'],
                                            test_plan=[order_payload[0]['testPlans'][0]['name']],
                                            test_units=[])
        self.order_page.sleep_tiny()
        self.info("get departments suggestion list for second suborder")
        _, department_suggestion_list2 = self.order_page.get_department_suggestion_lists(
            open_suborder_table=True, index=2)
        self.assertCountEqual(department_suggestion_list2, department_list)
        self.info("set department to {}".format(payload['departments'][2]['text']))
        self.order_page.set_departments(payload['departments'][2]['text'])
        self.order_page.save_and_wait('order:save_btn')
        self.info("assert that department of each suborder in department lis")
        suborder_data = self.order_page.get_suborder_data()["suborders"]
        for suborder in suborder_data:
            self.assertIn(suborder['departments'][0], department_list)

    def test089_order_of_test_units_in_analysis(self):
        """
        Orders: Ordering test units: Test units in the analysis section should display
        in the same order as in the order section
        LIMS-7415
        """
        self.info('create new order with 3 test units')
        response, payload = self.orders_api.create_order_with_test_units(3)
        self.info('get test units of order')
        order_testunits = [test_unit['name'] for test_unit in payload[0]['testUnits']]
        self.info('navigate to analysis tab')
        self.orders_page.navigate_to_analysis_active_table()
        self.info('filter by order number')
        self.analyses_page.filter_by_order_no(payload[0]['orderNoWithYear'])
        self.info('get child table data')
        table_data = self.analyses_page.get_child_table_data()
        analysis_testunits = [test_unit['Test Unit'] for test_unit in table_data]
        self.assertCountEqual(order_testunits, analysis_testunits)

    def test090_if_cancel_archive_order_no_order_suborder_analysis_will_archived(self):
        """
        [Archiving][MainOrder]Make sure that if user cancel archive order,
        No order or suborders or analysis of the order will be archived
        LIMS-5404
        """
        self.info('create order')
        self.order_page.create_new_order(material_type='Raw Material', save=False)
        self.info('dupliacte the suborder for 2 times')
        self.order_page.duplicate_from_table_view(number_of_duplicates=2)
        self.order_page.save(save_btn='order:save_btn')
        order_no = self.order_page.get_no()
        order_id = self.order_page.get_order_id()
        suborders_data, _ = self.orders_api.get_suborder_by_order_id(order_id)
        suborders = suborders_data['orders']
        self.assertEqual(3, len(suborders))
        analysis_no = []
        for suborder in suborders:
            analysis_no.append(suborder['analysis'][0])
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        self.info('click on arhcive then cancel popup')
        self.orders_page.archive_main_order_from_order_option(check_pop_up=True, confirm=False)
        table_records = self.orders_page.result_table(element='general:table')
        self.assertEqual(1, len(table_records) - 1)
        self.info('go to archived orders')
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        self.assertEqual(len(self.order_page.result_table()) - 1, 0)
        for i in range(0, len(analysis_no) - 1):
            self.base_selenium.refresh()
            self.orders_page.get_archived_items()
            self.orders_page.filter_by_analysis_number(filter_text=analysis_no[i])
            self.assertEqual(len(self.order_page.result_table()) - 1, 0)

    def test091_filter_by_analysis_number_with_year(self):
        """
         Filter: Analysis number format: In case the analysis number displayed with full year, I can filter by it
         LIMS-7425
        """
        self.info('open analysis configuration')
        self.analyses_page.open_analysis_configuration()
        self.info('set analysis number format to be Year before number')
        self.analyses_page.set_analysis_no_with_year()
        self.info('select random order and get analysis no of its suborder')
        orders, _ = self.orders_api.get_all_orders(limit=20)
        order = random.choice(orders['orders'])
        suborder, _ = self.orders_api.get_suborder_by_order_id(id=order['id'])
        analysis_no = suborder['orders'][0]['analysis'][0]
        self.info('navigate to analysis active table')
        self.orders_page.get_orders_page()
        self.orders_page.navigate_to_analysis_active_table()
        self.info('filter by analysis no')
        self.analyses_page.filter_by_analysis_number(filter_text=analysis_no)
        analysis = self.analyses_page.get_the_latest_row_data()
        result_analysis_no = analysis['Analysis No.']
        self.assertEqual(analysis_no, result_analysis_no)

    def test092_order_of_testunits_in_analysis_section(self):
        """
        Ordering test units Approach: In case I put test plans and test units at the same time , the order of
        the analysis section should be the test units of the test plans then the order test units

        LIMS-7416
        """
        response, _ = self.test_unit_api.get_all_test_units()
        random_testunit = random.choice(response['testUnits'])
        testunits_formated = [{'id': random_testunit['id'],
                               'name': random_testunit['name']}]
        res, payload = self.orders_api.create_new_order(testUnits=testunits_formated)

        testunit_of_test_plan = TestPlanAPI().get_testunits_in_testplan(payload[0]['testPlans'][0]['id'])
        testunits = [tu['name'] for tu in testunit_of_test_plan]
        testunits.append(testunits_formated[0]['name'])

        order_id = res['order']['mainOrderId']
        suborders = self.orders_api.get_suborder_by_order_id(id=order_id)[0]['orders']
        self.assertEqual(len(suborders), 1)
        analysis_number = suborders[0]['analysis'][0]
        self.order_page.get_orders_page()
        self.info('Navigating to analysis page')
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.filter_by_analysis_number(analysis_number)
        analysis_data = self.analyses_page.get_child_table_data(index=0)
        self.info('checking order of testunits in analysis section')
        test_units_list_in_analysis = [analysis['Test Unit'] for analysis in analysis_data]
        self.assertCountEqual(testunits, test_units_list_in_analysis)

    def test093_same_testunits_in_different_testplans(self):
        """
        Order: Add Same test units in different test plan
        LIMS-4354
        """
        self.test_plan_api = TestPlanAPI()
        self.info('create two identical test plans')
        tp1_pd = self.test_plan_api.create_completed_testplan_random_data()
        self.assertTrue(tp1_pd)
        testplan1_name = tp1_pd['testPlan']['text']
        # formated_testunit, formatted_article, formatted_material, material_type_id = self.test_plan_api.create_random_data_for_testplan()
        response2, testplan2 = self.test_plan_api.create_testplan(testUnits=tp1_pd['testUnits'],
                                                                  selectedArticles=tp1_pd['selectedArticles'],
                                                                  materialType=tp1_pd['materialType'],
                                                                  materialTypeId=tp1_pd['materialTypeId'])
        self.info('asserting api success')
        self.assertEqual(response2['message'], 'operation_success')
        testplan2_name = testplan2['testPlan']['text']

        testplans = testplan1_name + ', ' + testplan2_name
        self.order_page.get_orders_page()
        self.order_page.sleep_tiny()
        self.order_page.create_new_order(material_type=tp1_pd['materialType'][0]['text'],
                                         article=tp1_pd['selectedArticles'][0]['text'],
                                         test_plans=[testplan1_name, testplan2_name], test_units=[])
        self.order_page.sleep_tiny()
        order_id = self.order_page.get_order_id()
        suborders = self.orders_api.get_suborder_by_order_id(id=order_id)

        self.info('asserting api success')
        self.assertEqual(suborders[0]['status'], 1)
        analysis_number = [suborder['analysis'][0] for suborder in suborders[0]['orders']]
        self.info('asserting there is only one analysis for this order')
        self.assertEqual(len(analysis_number), 1)

        self.info('checking testunit for each testplan record ')
        self.order_page.get_orders_page()
        self.order_page.navigate_to_analysis_tab()
        self.analyses_page.sleep_tiny()
        self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
                                                 filter_text=analysis_number, field_type='text')
        analysis = self.analyses_page.get_the_latest_row_data()
        self.info('asserting status of analysis is open')
        self.assertEqual(analysis['Status'], 'Open')

        self.info('asserting correct testplans selected')
        self.assertEqual(analysis['Test Plans'], testplans)

        analysis_data = self.analyses_page.get_child_table_data(index=0)
        self.info('asserting 2 child records, one for each test plan')
        self.assertEqual(len(analysis_data), 2)
        self.orders_page.open_child_table(source=self.analyses_page.result_table()[0])
        for i in range(2):
            self.info('asserting testunit for testplan {} is {} = selected testunit {}'
                      .format(i + 1, analysis_data[i]['Test Unit'], tp1_pd['testUnits'][0]['name']))
            self.assertEqual(analysis_data[i]['Test Unit'], tp1_pd['testUnits'][0]['name'])

        self.orders_page.get_order_edit_page_by_id(order_id)
        self.info('Delete one of the testplans from the order ')
        self.order_page.sleep_tiny()
        self.info('click on first row and remove a testplan')
        self.order_page.open_suborder_edit()
        self.base_selenium.clear_items_in_drop_down(element='order:test_plan', confirm_popup=True, one_item_only=True)
        self.order_page.save(save_btn='order:save')
        self.order_page.get_orders_page()
        self.order_page.sleep_tiny()
        self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
                                                 filter_text=analysis_number, field_type='text')
        self.info('asserting correct testplans selected')
        self.order_page.sleep_tiny()
        self.assertEqual(self.analyses_page.get_the_latest_row_data()['Test Plans'], testplan1_name)
        analysis_data = self.analyses_page.get_child_table_data(index=0)
        self.info('asserting only 1 child record; as only one test plan is now selected')
        self.assertEqual(len(analysis_data), 1)
        self.orders_page.open_child_table(source=self.analyses_page.result_table()[0])
        self.info('asserting testunit for testplan2 is {} = selected testunit {}'
                  .format(analysis_data[0]['Test Unit'], tp1_pd['testUnits'][0]['name']))
        self.assertEqual(analysis_data[0]['Test Unit'], tp1_pd['testUnits'][0]['name'])

    def test094_select_large_number_of_test_units_in_one_testplan(self):
        """
          Orders: Test plan Approach: In case I select large number of test units in one test plan,
          they should display successfully in the pop up

          LIMS-4795
        """
        order = self.orders_api.get_order_with_multiple_sub_orders(no_suborders=2)
        self.info('create testplan with random data')
        testPlan = TestPlanAPI().create_completed_testplan_random_data(no_testunits=3)
        self.info(f'open order edit page : {order["id"]}')
        self.orders_page.get_order_edit_page_by_id(order['id'])
        testunit_names = []
        for testunit in testPlan['testUnits']:
            testunit_names.append(testunit['name'])
        self.info('update 2nd suborder')
        self.order_page.update_suborder(sub_order_index=1, material_type=testPlan['materialType'][0]['text'],
                                        articles=[testPlan['selectedArticles'][0]['text']],
                                        test_plans=[testPlan['testPlan']['text']],
                                        remove_old=True, confirm_pop_up=True)
        self.info('get testplan popup')
        results = self.order_page.get_testplan_pop_up(index=1)
        for result in results:
            if result['test_plan'] == testPlan['testPlan']['text']:
                for testunit in testunit_names:
                    self.assertIn(testunit, result['test_units'])
                  
    @parameterized.expand(['Name','No','Name:No'])
    def test095_change_contact_config(self,search_by):
        '''
         Orders: Contact configuration approach: In case the user
         configures the contact field to display name & number this action
         should reflect on the order active table
         LIMS-6632
        :param search_by:
        :return:
        '''
        self.contacts_page = Contacts()
        self.info('get random contact')
        contacts_response,_ = ContactsAPI().get_all_contacts(limit=10)
        self.assertEqual(contacts_response['status'], 1)
        payload = random.choice(contacts_response['contacts'])
        self.orders_page.open_order_config()
        self.info('change contact view by options')
        self.contacts_page.open_contact_configurations_options()
        if  search_by == 'Name':
            search_text = payload['name']
            result = payload['name']
            search_by = [search_by]
        elif search_by== 'No':
            search_text = 'No: '+ str(payload['companyNo'])
            result = str(payload['companyNo'])
            search_by = [search_by]
        elif search_by == 'Name:No':
            search_text = payload['name'] + ' No: ' + str(payload['companyNo'])
            search_by = search_by.split(':')
            result = payload['name']

        self.contacts_page.select_option_to_view_search_with(view_search_options=search_by)
        self.info('go to order active table')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_contact(filter_text=result)
        rows = self.orders_page.result_table()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
        self.info('assert contact appear in format {}'.format(search_by))
        self.assertEqual(order_data['Contact Name'],search_text)

    def test096_check_list_menu(self):
        """
          [Orders][Active table] Make sure that list menu will contain
          (COA,Archive , XSLX - Archived - Configurations) Only

          LIMS-5358
        """
        options = ['Duplicate', 'CoA', 'Archive', 'XSLX', 'Archived', 'Configurations']
        list = self.orders_page.get_right_menu_options()
        self.assertCountEqual(list, options)

    @parameterized.expand([('Name', 'Type'),
                           ('Unit', 'No'),
                           ('Quantification Limit', '')])
    @attr(series=True)
    def test097_test_unit_name_allow_user_to_filter_with_selected_two_options_order(self, search_view_option1,
                                                                                    search_view_option2):
        """
         Orders: Filter test unit Approach: Allow the search criteria in
         the drop down list in the filter section to be same as in the form

         LIMS-7411
        """
        self.test_units_page = TstUnits()
        self.test_units_page.get_test_units_page()
        self.test_units_page.open_configurations()
        self.test_units_page.open_testunit_name_configurations_options()
        self.test_units_page.select_option_to_view_search_with(
            view_search_options=[search_view_option1, search_view_option2])

        upperLimit = self.generate_random_number(lower=50, upper=100)
        lowerLimit = self.generate_random_number(lower=1, upper=49)
        self.info('Create new quantitative test unit with unit and quantification')
        response, payload = self.test_unit_api.create_quantitative_testunit(
            useSpec=False, useQuantification=True, quantificationUpperLimit=upperLimit,
            quantificationLowerLimit=lowerLimit, unit='m[g]{o}')
        self.assertEqual(response['status'], 1, payload)
        formated_tu, _ = TestUnitAPI().get_testunit_form_data(response['testUnit']['testUnitId'])
        test_unit = [{'id': formated_tu['testUnit']['id'], 'name': formated_tu['testUnit']['name']}]
        self.info('create new order created test unit number'.format(payload))
        res, order = self.orders_api.create_new_order(testUnits=test_unit)
        self.assertEqual(res['status'], 1, 'order not created with {}'.format(order))
        if search_view_option1 == 'Name' and search_view_option2 == 'Type':
            filter_text = payload['name']
        elif search_view_option1 == 'Unit' and search_view_option2 == 'No':
            filter_text = str(payload['number'])
        else:
            filter_text = str(payload['quantificationLowerLimit']) + '-' + str(payload['quantificationUpperLimit'])

        self.orders_page.get_orders_page()
        self.orders_page.sleep_tiny()
        self.orders_page.open_filter_menu()
        self.base_selenium.wait_element(element='orders:test_units_filter')
        self.orders_page.filter_by(filter_element='orders:test_units_filter', filter_text=filter_text)
        found_filter_text = self.base_selenium.get_text('orders:test_units_filter').replace("\n×", "")
        if search_view_option1 == 'Name' and search_view_option2 == 'Type':
            self.assertEqual(found_filter_text, payload['name'] + ': Quantitative')
        elif search_view_option1 == 'Unit' and search_view_option2 == 'No':
            self.assertEqual(found_filter_text, 'm[g]{o}: ' + str(payload['number']))
        else:
            self.assertEqual(found_filter_text, filter_text)

        self.orders_page.filter_apply()
        self.orders_page.sleep_tiny()
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if payload['name'] == suborder['Test Units']:
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.close_child_table(source=results[i])

    def test098_filter_configuration_fields(self):
        """
          Orders: Make sure that user can filter order TestUnit that exist
          on order only(TestUnit in Analysis not Included)

          LIMS-5379

          Orders: Filter Approach: Make sure that the user can filter from the
          default filter ( with status & dynamic fields )

          LIMS-5486
        """
        self.info("open filter menu")
        self.orders_page.open_filter_menu()
        self.info("open filter configuration")
        found_fields = self.orders_page.list_filter_feilds()
        self.info("fields in filter are {}".format(found_fields))
        required_fields = ['Analysis Results', 'Test Units', 'Material Type', 'Analysis No.',
                           'Departments', 'Test Plans', 'Changed By', 'Created On', 'Shipment Date',
                           'Test Date', 'Contact Name', 'Article Name', 'Order No.',
                           'Forwarding', 'Status']

        self.assertGreaterEqual(len(found_fields), len(required_fields))
        for field in required_fields:
            self.assertIn(field, found_fields)

    def test099_year_format_in_suborder_sheet(self):
        """
         Analysis number format: In case the analysis number displayed with full year,
         this should reflect on the export file

         LIMS-7424

         Order number format: In case the order number displayed with full year,
         this should reflect on the export file

         LIMS-7423
        """
        self.info('select random order')
        order = random.choice(self.orders_api.get_all_orders_json())
        order_no = order['orderNo']
        self.assertIn('-2020', order_no)
        response, _ = self.orders_api.get_suborder_by_order_id(order['orderId'])
        self.assertEqual(response['status'], 1)
        analysis_no = response['orders'][0]['analysis'][0]
        self.assertIn('-2020', analysis_no)
        self.orders_page.filter_by_order_no(order_no)
        row = self.orders_page.result_table()[0]
        self.assertTrue(row)
        self.orders_page.click_check_box(source=row)
        self.order_page.download_xslx_sheet()
        self.info('Comparing the downloaded  order ')
        values = self.order_page.sheet.iloc[0].values
        fixed_sheet_row_data = self.reformat_data(values)
        self.assertIn(order_no, fixed_sheet_row_data)
        self.assertIn(analysis_no, fixed_sheet_row_data)

    def test100_create_multiple_suborders_with_testplans_testunits(self):
        """
         New: Orders: table view: Create Approach: when you create suborders with multiple
         test plans & units select the corresponding analysis that triggered according to that.

         LIMS-4256
        """
        self.test_plan_api = TestPlanAPI()
        self.analysis_page = SingleAnalysisPage()
        self.info("generate data of first suborder")
        test_units = TestUnitAPI().get_testunits_with_material_type('All')
        test_units_names_only = [testunit['name'] for testunit in test_units]
        first_suborder_test_units = random.sample(test_units_names_only, 2)

        self.info("generate data of second suborder")
        first_test_plan = self.test_plan_api.create_completed_testplan_random_data()
        second_test_plan = self.test_plan_api.create_completed_testplan(
            material_type=first_test_plan['materialType'][0]['text'],
            formatted_article=first_test_plan['selectedArticles'][0])
        testplans = [first_test_plan, second_test_plan]
        testplans_of_second_suborder = [first_test_plan['testPlan']['text'], second_test_plan['testPlanEntity']['name']]
        second_suborder_test_units = []
        for i in range(2):
            second_suborder_test_units.extend(
                self.test_plan_api.get_testunits_in_testplan_by_No(testplans[i]['number']))

        self.info("generate data of third suborder")
        third_suborder_test_units = random.sample(test_units_names_only, 3)

        self.info("create new order")

        self.order_page.create_new_order(material_type=testplans[0]['materialType'][0]['text'],
                                         article=testplans[0]['selectedArticles'][0]['text'],
                                         test_units=first_suborder_test_units,
                                         test_plans=[], save=False)

        self.order_page.create_new_suborder(material_type=testplans[0]['materialType'][0]['text'],
                                            article_name=testplans[0]['selectedArticles'][0]['text'],
                                            test_plans=testplans_of_second_suborder, test_units=[])

        self.order_page.create_new_suborder(material_type=testplans[0]['materialType'][0]['text'],
                                            article_name=testplans[0]['selectedArticles'][0]['text'],
                                            test_plans=[], test_units=third_suborder_test_units)

        self.order_page.save(save_btn='order:save_btn')
        self.order_page.navigate_to_analysis_tab()
        self.assertEqual(self.analysis_page.get_analysis_count(), 3)
        for i in range(3):
            row = self.analysis_page.open_accordion_for_analysis_index(i)
            test_units = self.analysis_page.get_testunits_in_analysis(row)
            test_units_names = [name['Test Unit Name'].split(' ')[0] for name in test_units]
            if i == 0:
                self.assertCountEqual(test_units_names, first_suborder_test_units)
            elif i == 1:
                self.assertCountEqual(test_units_names, second_suborder_test_units)
            else:
                self.assertCountEqual(test_units_names, third_suborder_test_units)

    def test101_choose_test_plans_without_test_units(self):
        """
        Orders: Create: Orders Choose test plans without test units

        LIMS-4350
        """
        self.test_plan_api = TestPlanAPI()
        response, payload = self.orders_api.create_order_with_multiple_suborders_double_tp()
        self.assertEqual(response['message'], 'created_success')
        order_no = response['order']['orderNo']
        suborders_data, _ = self.orders_api.get_suborder_by_order_id(response['order']['mainOrderId'])
        self.assertEqual(len(suborders_data['orders']), 3)
        analysis_no = [suborder['analysis'][0] for suborder in suborders_data['orders']]
        test_units = []
        for i in range(3):
            for j in range(2):
                test_units.extend(self.test_plan_api.get_testunits_in_testplan(payload[i]['testPlans'][j]['id']))
        test_units_names = [tu['name'] for tu in test_units]
        self.orders_page.sleep_tiny()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        self.orders_page.sleep_tiny()
        suborders_data = self.order_page.get_child_table_data()
        analysis_no_list = [suborder['Analysis No.'].replace("'", "") for suborder in suborders_data]
        self.info('assert the order table has been updated')
        self.assertCountEqual(analysis_no, analysis_no_list)
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_order_no(filter_text=order_no)
        analysis_data = self.base_selenium.get_rows_cells_dict_related_to_header()
        self.assertEqual(len(analysis_data), 3)
        found_analysis_no = [analysis['Analysis No.'].replace("'", "") for analysis in analysis_data]
        self.info('assert the analysis table has been updated')
        self.assertCountEqual(analysis_no, found_analysis_no)
        for i in range(3):
            child_data = self.orders_page.get_child_table_data(index=2 - i)
            self.orders_page.sleep_tiny()
            test_units = [item['Test Unit'] for item in child_data]
            self.assertCountEqual(test_units, test_units_names[i * 2:(i * 2) + 2])

    def test102_multiple_suborders(self):
        """
        Orders: Table with add: Allow user to add any number of the suborders records not only 5 suborders

        LIMS-5220
        """
        response, payload = self.orders_api.create_order_with_multiple_suborders(no_suborders=10)
        self.assertEqual(response['status'], 1)
        testPlan = TestPlanAPI().create_completed_testplan_random_data()
        self.assertTrue(testPlan)
        self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
        suborder_table = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.assertEqual(len(suborder_table), 10)
        self.order_page.create_new_suborder(material_type=testPlan['materialType'][0]['text'],
                                            article_name=testPlan['selectedArticles'][0]['text'],
                                            test_plans=[testPlan['testPlan']['text']], test_units=[])
        self.order_page.sleep_tiny()
        self.order_page.save(save_btn='order:save_btn')
        self.info('duplicate 5 suborders')
        self.order_page.duplicate_from_table_view(number_of_duplicates=5)
        self.order_page.save_and_wait(save_btn='order:save_btn')
        table_after2 = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.assertEqual(len(table_after2), 16)
        self.order_page.navigate_to_analysis_tab()
        self.assertEqual(SingleAnalysisPage().get_analysis_count(), 16)

    def test103_create_order_with_test_plans_with_same_name(self):
        """
        Orders: Create Approach: Make sure In case you create two test plans with the same name
        and different materiel type, the test units that belongs to them displayed correct in
        analysis step two

        LIMS-6296
        """
        test_plans_list = TestPlanAPI().create_double_completed_testplan_same_name_diff_material()
        self.assertTrue(test_plans_list)
        test_units_list = [tu['testUnits'][0]['name'] for tu in test_plans_list]
        update_suborder = self.orders_api.get_suborders_data_of_test_plan_list(test_plans_list)
        self.info("create order with two suborders")
        response, payload = self.orders_api.create_order_with_multiple_suborders(
            no_suborders=2, suborders_fields=update_suborder)
        self.assertEqual(response['message'], 'created_success')
        self.info("open edit page of order {}".format(response['order']['mainOrderId']))
        self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
        self.info("Navigate to analysis step 2")
        self.order_page.navigate_to_analysis_tab()
        self.analysis_page = SingleAnalysisPage()
        self.info("assert that only 2 analysis triggered")
        self.assertEqual(self.analysis_page.get_analysis_count(), 2)
        for i in range(2):
            row = self.analysis_page.open_accordion_for_analysis_index(i)
            test_units = self.analysis_page.get_testunits_in_analysis(row)
            self.assertEqual(len(test_units), 1)
            test_units_name = test_units[0]['Test Unit Name'].split(' ')[0]
            self.assertEqual(test_units_name, test_units_list[i])
             
    @parameterized.expand(['update_a_field', 'no_updates'])
    def test104_edit_order_page_then_overview(self, edit_case):
        """
        Orders: Popup should appear when editing then clicking on overview without saving <All data will be lost>
        LIMS-6814

        Orders: No popup should appear when clicking on overview without changing anything
        LIMS-6821
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        self.info('edit order with No {}'.format(random_order['orderNo']))
        self.order_page.filter_by_order_no(random_order['orderNo'])
        row = self.orders_page.result_table()[0]
        self.order_page.open_edit_page(row=row)
        if edit_case == 'update_a_field':
            self.info('update the contact field')
            self.order_page.set_contact(remove_old=True)
        self.order_page.click_overview()
        if edit_case == 'update_a_field':
            self.assertIn('All data will be lost', self.order_page.get_confirmation_pop_up_text())
            self.assertTrue(self.order_page.confirm_popup(check_only=True))
        else:
            self.assertFalse(self.order_page.confirm_popup(check_only=True))
            self.info('asserting redirection to active table')
            self.assertEqual(self.order_page.orders_url, self.base_selenium.get_url())

    def test105_check_analysis_result_active_table(self):
        """
        [Orders][Active Table][Suborders] Make Sure that Next to the analysis result an icon will be displayed
        upon click a dialog will open containing (the current child table of analysis page ) table with the test units
        in it and it's specs and values.

        LIMS-5373
        """
        self.single_analysis_page = SingleAnalysisPage()
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1)
        order_id = response['order']['mainOrderId']
        testplan_info = TestPlanAPI().get_testplan_form_data(id=payload[0]['testPlans'][0]['id'])
        testplan_specs = '{}-{}'.format(testplan_info['specifications'][0]['lowerLimit'],
                                        testplan_info['specifications'][0]['upperLimit'])
        testunit_list = [testplan_info['specifications'][0]['name'], payload[0]['testUnits'][0]['name']]
        testunit_info = self.test_unit_api.get_testunit_form_data(id=payload[0]['testUnits'][0]['id'])
        testunit_specs = '{}-{}'.format(testunit_info[0]['testUnit']['lowerLimit'],
                                        testunit_info[0]['testUnit']['upperLimit'])
        specs_list = [testplan_specs, testunit_specs]

        self.orders_page.get_order_edit_page_by_id(order_id)
        self.info('navigate to analysis tab')
        self.order_page.navigate_to_analysis_tab()
        value = self.single_analysis_page.set_testunit_values(save=False)
        self.base_selenium.scroll()
        self.info('change validation options')
        analysis_result = self.single_analysis_page.change_validation_options()
        self.order_page.get_orders_page()
        self.order_page.filter_by_order_no(filter_text=payload[0]['orderNo'])
        suborders = self.order_page.get_child_table_data()
        self.info('asserting analysis result is displayed correctly')
        for suborder in suborders:
            if analysis_result == 'Conform W. Rest.':
                self.assertEqual(suborder['Analysis Results'], 'Conform With Restrictions (1)')
            else:
                self.assertEqual(suborder['Analysis Results'], analysis_result)
        self.info('asserting icon exists beside analysis results')
        self.assertTrue(self.base_selenium.check_element_is_exist(element='order:analysis_result_icon'))
        self.base_selenium.click(element='order:analysis_result_icon')
        testunits_table = self.base_selenium.get_rows_cells_dict_related_to_header(
            table_element='order:analysis_testunits_table')
        self.order_page.sleep_tiny()
        self.base_selenium.click(element='order:close_testunits_table')
        displayed_testunits = [testunit_record['Test Unit'] for testunit_record in testunits_table]
        displayed_testunits_specs = [testunit_record['Specifications'] for testunit_record in testunits_table]
        self.info('asserting all selected testunits are displayed')
        self.assertCountEqual(displayed_testunits, testunit_list)
        self.info('asserting all selected testunits specification are displayed')
        self.assertCountEqual(displayed_testunits_specs, specs_list)