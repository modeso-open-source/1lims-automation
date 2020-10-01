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
from ui_testing.pages.my_profile_page import MyProfile
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.base_api import BaseAPI
from parameterized import parameterized
from datetime import date
from nose.plugins.attrib import attr
from unittest import skip



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

    @parameterized.expand(['0', '1', '2'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-349")
    def test005_order_no_format_in_XLSX_sheet(self, year_option):
        """
         Orders: Search/filter Approach: User can search/filter by all the new number format
         (without year, number before year, number after year

         LIMS-4110
         LIMS-4109 format in XLSX sheet
        """
        if year_option == '2':  # year before number
            self.orders_api.set_configuration_year_before_no()
        elif year_option == '0':  # without year
            self.orders_api.set_configuration_without_year()
        response, payload = self.orders_api.create_new_order(yearOption=int(year_option))
        self.assertEqual(response['status'], 1)
        order_no = payload[0]['orderNoWithYear']
        self.info('can filter in order active table with order no in format .{}'.format(format))
        self.orders_page.filter_by_order_no(order_no)
        rows = self.orders_page.result_table()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
        self.assertEqual(order_no, order_data['Order No.'])
        self.assertTrue(
            self.orders_page.is_order_no_match_config(year_option=year_option, order_no=order_data['Order No.']))
        self.orders_page.click_check_box(rows[0])
        self.order_page.download_xslx_sheet()
        order_in_sheet = self.order_page.sheet.iloc[0]['Order No.']
        self.assertTrue(self.orders_page.is_order_no_match_config(year_option=year_option, order_no=order_in_sheet))

    @parameterized.expand(['0', '1', '2'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-349")
    def test006_order_no_format_in_duplicate_main_order_page(self, year_option):
        """
         Orders: Search/filter Approach: User can search/filter by all the new number format
         (without year, number before year, number after year

         LIMS-4110
         LIMS-4109 format in duplicate main order page
        """
        if year_option == '2':  # year before number
            self.orders_api.set_configuration_year_before_no()
        elif year_option == '0':  # without year
            self.orders_api.set_configuration_without_year()
        response, payload = self.orders_api.create_new_order(yearOption=int(year_option))
        self.assertEqual(response['status'], 1)
        order_no = payload[0]['orderNoWithYear']
        self.orders_page.filter_by_order_no(order_no)
        self.info('duplicate the main order')
        rows = self.orders_page.result_table()
        self.orders_page.click_check_box(rows[0])
        self.orders_page.duplicate_main_order_from_table_overview()
        self.orders_page.sleep_tiny()
        duplicated_order_number = self.order_page.get_no()
        self.assertTrue(
            self.orders_page.is_order_no_match_config(year_option=year_option, order_no=duplicated_order_number))

    @parameterized.expand(['0', '1', '2'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-349")
    def test007_order_no_format_in_create_form(self, year_option):
        """
        New: orders: No Approach: Number format should display in all sections
        (Table view, XLSX, Duplication, Suborder table, QR Code) in the configuration section

        LIMS-4109 format in create order form
        """
        if year_option == '2':  # year before number
            self.orders_api.set_configuration_year_before_no()
        elif year_option == '0':  # without year
            self.orders_api.set_configuration_without_year()
        self.info('open the create form')
        self.order_page.create_new_order()
        order_no = self.order_page.get_no()
        self.assertTrue(
            self.orders_page.is_order_no_match_config(year_option=year_option, order_no=order_no))

    @parameterized.expand(['0', '1', '2'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-349")
    def test008_order_no_format_in_analysis_section(self, year_option):
        """
        New: orders: No Approach: Number format should display in: Table view of the analysis section

        LIMS-4109
        """
        if year_option == '2':  # year before number
            self.orders_api.set_configuration_year_before_no()
        elif year_option == '0':  # without year
            self.orders_api.set_configuration_without_year()
        response, payload = self.orders_api.create_new_order(yearOption=int(year_option))
        self.assertEqual(response['status'], 1)
        order_no = payload[0]['orderNoWithYear']
        self.info('edit order with No {}'.format(order_no))
        self.orders_page.get_order_edit_page_by_id(response['order']['mainOrderId'])
        self.info('navigate to analysis tab')
        self.order_page.navigate_to_analysis_tab()
        analysis_record = SingleAnalysisPage().get_all_analysis_records()
        self.assertTrue(
            self.orders_page.is_order_no_match_config(year_option=year_option,
                                                      order_no=analysis_record[0]['Order No.']))

    @parameterized.expand(['0', '1', '2'])
    @attr(series=True)
    @skip("https://modeso.atlassian.net/browse/LIMSA-349")
    def test009_filter_by_order_no_format_in_analysis_active_table(self, year_option):
        """
         Orders: Search/filter Approach: User can search/filter by all the new number format
         (without year, number before year, number after year

         LIMS-4110 filter by order no in analysis active table
        """
        if year_option == '2':  # year before number
            self.orders_api.set_configuration_year_before_no()
        elif year_option == '0':  # without year
            self.orders_api.set_configuration_without_year()
        response, payload = self.orders_api.create_new_order(yearOption=int(year_option))
        self.assertEqual(response['status'], 1)
        order_no = payload[0]['orderNoWithYear']
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_order_no(order_no)
        self.analyses_page.sleep_tiny()
        self.assertEqual(len(self.orders_page.result_table()) - 1, 1)
        analysis_data = self.analyses_page.get_the_latest_row_data()
        self.assertEqual(analysis_data['Order No.'].replace("'", ""), order_no)
        self.assertTrue(self.orders_page.is_order_no_match_config(year_option=year_option,
                                                                  order_no=analysis_data['Order No.']))
