from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.testunits_page import TstUnits
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.order_page import Order
from ui_testing.pages.login_page import Login
from api_testing.apis.users_api import UsersAPI
from unittest import skip
from parameterized import parameterized
from nose.plugins.attrib import attr
import random


class TestUnitsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.test_unit_page = TstUnit()
        self.test_units_page = TstUnits()
        self.test_plan = TstPlan()
        self.article_api = ArticleAPI()
        self.test_unit_api = TestUnitAPI()
        self.set_authorization(auth=self.article_api.AUTHORIZATION_RESPONSE)
        self.test_unit_api.set_configuration()
        self.test_unit_page.get_test_units_page()

    @attr(series=True)
    #@skip('waiting for API deleting')
    def test036_archive_quantifications_limit_field(self):
        """
        User can archive the quantification limits field from the configuration section if not used.
        "Archive-allowed"
        LIMS-4164
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.archive_quantification_limit_field()
        if not self.test_unit_page.is_field_in_use():
            self.assertFalse(
                self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
            self.test_unit_page.get_archived_fields_tab()

            self.assertTrue(self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
            self.test_unit_page.get_test_units_page()
            self.test_unit_page.click_create_new_testunit()
            self.test_unit_page.set_testunit_type(testunit_type='Quantitative')
            self.assertFalse(self.base_selenium.check_element_is_exist(element='test_unit:use_quantification'))

    @attr(series=True)
    def test037_restore_quantifications_limit_field(self):
        """
        User can archive the quantification limits field from the configuration section if not used.

        "Restore"
        LIMS-4164
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.archive_quantification_limit_field()
        if not self.test_unit_page.is_field_in_use():
            self.test_unit_page.restore_quantification_limit_field()
            self.assertFalse(
                self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
            self.test_unit_page.get_active_fields_tab()
            self.assertTrue(self.base_selenium.check_element_is_exist('test_unit:configuration_testunit_useQuantification'))
            self.test_unit_page.get_test_units_page()
            self.test_unit_page.click_create_new_testunit()
            self.test_unit_page.set_testunit_type(testunit_type='Quantitative')
            self.assertTrue(self.base_selenium.check_element_is_exist(element='test_unit:use_quantification'))

    @attr(series=True)
    def test038_test_unit_name_is_mandatory(self):
        """
        New: Test unit: Configuration: Test unit Name Approach: Make the test units field
        as as mandatory field (This mean you can't remove it )

        LIMS- 5651
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.assertTrue(self.test_unit_page.check_all_options_of_search_view_menu())

    @parameterized.expand(['Name', 'Method', 'Type', 'No'])
    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMSA-382')
    def test039_test_unit_name_allow_user_to_search_with_selected_options_testplan(self, search_view_option):
        """
        New: Test Unit: Configuration: Test unit Name Approach: Allow user to search with
        (name, number, type, method) in the drop down list of the test plan for.

        LIMS- 6422
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        old_values = self.test_unit_page.select_option_to_view_search_with(view_search_options=[search_view_option])
        self.info('Create new testunit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('new testunit created with number  {}'.format(payload['number']))
        self.info('get random In Progrees test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['name'])
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=str(payload['number']))
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['method'])

        if search_view_option == 'Name':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option == 'Type':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option == 'Method':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option == 'No':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)

    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMSA-382')
    def test040_test_unit_name_search_default_options_name_type_in_testplan(self):
        """
        New: Test unit: Configuration: Test units field Approach: Allow name & type
        to display by default in the test plan form In case I select them from the
        test unit configuration

        LIMS-6423
        """
        # in set_configuration() I set search to be by name and type so I don't need to add this steps here
        self.info('Create new test unit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('new test unit created with number  {}'.format(payload['number']))
        self.info('get random In Progress test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.sleep_small()
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['name'])
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=str(payload['number']))
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['method'])
        self.assertTrue(is_name_exist)
        self.assertFalse(is_number_exist)
        self.assertTrue(is_type_exist)
        self.assertFalse(is_method_exist)

    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMSA-382')
    def test041_test_unit_name_view_method_option_multiple_line_in_testplan(self):
        """
        New: Test Unit: Configuration: Test unit Name Approach: In case you select
        the method to display and you entered long text in it, the method should
        display into multiple lines (test plan)

        LIMS-6424
        """
        self.info('Generate random data for update')
        new_random_method = self.generate_random_string() + \
                            self.generate_random_string() + \
                            self.generate_random_string()

        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.test_unit_page.select_option_to_view_search_with(view_search_options=['Method'])
        self.info('Create new testunit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit(method=new_random_method)
        self.assertEqual(response['status'], 1, payload)
        self.info('new testunit created with number  {}'.format(payload['number']))
        self.info('get random In Progrees test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.set_test_unit(test_unit=new_random_method)
        multiple_lines_properties = self.test_plan.get_testunit_in_testplan_title_multiple_line_properties()
        self.assertEquals(multiple_lines_properties['textOverflow'], 'clip')
        self.assertEquals(multiple_lines_properties['lineBreak'], 'auto')

    @parameterized.expand([('Name', 'Type'),
                           ('Name', 'Method'),
                           ('Name', 'No'),
                           ('Type', 'Method'),
                           ('Type', 'No'),
                           ('Method', 'No')])
    @attr(series=True)
    @skip('https://modeso.atlassian.net/browse/LIMSA-382')
    def test042_test_unit_name_allow_user_to_search_with_selected_two_options_testplan(self, search_view_option1,
                                                                                       search_view_option2):
        """
        New: Test Unit: Configuration: Test unit Name Approach: Allow user to search with
        (name, number, type, method) in the drop down list of the analysis for

        LIMS- 6426
        """
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.test_unit_page.select_option_to_view_search_with(
            view_search_options=[search_view_option1, search_view_option2])
        self.info('Create new test unit with qualitative and random generated data')
        response, payload = self.test_unit_api.create_qualitative_testunit()
        self.assertEqual(response['status'], 1, payload)
        self.info('new test unit created with number  {}'.format(payload['number']))
        self.info('get random In Progress test plan')
        test_plan = random.choice(TestPlanAPI().get_inprogress_testplans())
        self.assertTrue(test_plan, 'No test plan selected')
        self.info('Navigate to test plan edit page')
        self.test_plan.get_test_plan_edit_page_by_id(test_plan['id'])
        self.test_plan.sleep_small()
        is_name_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['name'])
        is_number_exist = self.test_plan.search_test_unit_not_set(test_unit=str(payload['number']))
        is_type_exist = self.test_plan.search_test_unit_not_set(test_unit='Qualitative')
        is_method_exist = self.test_plan.search_test_unit_not_set(test_unit=payload['method'])

        if search_view_option1 == 'Name' and search_view_option2 == 'Type':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'Name' and search_view_option2 == 'Method':
            self.assertTrue(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option1 == 'Name' and search_view_option2 == 'No':
            self.assertTrue(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'Type' and search_view_option2 == 'Method':
            self.assertFalse(is_name_exist)
            self.assertFalse(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertTrue(is_method_exist)
        elif search_view_option1 == 'Type' and search_view_option2 == 'No':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertTrue(is_type_exist)
            self.assertFalse(is_method_exist)
        elif search_view_option1 == 'Method' and search_view_option2 == 'No':
            self.assertFalse(is_name_exist)
            self.assertTrue(is_number_exist)
            self.assertFalse(is_type_exist)
            self.assertTrue(is_method_exist)

    @attr(series=True)
    def test049_filter_by_testunit_changed_by(self):
        """
        New: Test units: Filter Approach: Make sure you can filter by changed by

        LIMS-6428
        """
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_units_page.get_test_units_page()
        new_name = self.generate_random_string()
        method = self.generate_random_string()
        test_unit_no = self.test_unit_page.create_qualitative_testunit(name=new_name, method=method)
        self.test_unit_page.save_and_wait()
        self.assertTrue(test_unit_no, 'Test unit not created')
        self.info('New unit is created successfully with number: {}'.format(test_unit_no))
        self.test_units_page.sleep_tiny()
        test_unit_found = self.test_units_page.filter_by_user_get_result(payload['username'])
        self.assertTrue(test_unit_found)

    @parameterized.expand([('Name', 'Type'),
                           ('Name', 'Method'),
                           ('Name', 'No'),
                           ('Type', 'Method'),
                           ('Type', 'No'),
                           ('No', 'Method'),
                           ('Unit', 'No'),
                           ('Quantification Limit', '')
                           ])
    @attr(series=True)
    def test051_test_unit_name_allow_user_to_search_with_selected_two_options_order(self, first_search_option,
                                                                                    second_search_option):
        """
        Test Unit: Configuration: Test units Name Approach: When the user select any two options
        from the test unit configuration, this action should reflect on the order form

        LIMS-6672

        Orders: Default filter test unit Approach: Allow the search criteria in the drop down list
        in the filter section to be same as in the form

        LIMS-7414
        """
        options_exist = {}
        order_page = Order()
        self.test_unit_page.open_configurations()
        self.test_unit_page.open_testunit_name_configurations_options()
        self.test_unit_page.select_option_to_view_search_with(
            view_search_options=[first_search_option, second_search_option])

        self.info('create new quantitative test unit with unit and quantification')
        response, payload = self.test_unit_api.create_quantitative_testunit(
            useSpec=False, useQuantification=True, unit='m[g]{o}',
            quantificationUpperLimit=self.generate_random_number(lower=50, upper=100),
            quantificationLowerLimit=self.generate_random_number(lower=1, upper=49))
        self.assertEqual(response['status'], 1, payload)
        quantification_limit = '{}-{}'.format(payload['quantificationLowerLimit'],
                                              payload['quantificationUpperLimit'])
        self.info('new test unit created with number  {}'.format(payload['number']))

        self.info('get random order')
        radndom_order = random.choice(OrdersAPI().get_all_orders_json())
        self.assertTrue(radndom_order, 'No order selected')
        self.info('navigate to order edit page')
        order_page.get_order_edit_page_by_id(radndom_order['orderId'])
        order_page.sleep_small()

        if first_search_option == "Type":
            if second_search_option == "Method":
                checked_text = f'Quantitative: {payload["method"]}'
            elif second_search_option == "No":
                checked_text = f'Quantitative: {payload["number"]}'
        else:
            checked_text = f'{payload["name"]}: Quantitative'

        self.info("is test unit options existing?")
        options_exist['is_name_exist'] = order_page.is_test_unit_option_exist(search_field=payload['name'])
        options_exist['is_no_exist'] = order_page.is_test_unit_option_exist(search_field=str(payload['number']))
        options_exist['is_type_exist'] = order_page.is_test_unit_option_exist(search_field='Quantitative',
                                                                              checked_text=checked_text)
        options_exist['is_method_exist'] = order_page.is_test_unit_option_exist(search_field=payload['method'])
        options_exist['is_unit_exist'] = order_page.is_test_unit_option_exist(search_field=payload['unit'])
        options_exist['is_quantification_limit_exist'] = order_page.is_test_unit_option_exist(
            search_field=quantification_limit)

        for key, value in options_exist.items():
            if (first_search_option.lower().replace(' ', '_') in key) or (len(second_search_option.lower()) > 0 and second_search_option.lower() in key):
                self.assertTrue(value, f'{key} value should be True')
            else:
                self.assertFalse(value, f'{key} value should be False')
