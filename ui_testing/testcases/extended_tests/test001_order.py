from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.header_page import Header
from ui_testing.pages.login_page import Login
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from ui_testing.pages.analysis_page import SingleAnalysisPage
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.article_api import ArticleAPI
from ui_testing.pages.my_profile_page import MyProfile
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.base_api import BaseAPI
from parameterized import parameterized
from datetime import date
from nose.plugins.attrib import attr
from unittest import skip
import random


class OrdersWithoutArticleTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.test_plan_api = TestPlanAPI()
        self.general_utilities = GeneralUtilitiesAPI()
        self.set_authorization(auth=BaseAPI().AUTHORIZATION_RESPONSE)
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()
        self.header_page = Header()
        article_enabled = self.general_utilities.is_article_enabled()
        if article_enabled:
            self.info('go to Modules Configurations')
            self.header_page.get_modules_config_page()
            self.header_page.disable_article_option()
        self.header_page.sleep_tiny()
        self.order_page.get_orders_page()

    def tearDown(self):
        article_enabled = self.general_utilities.is_article_enabled()
        if not article_enabled:
            self.header_page.get_modules_config_page()
            self.header_page.disable_article_option()
        return super().tearDown()

    @attr(series=True)
    def test001_create_order_without_article(self):
        """
        orders without articles: check that user can create order without article

        LIMS-3253
        """
        created_testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.assertTrue(created_testplan)
        formatted_material = created_testplan['materialType'][0]
        created_testunit = self.test_unit_api.create_qualitative_testunit(selectedMaterialTypes=[formatted_material])
        self.info('asserting article is not found in orders active table configuration')
        child_table_header = self.orders_page.navigate_to_child_table_configuration()
        self.assertNotIn('Article Name', child_table_header)
        self.orders_page.open_child_table(self.orders_page.result_table()[0])
        header_row = self.base_selenium.get_table_head_elements(element='general:table_child')
        displayed_headers = [h.text for h in header_row]
        self.info('asserting article is not displayed in orders table')
        self.assertNotIn('Article Name', displayed_headers)
        order_no, testunits, testplans = self.order_page.create_new_order(
            material_type=formatted_material['text'], test_plans=[created_testplan['testPlan']['text']],
            test_units=[created_testunit[1]['name']], article=None, check_testunits_testplans=True)

        self.info('asserting article field is not displayed in new order page')
        fields = self.base_selenium.get_table_head_elements(element='order:suborder_table')
        fields_text = [f.text for f in fields]
        self.assertNotIn('Article: *', fields_text)

        self.info('asserting All displayed testunits are loaded correctly according to '
                  'selected material type {}'.format(formatted_material['text']))
        testunit_materials = self.test_unit_api.get_testunits_material_types(testunits)
        self.assertTrue(any(material in ['All', formatted_material['text']] for material in testunit_materials))

        self.info('asserting All displayed testplans are loaded correctly according to '
                  'selected material type {}'.format(formatted_material['text']))
        testplan_materials = self.test_plan_api.get_testplans_material_types(testplans)
        self.assertTrue(any(material in ['All', formatted_material['text']] for material in testplan_materials))

        self.order_page.sleep_tiny()
        self.order_page.get_orders_page()
        self.order_page.sleep_tiny()
        self.order_page.filter_by_order_no(filter_text=order_no)
        latest_order_data = \
            self.base_selenium.get_row_cells_dict_related_to_header(row=self.order_page.result_table()[0])
        self.info('asserting the order is successfully created')
        self.assertEqual(order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

    @attr(series=True)
    def test002_create__order_from_existing_order_without_article(self):
        """
         Orders without articles: when creating a new order from existing order,
         all data should be loaded, without article

         LIMS-3254
        """
        created_testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.assertTrue(created_testplan)
        formatted_material = created_testplan['materialType'][0]
        created_testunit = self.test_unit_api.create_qualitative_testunit(selectedMaterialTypes=[formatted_material])
        material_type = formatted_material['text']
        self.info('create order from an existing one')
        self.orders_page.sleep_tiny()
        order_no = self.order_page.create_existing_order_with_auto_fill()
        self.assertFalse(self.base_selenium.check_element_is_exist(element='order:article'))
        self.info('switch to material type {}'.format(material_type))
        self.order_page.set_material_type(material_type=material_type)
        self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
        testunits = self.base_selenium.get_drop_down_suggestion_list(element='order:test_unit',
                                                                     item_text=' ')
        testplans = self.base_selenium.get_drop_down_suggestion_list(element='order:test_plan',
                                                                     item_text=' ')

        self.info('asserting All displayed testunits are loaded correctly according to '
                  'selected material type {}'.format(material_type))
        testunit_materials = self.test_unit_api.get_testunits_material_types(testunits)
        self.assertTrue(any(material in ['All', material_type] for material in testunit_materials))

        self.info('asserting All displayed testplans are loaded correctly according to '
                  'selected material type {}'.format(material_type))
        testplan_materials = self.test_plan_api.get_testplans_material_types(testplans)
        self.assertTrue(any(material in ['All', material_type] for material in testplan_materials))

        self.order_page.set_test_unit(created_testunit[1]['name'])
        self.order_page.set_test_plan(created_testplan['testPlan']['text'])
        self.order_page.save(save_btn='order:save_btn')
        self.info('assert order is created successfully')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        results = self.order_page.result_table()[0].text
        self.assertIn(order_no.replace("'", ""), results.replace("'", ""))

    @parameterized.expand(['cancel', 'confirm'])
    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMS-3255')
    def test003_edit_material_type_order_without_article(self, case):
        """
        Orders without articles: When editing an order with test plan, the form should  be opened without article

        LIMS-3255 (edit material type case)
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        response, payload = self.orders_api.get_suborder_by_order_id(random_order['orderId'])
        self.assertEqual(response['status'], 1)
        first_suborder = response['orders'][0]
        new_material = random.choice(
            self.general_utilities.get_formatted_material_types_without_duplicate(first_suborder['materialType']))
        material_type = new_material['name']
        new_suborder = self.orders_api.get_suborder_valid_data({'id': new_material['id'], 'text': new_material['name']})
        self.assertTrue(new_suborder)
        new_testunit_list = [new_suborder['tp_attached_tu'], new_suborder['Test Unit']]
        self.info('edit material type of first suborder of order No {}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['orderId'])
        first_suborder_before_edit = self.order_page.get_suborder_data()['suborders'][0]
        self.order_page.open_suborder_edit(sub_order_index=0)
        self.info('update material type from {} to {}'.format(first_suborder['materialType'],
                                                              new_suborder['Material Type']))
        self.order_page.set_material_type(material_type=material_type)
        pop_up = self.base_selenium.find_element(element='general:confirmation_pop_up')
        self.assertIn("All analysis created with this order and test plan will be deleted", pop_up.text)
        if case == 'cancel':
            self.order_page.confirm_popup(force=False)
            self.base_selenium.refresh()
            self.order_page.sleep_tiny()
            suborder_after_cancel = self.order_page.get_suborder_data()['suborders'][0]
            self.assertCountEqual(first_suborder_before_edit, suborder_after_cancel)
        else:
            self.order_page.confirm_popup()
            self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
            self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
            self.order_page.set_test_plan(new_suborder['Test Plan'])
            self.order_page.set_test_unit(new_suborder['Test Unit'])
            self.order_page.save(save_btn='order:save_btn')
            self.info('assert that analysis updated is created successfully')
            self.orders_page.get_orders_page()
            self.orders_page.navigate_to_analysis_active_table()
            self.analyses_page.filter_by_analysis_number(first_suborder['analysis'][0])
            data_found = self.analyses_page.get_the_latest_row_data()
            self.assertEqual(data_found['Test Plans'], new_suborder['Test Plan'])
            child_data = self.analyses_page.get_child_table_data()
            testunit_list = [tu['Test Unit'] for tu in child_data]
            self.assertCountEqual(testunit_list, new_testunit_list)

    @parameterized.expand(['cancel', 'confirm'])
    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMS-3255')
    def test004_edit_testplan_order_without_article(self, case):
        """
        Orders without articles: When editing an order with test plan, the form should  be opened without article

        LIMS-3255 (edit test plan case)
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        response, payload = self.orders_api.get_suborder_by_order_id(random_order['orderId'])
        self.assertEqual(response['status'], 1)
        first_suborder = response['orders'][0]
        article_id = ArticleAPI().get_article_id(article_no=first_suborder['articleNo'],
                                                 article_name=first_suborder['article'])
        formatted_article = {'id': article_id, 'text': first_suborder['article']}
        new_test_plan = TestPlanAPI().create_completed_testplan(
            material_type=first_suborder['materialType'],
            formatted_article=formatted_article)['testPlanEntity']['name']
        self.info('edit test plan of first suborder of order No {}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['orderId'])
        first_suborder_before_edit = self.order_page.get_suborder_data()['suborders'][0]
        self.info('update test plan from {} to {}'.format(first_suborder['testPlans'], new_test_plan))
        self.order_page.update_suborder(test_plans=[new_test_plan], remove_old=True)
        if case == 'cancel':
            self.order_page.cancel(force=False)
            self.base_selenium.refresh()
            self.order_page.sleep_tiny()
            suborder_after_cancel = self.order_page.get_suborder_data()['suborders'][0]
            self.assertCountEqual(first_suborder_before_edit, suborder_after_cancel)
        else:
            self.order_page.save_and_wait(save_btn='order:save_btn')
            self.assertEqual(self.order_page.get_test_plan(), new_test_plan)
            self.info('assert that analysis updated is created successfully')
            self.orders_page.get_orders_page()
            self.orders_page.navigate_to_analysis_active_table()
            self.analyses_page.filter_by_analysis_number(first_suborder['analysis'][0])
            data_found = self.analyses_page.get_the_latest_row_data()
            self.assertEqual(data_found['Test Plans'], new_test_plan)

    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMS-3255')
    def test005_add_testplan_order_without_article(self):
        """
        Orders without articles: When editing an order with test plan, the form should  be opened without article

        LIMS-3255 (Add test plan case)
        """
        data = TestPlanAPI().create_multiple_test_plan_with_same_article(no_of_testplans=2)
        formatted_testplan = {'testPlan': {'id': data['testPlans'][0]['id'],
                                           'text': data['testPlans'][0]['name']}}
        response, payload = self.orders_api.create_new_order(
            testPlans=[formatted_testplan], testUnits=[], materialType=data['material_type'],
            materialTypeId=data['material_type']['id'], article=data['article'], articleId=data['article']['id'])
        self.assertEqual(response['status'], 1)
        test_units = [TestPlanAPI().get_testunits_in_testplan(data['testPlans'][0]['id'])[0][ 'name'],
                      TestPlanAPI().get_testunits_in_testplan(data['testPlans'][1]['id'])[0][ 'name']]
        self.info("open edit page of order no {}".format(response['order']['orderNo']))
        self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
        self.info('Add test plan {}'.format(data['testPlans'][1]['name']))
        self.order_page.update_suborder(test_plans=[data['testPlans'][1]['name']], remove_old=False)
        self.order_page.save(save_btn='order:save_btn')
        self.order_page.open_suborder_edit()
        self.assertCountEqual([data['testPlans'][0]['name'], data['testPlans'][1]['name']],
                              self.order_page.get_test_plan())
        self.info('assert that analysis updated is created successfully')
        self.order_page.navigate_to_analysis_tab()
        self.assertEqual(SingleAnalysisPage().get_analysis_count(), 1)
        row = SingleAnalysisPage().open_accordion_for_analysis_index(index=0)
        analysis_data = SingleAnalysisPage().get_testunits_in_analysis(row)
        test_units_in_analysis = [tu['Test Unit Name'].split(' ()')[0] for tu in analysis_data]
        self.assertCountEqual(test_units_in_analysis, test_units)

    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMS-3255')
    def test006_edit_order_number_without_article(self):
        """
         Orders without articles: When editing an order with test plan, the form should  be opened without article

         LIMS-3255 (update order number)
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        self.info('edit order with No {}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        order_url = self.base_selenium.get_url()
        self.info('order_url : {}'.format(order_url))
        new_number = self.generate_random_string()
        self.order_page.set_no(new_number)
        self.order_page.save(save_btn='order:save_btn')
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_SMALL)
        current_number = self.order_page.get_no().replace("'", "")
        self.info('Assert {} (current_number) == {} (new_number)'.format(current_number, new_number))
        self.assertEqual(current_number, new_number)

    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMS-3255')
    def test007_update_contact_order_without_article(self):
        """
         Orders without articles: When editing an order with test plan, the form should  be opened without article

         LIMS-3255 (update contact)
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        self.info('edit order with No {}'.format(random_order['orderNo']))
        self.orders_page.get_order_edit_page_by_id(random_order['id'])
        order_url = self.base_selenium.get_url()
        self.info('order_url : {}'.format(order_url))
        new_contact = self.order_page.set_contact(remove_old=True)
        self.order_page.save(save_btn='order:save_btn')
        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_SMALL)
        current_contact = self.order_page.get_contact()
        self.info('Assert {} (current_contact) == {} (new_contact)'.format(current_contact, new_contact))
        self.assertEqual(current_contact, new_contact)



class OrdersExtendedTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.test_plan_api = TestPlanAPI()
        self.general_utilities = GeneralUtilitiesAPI()
        self.header_page = Header()
        self.my_profile_page = MyProfile()
        self.set_authorization(auth=BaseAPI().AUTHORIZATION_RESPONSE)
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()
        self.order_page.get_orders_page()
        self.selected_language = 'EN'

    def tearDown(self):
        if self.selected_language == 'DE':
            self.my_profile_page.get_my_profile_page()
            self.my_profile_page.chang_lang(lang='EN')
        return super().tearDown()

    @parameterized.expand(['EN', 'DE'])
    @attr(series=True)
    def test003_new_fields_are_displayed_in_order_child_table(self, lang):
        """
        Orders : child table: check that new fields of "Forwarding" , "Report sent by", "validation date" and
        "validation by"have been added to order's child table in both EN and DE

        LIMS-7714
        LIMS-7715
        """
        if lang == 'EN':
            required_headers = ['Forwarding', 'Report sent by', 'Validation by', 'Validation date']
        else:
            self.selected_language = 'DE'
            self.my_profile_page.get_my_profile_page()
            self.my_profile_page.chang_lang(lang='DE')
            self.orders_page.get_orders_page()
            required_headers = ['Versand', 'Bericht Versand duch', 'Probenfreigabe Datum', 'Probenfreigabe durch']

        self.orders_page.open_child_table(self.orders_page.result_table()[0])
        header_row = self.base_selenium.get_table_head_elements(element='general:table_child')
        displayed_child_headers = [h.text for h in header_row]
        displayed_Configuration_headers = self.orders_page.navigate_to_child_table_configuration()
        for header in required_headers:
            self.info('asserting {} is displayed '.format(header))
            self.assertIn(header, displayed_child_headers)
            self.assertIn(header, displayed_Configuration_headers)

    @attr(series=True)
    def test004_check_validation_date_validation_by(self):
        """
         Orders: Validation date & Validation by : check that when user update the validation date &
         the validation by, the update should reflect on order's child table

         LIMS-7729
        """
        today = date.today()
        current_date = today.strftime("%d.%m.%Y")
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.single_analysis_page = SingleAnalysisPage()
        self.login_page = Login()
        self.info("create new order and update its validation option to be conform")
        order_response, order_payload = self.orders_api.create_new_order()
        self.assertEqual(order_response['status'], 1, order_payload)
        order_no = order_payload[0]['orderNo']
        self.info('edit order with No {}'.format(order_no))
        self.orders_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        self.order_page.sleep_small()
        self.info('navigate to analysis tab')
        self.order_page.navigate_to_analysis_tab()
        self.single_analysis_page.set_testunit_values()
        self.info('change validation options to conform')
        self.single_analysis_page.change_validation_options(text='Conform')
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        suborders_data = self.order_page.get_child_table_data(index=0)
        self.info('assert validation by is set correctly')
        self.assertEqual(suborders_data[0]['Validation by'], self.base_selenium.username)
        self.assertEqual(suborders_data[0]['Validation date'], current_date)
        self.info('go to analysis table and assert validation by and validation options'
                  ' are set correctly as in order active table')
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_analysis_number(suborders_data[0]['Analysis No.'])
        analysis_data = self.analyses_page.get_the_latest_row_data()
        self.assertEqual(suborders_data[0]['Validation by'], analysis_data['Validation by'])
        self.assertEqual(suborders_data[0]['Validation date'], analysis_data['Validation date'])
        self.info("Logout then login again using new user {}".format(payload['username']))
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.orders_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        self.info('change validation options so validation by is changed to {}', payload['username'])
        self.order_page.navigate_to_analysis_tab()
        self.single_analysis_page.change_validation_options(text='Approved')
        self.orders_page.get_orders_page()
        self.orders_page.navigate_to_order_active_table()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        suborders_after = self.order_page.get_child_table_data(index=0)
        self.assertEqual(suborders_after[0]['Validation by'], payload['username'])
        self.assertEqual(suborders_after[0]['Validation date'], current_date)
