from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.order_page import SubOrders
from ui_testing.pages.orders_page import Orders
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from parameterized import parameterized
from unittest import skip
import random


@skip('https://modeso.atlassian.net/browse/LIMSA-389')
class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.suborder_table = SubOrders()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.order_page.get_orders_page()
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()
        self.orders_api.set_filter_configuration()

    def test001_duplicate_sub_order_table_with_add(self):
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
        self.info('create new order')
        response, payload = self.orders_api.create_new_order()
        order_number = payload[0]['orderNoWithYear']
        suborders = self.orders_api.get_suborder_by_order_id(response['order']['mainOrderId'])[0]['orders']
        contacts = [contact['text'] for contact in payload[0]['contact']]

        self.orders_page.filter_by_order_no(order_number)
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
        self.info("duplicate first suborder from table view")
        self.suborder_table.duplicate_from_table_view(index_to_duplicate_from=0)
        after_duplicate_order = self.suborder_table.get_suborder_data()
        self.info("make sure that the new order has same order No and contact")
        self.assertEqual(order_number, after_duplicate_order['orderNo'].replace("'", ""))
        self.assertCountEqual(contacts, after_duplicate_order['contacts'])
        self.info("save the duplicated order")
        self.order_page.save(save_btn='orders:save_order')
        self.info("go back to the table view, and assert that duplicated suborder added to child table")
        self.order_page.get_orders_page()
        self.order_page.filter_by_order_no(order_number)
        suborder_data = self.order_page.get_child_table_data()
        self.assertTrue(len(suborder_data), len(suborders) + 1)
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_analysis_number(suborder_data[0]['Analysis No.'])
        analysis_result = self.analyses_page.get_the_latest_row_data()['Analysis No.'].replace("'", "")
        self.assertEqual(suborder_data[0]['Analysis No.'].replace("'", ""), analysis_result)

    def test002_duplicate_main_order_change_contact(self):
        """
        Duplicate from the main order Approach: Duplicate then change the contact
        LIMS-6222
        """
        res, _ = self.contacts_api.create_contact()
        self.assertEqual(res['status'], 1)
        new_contact = res['company']['name']
        self.info('create new order')
        response, payload = self.orders_api.create_new_order()
        order_number = payload[0]['orderNoWithYear']
        self.info("duplicate order No {}".format(order_number))
        self.order_page.filter_by_order_no(order_number)
        duplicated_order_no = f"{self.orders_api.generate_random_number(999, 999999)}-{self.orders_api.get_current_year()}"
        self.order_page.duplicate_main_order_from_order_option(duplicated_order_no)
        self.order_page.set_contacts(contacts=[new_contact], remove_old=True)
        self.order_page.save(save_btn='order:save')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicated_order_no)
        self.assertEqual(len(self.orders_page.result_table())-1, 1)
        order = self.orders_page.get_the_latest_row_data()
        self.assertEqual(order['Contact Name'], new_contact)

    def test003_duplicate_main_order_with_multiple_contacts(self):
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
        duplicated_order_no = f"{self.orders_api.generate_random_number(999, 999999)}-{self.orders_api.get_current_year()}"
        self.order_page.duplicate_main_order_from_order_option(duplicated_order_no)
        self.order_page.save(save_btn='order:save')
        self.info("navigate to orders' active table and check that duplicated suborder found")
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicated_order_no)
        duplicated_order_data = self.orders_page.get_the_latest_row_data()
        duplicated_contacts = duplicated_order_data['Contact Name'].split(',\n')
        self.assertCountEqual(duplicated_contacts, contacts)

    def test004_duplicate_sub_order_with_multiple_contacts(self):
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
        self.orders_page.navigate_to_analysis_active_table()
        for analysis in analyses_numbers:
            self.analyses_page.filter_by_analysis_number(analysis)
            analysis_data = self.analyses_page.get_the_latest_row_data()
            duplicated_contacts_in_analyses = analysis_data['Contact Name'].split(',\n')
            self.assertEqual(len(duplicated_contacts_in_analyses), 3)
            self.assertCountEqual(duplicated_contacts, contacts)

    @parameterized.expand(['main_order', 'sub_order'])
    def test005_duplicate_order_and_change_article(self, case):
        """
        Duplicate from the main order Approach: Duplicate then change the article

        LIMS-6220

        Duplicate suborder Approach: Duplicate any sub order then change the article

        LIMS-6228
        """
        self.info('create order with test_unit and test_plan')
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1)
        test_unit_before_duplicate = payload[0]['testUnits'][0]['name']
        self.info('Order created with order No {}, article {}'.format(
            payload[0]['orderNo'], payload[0]['article']['text']))
        article = ArticleAPI().get_formatted_article_with_formatted_material_type(
            material_type=payload[0]['materialType'],
            avoid_article=payload[0]['article']['text'])
        self.order_page.filter_by_order_no(payload[0]['orderNo'])
        if case == 'main_order':
            self.info("duplicate main order no {}".format(payload[0]['orderNo']))
            duplicated_order_no = f"{self.orders_api.generate_random_number(999, 999999)}-{self.orders_api.get_current_year()}"
            self.order_page.duplicate_main_order_from_order_option(duplicated_order_no)
            self.suborder_table.open_suborder_edit_mode()
        else:
            self.info("duplicate sub order of order no {}".format(payload[0]['orderNo']))
            self.orders_page.open_child_table(source=self.orders_page.result_table()[0])
            self.orders_page.duplicate_sub_order_from_table_overview()
        self.orders_page.sleep_tiny()
        self.info("update article to {}".format(article['name']))
        self.suborder_table.remove_article()
        self.suborder_table.set_article(article=article['name'])
        self.order_page.save(save_btn='order:save')
        self.orders_page.sleep_tiny()
        self.info("assert that test plan is empty and test unit is {}".format(test_unit_before_duplicate))
        self.assertEqual(self.suborder_table.get_test_plans(), None)
        self.assertCountEqual([test_unit_before_duplicate], self.suborder_table.get_test_units())
        duplicated_order_no = self.order_page.get_order_no()
        self.info("navigate to active table")
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicated_order_no)
        duplicated_order_data = self.orders_page.get_child_table_data()[0]
        self.info('assert that duplicated order data is updated correctly')
        self.assertEqual(duplicated_order_data['Test Plans'], '-')
        self.assertEqual(duplicated_order_data['Article Name'], article['name'])
        self.assertEqual(duplicated_order_data['Test Units'], test_unit_before_duplicate)

    @parameterized.expand(["main_order", "sub_order"])
    def test006_duplicate_order_and_change_material_type(self, case):
        """
        duplicate the main order then change the materiel type
        LIMS-6219
        """
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1)
        old_material = payload[0]['materialType']['text']
        self.info('get completed test plan with different material type')
        new_suborder_data = TestPlanAPI().get_suborder_data_with_different_material_type(old_material)
        self.order_page.filter_by_order_no(payload[0]['orderNo'])
        if case == "main_order":
            self.info('duplicate the main order')
            duplicated_order_no = f"{self.orders_api.generate_random_number(999, 999999)}-{self.orders_api.get_current_year()}"
            self.order_page.duplicate_main_order_from_order_option(duplicated_order_no)
        else:
            self.order_page.get_child_table_data()
            self.info("duplicate first sub order of order {} from suborder's options".format(payload[0]['orderNo']))
            self.order_page.duplicate_sub_order_from_table_overview()
        self.info('change material type of first suborder')
        self.suborder_table.set_material_type(material_type=new_suborder_data['material_type'])
        self.order_page.sleep_tiny()
        self.info('Make sure that article, test unit, and test plan are empty')
        self.assertEqual(self.suborder_table.get_article(), None)
        self.assertEqual(self.suborder_table.get_test_units(), None)
        self.assertEqual(self.suborder_table.get_test_plans(), None)
        if case == "main_order":
            duplicated_order_number = self.order_page.get_order_no()
            self.info('order to be duplicated is {}, new order no is {}'.
                      format(payload[0]['orderNo'], duplicated_order_number))
            self.assertNotEqual(payload[0]['orderNo'], duplicated_order_number)
        self.info('Update article, test unit and test plan')
        self.suborder_table.set_article(article=new_suborder_data['article'])
        self.suborder_table.set_test_plans(test_plans=[new_suborder_data['test_plan']])
        self.suborder_table.set_test_units(test_units=[new_suborder_data['test_unit']])
        self.info('duplicated order material is {}, article {}, test_unit {} and test_plan {}'.
                  format(new_suborder_data['material_type'], new_suborder_data['article'],
                         new_suborder_data['test_unit'], new_suborder_data['test_plan']))
        self.order_page.save(save_btn='order:save_btn', sleep=True)
        self.info("navigate to orders' page to make sure that order duplicated correctly with selected data")
        self.order_page.get_orders_page()
        if case == 'main_order':
            self.orders_page.filter_by_order_no(duplicated_order_number)
        else:
            self.order_page.filter_by_order_no(payload[0]['orderNo'])
        suborder_data = self.order_page.get_child_table_data()[0]
        self.info('Make sure that suborder data is correct')
        self.assertEqual(suborder_data['Material Type'], new_suborder_data['material_type'])
        self.assertEqual(suborder_data['Article Name'], new_suborder_data['article'])
        self.assertEqual(suborder_data['Test Units'], new_suborder_data['test_unit'])
        self.assertEqual(suborder_data['Test Plans'], new_suborder_data['test_plan'])

    def test007_Duplicate_sub_order_with_multiple_testplans_and_testunits_delete_approach(self):
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

    @parameterized.expand(['change', 'add'])
    def test008_duplicate_main_order_with_testPlan_and_testUnit_edit_both(self, case):
        """
        Duplicate from the main order Approach: Duplicate then change the test units & test plans
        LIMS-6221
        Duplicate from the main order Approach: Duplicate then update test unit/plan by deleting
        any test plan & test unit
        LIMS-6841
        Duplicate from the main order Approach: Duplicate by adding test unit & plan
        LIMS-6231
        """
        self.info('create order with test plan and test unit')
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1, response)
        new_test_plan_data = TestPlanAPI().create_completed_testplan(
            material_type=payload[0]['materialType']['text'], formatted_article=payload[0]['article'])
        new_test_plan = new_test_plan_data['testPlanEntity']['name']
        new_test_unit = new_test_plan_data['specifications'][0]['name']

        self.info("duplicate order No {} ".format(payload[0]['orderNo']))
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        self.info("duplicate main order")
        duplicated_order_no = f"{self.orders_api.generate_random_number(999, 999999)}-{self.orders_api.get_current_year()}"
        self.order_page.duplicate_main_order_from_order_option(duplicated_order_no)
        self.order_page.save(save_btn='order:save')
        self.assertIn("duplicateMainOrder", self.base_selenium.get_url())
        self.order_page.sleep_medium()
        self.info("duplicated order No is {}".format(duplicated_order_no))
        if case == 'add':
            self.info("add test plan {} and test unit {} to duplicated order".format(new_test_plan, new_test_unit))
            self.suborder_table.update_suborder(test_plans=[new_test_plan], test_units=[new_test_unit])
        else:
            self.info("update test plan to {} and test unit to {}".format(new_test_plan, new_test_unit))
            self.suborder_table.update_suborder(test_plans=[new_test_plan], test_units=[new_test_unit],
                                                remove_old=True, confirm_pop_up=True)
        import ipdb; ipdb.set_trace()
        self.order_page.save(save_btn='order:save')
        self.info("navigate to active table")
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(duplicated_order_no)
        self.assertEqual(len(self.orders_page.result_table())-1, 1)
        duplicated_suborder_data = self.order_page.get_child_table_data()[0]
        if case == 'change':
            self.info("assert that test unit updated to {}, test plan {}".format(
                new_test_unit, new_test_plan))
            self.assertEqual(duplicated_suborder_data['Test Units'], new_test_unit)
            self.assertEqual(duplicated_suborder_data['Test Plans'], new_test_plan)
        else:
            self.info("assert that test unit {}, test plan {} added to duplicated order".format(
                new_test_unit, new_test_plan))
            self.assertIn(new_test_unit, duplicated_suborder_data['Test Units'])
            self.assertIn(new_test_plan, duplicated_suborder_data['Test Plans'])

        self.info("navigate to analysis page")
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_order_no(duplicated_order_no)
        analyses = self.analyses_page.get_the_latest_row_data()
        if case == 'add':
            self.assertIn(new_test_plan, analyses['Test Plans'].replace("'", ""))
        else:
            self.assertEqual(new_test_plan, analyses['Test Plans'].replace("'", ""))
        child_data = self.analyses_page.get_child_table_data()
        test_units = [test_unit['Test Unit'] for test_unit in child_data]
        self.assertIn(new_test_unit, test_units)

    def test009_duplicate_sub_order_with_testPlan_and_testUnit_change_both(self):
        """
        Duplicate suborder Approach: Duplicate any sub order then change the units & test plans
        (remove them and put another ones )

        LIMS-6229
        """
        self.info('create order with test plan and test unit')
        response, payload = self.orders_api.create_new_order()
        self.assertEqual(response['status'], 1)
        self.info('order created with payload {}'.format(payload))
        new_test_plan_data = TestPlanAPI().create_completed_testplan(
            material_type=payload[0]['materialType']['text'], formatted_article=payload[0]['article'])
        new_test_plan = new_test_plan_data['testPlanEntity']['name']
        new_test_unit = new_test_plan_data['specifications'][0]['name']
        self.info("duplicate order No {} ".format(payload[0]['orderNo']))
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        self.info("duplicate sub order with one copy only")
        self.orders_page.open_child_table(source=self.orders_page.result_table()[0])
        self.orders_page.duplicate_sub_order_from_table_overview()
        self.info("update test plan to {} and test unit to {}".format(new_test_plan, new_test_unit))
        self.suborder_table.update_suborder(test_plans=[new_test_plan], test_units=[new_test_unit],
                                            remove_old=True, article=None)
        self.order_page.save(save_btn='order:save')
        self.info("navigate to analysis active table")
        self.order_page.get_orders_page()
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_order_no(payload[0]['orderNo'])
        analyses = self.analyses_page.get_the_latest_row_data()
        self.assertEqual(new_test_plan, analyses['Test Plans'].replace("'", ""))
        child_data = self.analyses_page.get_child_table_data()
        test_units = [test_unit['Test Unit'] for test_unit in child_data]
        self.assertIn(new_test_unit, test_units)

    def test010_Duplicate_sub_order_with_multiple_testplans_and_testunits_add_approach(self):
        """
        Duplicate suborder Approach: Duplicate any sub order then add test unit & test plan

        LIMS-6232
        """
        self.info('create order data multiple test plans and test units')
        response, payload = self.orders_api.create_order_with_double_test_plans()
        self.assertEqual(response['status'], 1, payload)
        test_plans = [payload[0]['testPlans'][0]['testPlan']['text'], payload[0]['testPlans'][1]['testPlan']['text']]
        test_units = [payload[0]['testUnits'][0]['name'], payload[0]['testUnits'][1]['name']]
        self.info("get new completed test plan with article {} and material_type {}".format(
            payload[0]['article']['text'], payload[0]['materialType']['text']))

        new_test_plan_data = TestPlanAPI().create_completed_testplan(
            material_type=payload[0]['materialType']['text'], formatted_article=payload[0]['article'])
        test_plan = new_test_plan_data['testPlanEntity']['name']
        test_unit = new_test_plan_data['specifications'][0]['name']

        test_plans.append(test_plan)
        test_units.append(test_unit)

        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        self.info("duplicate the sub order of order {} from suborder's options".format(payload[0]['orderNo']))
        self.orders_page.get_child_table_data()
        self.orders_page.duplicate_sub_order_from_table_overview()
        self.suborder_table.set_test_plans(test_plans=[test_plan])
        self.suborder_table.set_test_units(test_units=[test_unit])
        self.order_page.save(save_btn='order:save', sleep=True)
        self.orders_page.sleep_small()
        analysis_no = self.suborder_table.get_suborder_data()['suborders'][1]['analysis_no']
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

    def test011_duplicate_main_order_with_testPlans_and_testUnits(self):
        """
        Duplicate main order Approach: duplicate order with test plan & test units
        LIMS-4353
        """
        self.info('create order with multiple test plans and test units')
        response, payload = self.orders_api.create_order_with_double_test_plans()
        self.assertEqual(response['status'], 1, payload)
        test_plans = [payload[0]['selectedTestPlans'][0]['name'], payload[0]['selectedTestPlans'][1]['name']]
        test_units = [testunit['name'] for testunit in payload[0]['selectedTestUnits']]
        test_units.extend(TestPlanAPI().get_testunits_in_testplan(payload[0]['testPlans'][0]['testPlan']['id']))
        test_units.extend(TestPlanAPI().get_testunits_in_testplan(payload[0]['testPlans'][1]['testPlan']['id']))
        self.info("created order has test plans {} ".format(test_plans))
        self.info("created order has test units {} ".format(test_units))
        self.orders_page.filter_by_order_no(payload[0]['orderNo'])
        self.info("duplicate order no {}".format(payload[0]['orderNo']))
        duplicated_order_no = f"{self.orders_api.generate_random_number(999, 999999)}-{self.orders_api.get_current_year()}"
        self.order_page.duplicate_main_order_from_order_option(duplicated_order_no)
        self.orders_page.sleep_small()
        self.order_page.save(save_btn='order:save', sleep=True)
        self.assertNotEqual(duplicated_order_no, payload[0]['orderNo'])
        self.info("navigate to analysis page  and make sure duplicated order created with same data")
        self.order_page.get_orders_page()
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_order_no(duplicated_order_no)
        self.assertEqual(len(self.analyses_page.result_table())-1, 1)
        duplicated_test_plans = self.analyses_page.get_the_latest_row_data()['Test Plans'].split(', ')
        self.assertEqual(duplicated_test_plans, test_plans)
        duplicated_suborder_data = self.order_page.get_child_table_data()
        duplicated_test_units = [testunit['Test Unit'] for testunit in duplicated_suborder_data]
        # we need to assert not equal because the test units in the child table included the test units
        # in the orders section and in the test plans it self
        self.assertNotEqual(test_units, duplicated_test_units)

    @parameterized.expand(["duplicate", "edit"])
    def test012_Duplicate_or_update_order_with_test_plan_only(self, case):
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
            self.suborder_table.update_suborder(test_plans=[new_test_plan], remove_old=True)
        else:
            self.suborder_table.update_suborder(test_plans=[new_test_plan], remove_old=True,
                                                confirm_pop_up=True)

        self.order_page.save_and_wait(save_btn='order:save_btn')
        self.info('Get suborder data to check it updated correctly')
        suborder_after_refresh = self.suborder_table.get_suborder_data()['suborders'][0]
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
