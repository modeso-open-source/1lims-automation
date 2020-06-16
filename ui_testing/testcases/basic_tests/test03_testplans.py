from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.articles_page import Articles
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.base_pages import BasePages
from ui_testing.pages.order_page import Order
from api_testing.apis.test_plan_api import TestPlanAPI
from ui_testing.pages.header_page import Header
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from unittest import skip
from parameterized import parameterized
import random


class TestPlansTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.test_plan = TstPlan()
        self.articles_page = Articles()
        self.test_unit_page = TstUnit()
        self.order_page = Order()
        self.base_page = BasePages()
        self.test_plan_api = TestPlanAPI()
        self.users_api = UsersAPI()
        self.test_unit_api = TestUnitAPI()
        self.article_api = ArticleAPI()

        self.set_authorization(auth=self.article_api.AUTHORIZATION_RESPONSE)
        self.test_plan.get_test_plans_page()

    def test001_test_plan_delete_testunit(self):
        '''
        LIMS-3504
        Testing deleting a test unit from testplan create or update step two
        It deletes the first test unit in the chosen test plan and saves this,
        then refreshes the page and checks if the deletion was done correctly.
        '''
        completed_test_plans = self.test_plan_api.get_completed_testplans(limit=500)
        testplan_name = random.choice(completed_test_plans)['testPlanName']

        # navigate to the chosen testplan edit page
        self.test_plan.get_test_plan_edit_page(testplan_name)

        # navigate to the testunits selection tab [Test plan create or update step 2] and get the testunits
        self.test_plan.navigate_to_testunits_selection_page()
        self.test_plan.switch_test_units_to_row_view()
        all_testunits = self.test_plan.get_all_testunits_in_testplan()

        # get the name of the first testunit, which is the one to be deleted
        deleted_test_unit = (all_testunits[0])[0]

        # delete the first testunit
        self.test_plan.delete_the_first_testunit_from_the_tableview()

        # save the changes
        self.test_plan.save_and_confirm_popup()

        # refresh the page to make sure the changes were saved correctly
        self.info('Refreshing the page')
        self.base_selenium.refresh()
        self.test_plan.sleep_small()

        self.test_plan.navigate_to_testunits_selection_page()
        all_testunits = self.test_plan.get_all_testunits_in_testplan()

        # checking if the data was saved correctly
        self.info('Checking if the changes were saved successfully')
        deleted_test_unit_found = self.test_plan.check_if_deleted_testunit_is_available(
            all_testunits=all_testunits, deleted_test_unit=deleted_test_unit)
        self.assertFalse(deleted_test_unit_found)

    @parameterized.expand(['InProgress', 'Completed'])
    def test002_test_plan_edit_status(self, status):
        """
        Creation Approach: when the status converted from completed to completed, new version created
        when the status converted from In-Progress to completed, no new version created

        LIMS-3502
        LIMS-3501
        """
        testplan = random.choice(self.test_plan_api.get_testplans_with_status(status=status))
        testplan_name = testplan['testPlanName']
        testplan_version = testplan['version']
        self.info('Navigating to edit page of testplan: {} with version: {}'.format(testplan_name, testplan_version))
        self.test_plan.get_test_plan_edit_page(name=testplan_name)

        # go to step 2 and add testunit
        self.info('Going to step 2 to add testunit to this test plan')
        self.test_plan.set_test_unit()
        if status == 'InProgress':
            self.info('Saving and completing the testplan')
            self.test_plan.save(save_btn='test_plan:save_and_complete', sleep=True)
        else:
            self.test_plan.save_and_confirm_popup()

        # go back to the active table
        self.test_plan.get_test_plans_page()

        # get the testplan to check its version
        self.info('Getting the currently changed testplan to check its status and version')
        new_testplan_version, testplan_row_data_status = \
            self.test_plan.get_testplan_version_and_status(search_text=testplan_name)

        if status == 'InProgress':
            self.assertEqual(int(new_testplan_version), testplan_version)
        else:
            self.assertGreater(int(new_testplan_version), int(testplan_version))

        self.assertEqual(testplan_row_data_status, 'Completed')

    def test003_archive_test_plan_one_record(self):
        '''
        LIMS-3506 Case 1
        Archive one record
        '''
        self.info('Choosing a random testplan table row')
        selected_test_plan = self.test_plan.select_random_table_row(element='test_plans:test_plans_table')
        testplan_number = selected_test_plan['Test Plan No.']

        # archive and navigate to archived table
        self.info('Archiving the selected item and navigating to the archived items table')
        self.test_plan.archive_selected_items()
        self.test_plan.get_archived_items()
        archived_row = self.test_plan.search(testplan_number)

        self.info('Checking if testplan number: {} is archived correctly'.format(testplan_number))
        self.assertIn(selected_test_plan['Test Plan Name'], archived_row[0].text)
        self.info('Testplan number: {} is archived correctly'.format(testplan_number))

    def test004_restore_test_plan_one_record(self):
        '''
        LIMS-3506 Case 1
        Restore one record
        '''

        self.test_plan.get_archived_items()

        self.base_selenium.LOGGER.info('Choosing a random testplan table row')
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_number = row_data['Test Plan No.']
        self.test_plan.sleep_small()

        # restore and navigate to active table
        self.base_selenium.LOGGER.info('Testplan number: {} will be restored'.format(testplan_number))

        self.base_selenium.LOGGER.info('Selecting the row')
        self.test_plan.click_check_box(source=row)
        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Restoring the selected item and navigating to the active items table')
        self.test_plan.restore_selected_items()
        self.test_plan.get_active_items()

        self.test_plan.open_filter_menu()
        self.test_plan.filter_by_testplan_number(testplan_number)
        restored_row = self.test_plan.result_table()
        self.base_selenium.LOGGER.info('Checking if testplan number: {} is restored correctly'.format(testplan_number))
        self.assertIn(row_data['Test Plan Name'], restored_row[0].text)
        self.base_selenium.LOGGER.info('Testplan number: {} is restored correctly'.format(testplan_number))

    def test005_archive_test_plan_multiple_records(self):
        '''
        LIMS-3506 Case 2
        Archive and restore multiple records
        '''

        self.base_selenium.LOGGER.info('Choosing random multiple testplans table rows')
        rows = self.test_plan.select_random_multiple_table_rows(element='test_plans:test_plans_table')
        testplan_rows = rows[0]
        testplans_numbers = []
        for row in testplan_rows:
            testplans_numbers.append(row['Test Plan No.'])
        self.test_plan.sleep_small()

        # archive and navigate to archived table
        self.base_selenium.LOGGER.info('Testplan numbers: {} will be archived'.format(testplans_numbers))
        self.base_selenium.LOGGER.info('Archiving the selected items and navigating to the archived items table')
        self.test_plan.archive_selected_items()

        self.base_selenium.LOGGER.info(
            'Checking if testplan numbers: {} are archived correctly'.format(testplans_numbers))

        self.test_plan.get_archived_items()
        archived_rows = self.test_plan.filter_multiple_rows_by_testplans_numbers(testplans_numbers)

        self.assertIsNotNone(archived_rows)
        self.assertEqual(len(archived_rows), len(testplans_numbers))

        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Testplan numbers: {} are archived correctly'.format(testplans_numbers))

    def test006_restore_test_plan_multiple_records(self):
        '''
        LIMS-3506 Case 2
        Archive and restore multiple records
        '''
        self.test_plan.get_archived_items()

        self.base_selenium.LOGGER.info('Choosing random multiple testplans table rows')
        rows = self.test_plan.select_random_multiple_table_rows(element='test_plans:test_plans_table')
        testplan_rows = rows[0]
        testplans_numbers = []
        for row in testplan_rows:
            testplans_numbers.append(row['Test Plan No.'])
        self.test_plan.sleep_small()

        # archive and navigate to archived table
        self.base_selenium.LOGGER.info('Testplan numbers: {} will be restored'.format(testplans_numbers))
        self.test_plan.restore_selected_items()
        self.base_selenium.LOGGER.info(
            'Checking if testplan numbers: {} are restored correctly'.format(testplans_numbers))
        self.test_plan.get_active_items()

        restored_rows = self.test_plan.filter_multiple_rows_by_testplans_numbers(testplans_numbers)

        self.assertIsNotNone(restored_rows)
        self.assertEqual(len(restored_rows), len(testplans_numbers))
        self.base_selenium.LOGGER.info('Testplan numbers: {} are restored correctly'.format(testplans_numbers))

    @skip('https://modeso.atlassian.net/browse/LIMS-6403')
    def test007_exporting_test_plan_one_record(self):
        '''
        LIMS-3508 Case 1
        Exporting one record
        '''
        self.base_selenium.LOGGER.info('Choosing a random testplan table row')
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_number = row_data['Test Plan No.']
        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Testplan number: {} will be exported'.format(testplan_number))

        self.base_selenium.LOGGER.info('Selecting the row')
        self.test_plan.click_check_box(source=row)
        self.test_plan.sleep_small()

        self.test_plan.download_xslx_sheet()

        row_data_list = list(row_data.values())
        self.base_selenium.LOGGER.info('Comparing the testplan no. {} '.format(testplan_number))
        values = self.test_plan.sheet.iloc[0].values
        fixed_sheet_row_data = self.fix_data_format(values)
        for item in row_data_list:
            if item != '' and item != '-':
                self.assertIn(item, fixed_sheet_row_data)

    @skip('https://modeso.atlassian.net/browse/LIMS-6403')
    def test008_exporting_test_plan_multiple_records(self):
        '''
        LIMS-3508 Case 2
        Exporting multiple records
        '''
        self.base_selenium.LOGGER.info('Choosing random multiple testplans table rows')
        rows = self.test_plan.select_random_multiple_table_rows(element='test_plans:test_plans_table')
        testplan_rows = rows[0]
        testplans_numbers = []
        for row in testplan_rows:
            testplans_numbers.append(row['Test Plan No.'])
        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Testplans numbers: {} will be exported'.format(testplans_numbers))

        self.test_plan.download_xslx_sheet()

        row_data_list = []
        for row_data in testplan_rows:
            row_data_list.append(list(row_data.values()))

        self.base_selenium.LOGGER.info('Comparing the testplan no. {} '.format(testplans_numbers))
        row_data_list = sorted(row_data_list, key=lambda x: x[1], reverse=True)

        for index in range(len(row_data_list)):
            fixed_row_data = self.fix_data_format(row_data_list[index])
            values = self.test_plan.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                if item != '' and item != '-':
                    self.assertIn(item, fixed_sheet_row_data)

    def test009_test_plan_duplicate(self):
        """
        LIMS-3679
        Duplicate a test plan

        LIMS-3679
        """
        # get the maximum number given to the latest testplan
        #latest_testplan_number = self.test_plan.get_the_latest_row_data()['Test Plan No.'].replace("'", "")
        #duplicated_test_plan_number = int(latest_testplan_number) + 1
        #self.info('The duplicated testplan should have the number: {}'.format(duplicated_test_plan_number))

        self.info('Choosing a random testplan table row')
        testPlan = random.choice(self.test_plan_api.get_completed_testplans())
        testunits = self.test_plan_api.get_testunits_in_testplan(id=testPlan['id'])
        self.test_plan.open_filter_menu()
        self.test_plan.filter_by_testplan_number(testPlan['number'])
        self.test_plan.sleep_small()
        self.test_plan.click_check_box(source=self.base_page.result_table()[0])
        self.test_plan.sleep_small()

        self.info('Duplicating testplan number: {}'.format(testPlan['number']))
        self.test_plan.duplicate_selected_item()
        duplicated_test_plan_number = self.test_plan.duplicate_testplan(change=['name'])

        duplicated_testplan_data, duplicated_testplan_childtable_data = \
            self.test_plan.get_specific_testplan_data_and_childtable_data(
                filter_by='number', filter_text=duplicated_test_plan_number)
        duplicated_test_units = []
        for testunit in duplicated_testplan_childtable_data:
            duplicated_test_units.append(testunit['Test Unit Name'])

        self.info('Asserting that the data is duplicated correctly')
        self.assertEqual(testPlan['materialType'], duplicated_testplan_data['Material Type'])
        self.assertEqual(testPlan['article'][0], duplicated_testplan_data['Article Name'])
        self.assertEqual(testPlan['articleNo'][0], duplicated_testplan_data['Article No.'])
        for testunit in testunits:
            self.assertIn(testunit['name'], duplicated_test_units)

    def test010_test_plan_completed_to_inprogress(self):
        '''
        LIMS-3503
        When the testplan status is converted from completed to in progress a new version is created
        '''
        self.base_selenium.LOGGER.info('Searching for test plans with Completed status')
        completed_testplans = self.test_plan_api.get_completed_testplans(limit=500)

        if completed_testplans is not None:
            self.base_selenium.LOGGER.info('Getting the first testplan')
            completed_testplan = completed_testplans[0]
            old_completed_testplan_name = completed_testplan['testPlanName']
            old_completed_testplan_version = completed_testplan['version']
            self.base_selenium.LOGGER.info(
                'Navigating to edit page of testplan: {} with version: {}'.format(old_completed_testplan_name,
                                                                                  old_completed_testplan_version))
            self.test_plan.get_test_plan_edit_page(name=old_completed_testplan_name)

            # go to step 2 and remove all the testunits
            self.base_selenium.LOGGER.info('Going to step 2 to remove all the testunits from it')
            self.test_plan.navigate_to_testunits_selection_page()
            self.test_plan.delete_all_testunits()
            self.test_plan.save_and_confirm_popup()

            # go back to the active table
            self.test_plan.get_test_plans_page()

            # get the testplan to check its version
            self.base_selenium.LOGGER.info('Getting the currently changed testplan to check its status and version')
            inprogress_testplan_version, testplan_row_data_status = self.test_plan.get_testplan_version_and_status(
                search_text=old_completed_testplan_name)

            self.assertEqual(old_completed_testplan_version + 1, int(inprogress_testplan_version))
            self.assertEqual(testplan_row_data_status, 'In Progress')

    @parameterized.expand(['same', 'all'])
    def test012_create_testplans_same_name_article_materialtype(self, same):
        """
        LIMS-3499
        Testing the creation of two testplans with the same name, material type
        and article, this shouldn't happen

        LIMS-3500
        New: Test plan: Creation Approach: I can't create two test plans
        with the same name & same materiel type & one with any article
        and the other one all
        """
        testplans = self.test_plan_api.get_all_test_plans_json()
        testplan = random.choice(testplans)

        testplan_name = self.test_plan.create_new_test_plan(
            material_type=testplan['materialType'], article=(testplan['article'])[0])
        self.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
            testplan_name, (testplan['article'])[0], testplan['materialType']))

        # create another testplan with the same data
        if "same" == same:
            article_name = (testplan['article'])[0]
        else:
            article_name = "All"

        self.test_plan.create_new_test_plan(
            name=testplan_name, material_type=testplan['materialType'], article=article_name)
        self.info('Waiting for the error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert the error message')
        self.assertTrue(validation_result)

    def test012_create_testplans_same_name_different_materialtype(self):
        '''
        LIMS-3498
        Testing the creation of two testplans with the same name, but different material type
        and article. It should be created successfully.
        '''

        testplans = self.test_plan_api.get_all_test_plans_json()
        first_testplan = random.choice(testplans)
        second_testplan = random.choice(testplans)

        testplan_name = self.test_plan.create_new_test_plan(material_type=first_testplan['materialType'],
                                                            article=(first_testplan['article'])[0])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, (first_testplan['article'])[0], first_testplan['materialType']))

        self.base_selenium.LOGGER.info(
            'Attempting to create another testplan with the same name as the previously created one, but with different material type and article name')

        # create another testplan with the same name, but with the second article's data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=second_testplan['materialType'],
                                            article=(second_testplan['article'])[0])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, (second_testplan['article'])[0], second_testplan['materialType']))

        data = self.test_plan.search(testplan_name)
        self.assertGreaterEqual(len(data), 2)

    def test013_create_testplans_same_name_materialtype_all_article(self):
        '''
        LIMS-3500
        New: Test plan: Creation Approach: I can't create two test plans
        with the same name & same materiel type & one with any article
        and the other one all
        '''

        testplans = self.test_plan_api.get_all_test_plans_json()
        testplan = random.choice(testplans)

        testplan_name = self.test_plan.create_new_test_plan(material_type=testplan['materialType'],
                                                            article=(testplan['article'])[0])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, (testplan['article'])[0], testplan['materialType']))

        self.base_selenium.LOGGER.info(
            'Attempting to create another testplan with the same name & material type as the previously created one,'
            ' and all articles')

        # create another testplan with the same data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=testplan['materialType'],
                                            article='All')

        self.base_selenium.LOGGER.info(
            'Waiting for the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            'Assert the error message to make sure that validation forbids the creation of two testplans having the same name, material type one of any article and the other for all articles? {}'.format(
                validation_result))
        self.assertTrue(validation_result)

    @skip('https://modeso.atlassian.net/browse/LIMS-6405')
    def test014_delete_used_testplan(self):
        '''
        LIMS-3509
        If a testplan is used, it can't be deleted
        '''
        test_plan_dict = self.get_active_article_with_tst_plan(test_plan_status='complete')
        testplan_name = test_plan_dict['Test Plan Name']
        testplan_article = test_plan_dict['Article Name']
        testplan_materialtype = test_plan_dict['Material Type']

        # create a new order with this testplan
        self.order_page.get_orders_page()
        self.order_page.create_new_order(material_type=testplan_materialtype, article=testplan_article,
                                         test_plans=[testplan_name])

        # delete testplan
        self.test_plan.get_test_plans_page()
        self.base_selenium.LOGGER.info('Testplan number: {} will be archived'.format(testplan_name))
        testplan_deleted = self.test_plan.delete_selected_item_from_active_table_and_from_archived_table(
            item_name=testplan_name)

        # check for the error popup that this testplan is used and can't be deleted
        self.assertFalse(testplan_deleted)

    def test015_archived_testplan_shouldnot_appear_in_order(self):
        '''
        LIMS-3708
        In case a testplan is archived, it shouldn't appear when creating a new order
        '''

        # choose a random testplan
        main_testplan_data = (self.test_plan.select_random_table_row(element='test_plans:test_plans_table'))
        testplan_number = (main_testplan_data['Test Plan No.']).replace("'", '')

        # get testplan data from an api call
        testplan_data = \
            (self.test_plan_api.get_testplan_with_filter(filter_option='number', filter_text=testplan_number))[0]

        # get information, material type and article
        testplan_name = testplan_data['testPlanName']
        testplan_materialtype = testplan_data['materialType']
        testplan_article = (testplan_data['article'])[0]

        # archive this testplan
        self.base_selenium.LOGGER.info('Archiving test plan: {}'.format(testplan_name))
        self.test_plan.archive_selected_items()

        # go to order's section
        self.order_page.get_orders_page()

        # create a new order with material type and article same as the saved ones
        self.order_page.create_new_order(material_type=testplan_materialtype, article=testplan_article,
                                         test_plans=[testplan_name])
        order_data = self.order_page.get_suborder_data()

        # get the first suborder's testplan and make sure it's an empty string
        suborder_first_testplan = (((order_data['suborders'])[0])['testplans'])[0]
        self.assertEqual(len(suborder_first_testplan), 0)

    def test016_testunit_sub_super_scripts(self):
        '''
        LIMS-5796
        Create a testunit with sub/super scripts, use this testunit to create a testplan
        and check the sub/super scripts in the card view
        '''
        testunit_name = self.generate_random_string()
        self.test_unit_page.get_test_units_page()

        active_articles_with_materialtype_dictionary = self.article_api.get_active_articles_with_material_type()
        random_materialtype = random.choice(list(active_articles_with_materialtype_dictionary.keys()))
        articles_with_chosen_materialtype = active_articles_with_materialtype_dictionary[random_materialtype]
        random_article = random.choice(articles_with_chosen_materialtype)

        self.test_unit_page.create_qualitative_testunit(name=testunit_name, unit='mg[2]{o}', method='a',
                                                        material_type=random_materialtype)
        testunit_unit_display = (self.base_selenium.find_element(element='test_unit:unit_display_value')).text

        self.test_unit_page.save()

        self.assertEqual(testunit_unit_display, 'mg2o')
        self.test_plan.get_test_plans_page()

        testplan_name = self.test_plan.create_new_test_plan(material_type=random_materialtype, article=random_article,
                                                            test_unit=testunit_name)

        self.test_plan.get_test_plan_edit_page(testplan_name)
        self.test_plan.navigate_to_testunits_selection_page()

        unit = self.base_selenium.find_element('test_plan:testunit_unit').text
        self.assertEqual(unit, testunit_unit_display)
        self.test_plan.switch_test_units_to_row_view()
        unit = self.base_selenium.find_element('test_plan:testunit_unit').text
        self.assertEqual(unit, testunit_unit_display)

    def test017_filter_by_testplan_number(self):
        '''
        LIMS-6473
        User can filter with testplan number
        '''

        testplans = self.test_plan_api.get_all_test_plans_json()
        random_testplan = random.choice(testplans)

        self.test_plan.open_filter_menu()
        self.test_plan.filter_by_testplan_number(random_testplan['number'])
        testplan_found = self.test_plan.result_table()
        self.assertIn(str(random_testplan['number']), (testplan_found[0].text).replace("'", ""))
        self.base_selenium.LOGGER.info('Filtering by number was done successfully')

    def test018_filter_by_testplan_name(self):
        '''
        LIMS-6470
        User can filter with testplan name
        '''

        testplans = self.test_plan_api.get_all_test_plans_json()
        random_testplan = random.choice(testplans)

        testplans_found = self.test_plan.filter_by_element_and_get_results('Testplan Name',
                                                                           'test_plans:testplan_name_filter',
                                                                           random_testplan['testPlanName'], 'drop_down')
        self.base_selenium.LOGGER.info('Checking if the results were filtered successfully')
        results_found = True
        while results_found:
            for tp in testplans_found:
                if len(tp.text) > 0:
                    self.assertIn(str(random_testplan['testPlanName']), tp.text)
            if self.base_page.is_next_page_button_enabled():
                self.base_selenium.click('general:next_page')
                self.test_plan.sleep_small()
                testplans_found = self.test_plan.result_table()
            else:
                results_found = False

        self.base_selenium.LOGGER.info('Filtering by name was done successfully')

    @parameterized.expand(['Completed', 'In Progress'])
    def test019_filter_by_testplan_status(self,status):
        '''
        LIMS-6474
        User can filter with status
        '''
        testplans_found = \
            self.test_plan.filter_by_element_and_get_results('Status', 'test_plans:testplan_status_filter',
                                                             status, 'drop_down')

        if len(testplans_found):
            results_found = True
        else:
            self.info("filter failed or no elements with this status!")

        while results_found:
            for tp in testplans_found:
                if len(tp.text) > 0:
                    self.assertIn(status, tp.text)
                    if status == "In Progress":
                        self.assertNotIn('Completed', tp.text)
                    else:
                        self.assertNotIn('In Progress', tp.text)

            if self.base_page.is_next_page_button_enabled():
                self.info('Navigating to the next page')
                self.base_selenium.click('general:next_page')
                self.test_plan.sleep_tiny()
                testplans_found = self.test_plan.result_table()
            else:
                results_found = False

        self.info('Filtering by status was done successfully')

    def test020_filter_by_testplan_changed_by(self):
        '''
        LIMS-6475
        User can filter with changed by field
        '''
        self.header_page = Header()
        random_user_name = self.generate_random_string()
        random_user_email = self.header_page.generate_random_email()
        random_user_password = self.generate_random_string()
        self.info('Calling the users api to create a new user with username: {}'.format(random_user_name))
        self.users_api.create_new_user(username=random_user_name, email=random_user_email,
                                       password=random_user_password)

        self.header_page.click_on_header_button()
        self.base_selenium.click('header:logout')
        self.login_page.login(username=random_user_name, password=random_user_password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_plan.get_test_plans_page()

        testplan_name = self.test_plan.create_new_test_plan()

        self.info('New testplan is created successfully with name: {}'.format(testplan_name))

        self.base_page.set_all_configure_table_columns_to_specific_value(value=True)

        testplan_found = self.test_plan.filter_by_element_and_get_results(
            'Changed By', 'test_plans:testplan_changed_by_filter', random_user_name, 'drop_down')
        self.assertEqual(len(testplan_found), 2)
        self.assertIn(random_user_name, testplan_found[0].text)
        self.assertIn(testplan_name, testplan_found[0].text)

    @parameterized.expand(['ok', 'cancel'])
    def test021_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table

        LIMS-6203
        """
        self.test_plan.click_create_test_plan_button()
        self.test_plan.sleep_tiny()
        # click on Overview, this will display an alert to the user
        self.base_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.base_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
            self.info('clicking on Overview confirmed')
        else:
            self.base_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans/add'.format(self.base_selenium.url))
            self.info('clicking on Overview cancelled')

    def test022_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202
        """
        self.test_plan.get_random_test_plans()
        testplans_url = self.base_selenium.get_url()
        self.info('testplans_url : {}'.format(testplans_url))
        # click on Overview, it will redirect you to articles' page
        self.info('click on Overview')
        self.base_page.click_overview()
        self.test_plan.sleep_tiny()
        self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
        self.info('clicking on Overview confirmed')

    def test023_testplans_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page

        LIMS-6201
        """
        test_plans_response = self.test_plan_api.get_all_test_plans()
        testplans = test_plans_response.json()['testPlans']
        testplan_name = random.choice(testplans)['testPlanName']
        search_results = self.test_plan.search(testplan_name)
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
            if search_data['Test Plan Name'] == testplan_name:
                break
        else:
            self.assertTrue(False, " * There is no search results for it, Report a bug.")
        self.assertEqual(testplan_name, search_data['Test Plan Name'])
        # Navigate to articles page
        self.info('navigate to articles page')
        self.articles_page.get_articles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}articles'.format(self.base_selenium.url))

    def test024_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration
        LIMS-6288
        """
        assert (self.test_unit_page.deselect_all_configurations(), False)

    def test026_test_unit_update_version_in_testplan(self):
        """
        LIMS-3703
        Test plan: Test unit Approach: In case I update category & iteration of test unit that used in test plan with new version
        ,when  go to test plan to add the same test unit , I found category & iteration updated
        """
        # select random test unit to create the test plan with it
        testunits, payload = self.test_unit_api.get_all_test_units(limited=20, filter='{"materialTypes":"all"}')
        testunit = random.choice(testunits['testUnits'])
        self.info('A random test unit is chosen, its name: {}, category: {} and number of iterations: {}'.format(
            testunit['name'], testunit['categoryName'], testunit['iterations']))

        # create the first testplan
        first_testplan_name, payload1 = self.test_plan_api.create_testplan()
        self.info('First test plan create with name: {}'.format(
            payload1['testPlan']['text']))

        # go to testplan edit to get the number of iterations and testunit category
        first_testplan_testunit_category, first_testplan_testunit_iteration =self.test_plan.get_testunit_category_iterations(
            payload1['testPlan']['text'], testunit['name'])

        # go to testunits active table and search for this testunit-
        self.test_unit_page.get_test_units_page()
        self.base_selenium.LOGGER.info(
            'Navigating to test unit {} edit page'.format(testunit['name']))
        self.test_unit_page.search(value=testunit['name'])
        self.test_unit_page.open_edit_page(row=self.test_unit_page.result_table()[0])

        new_iteration = str(int(first_testplan_testunit_iteration) + 1)
        # update the iteration and category
        new_category = self.test_unit_page.set_category('')
        self.test_unit_page.set_testunit_iteration(new_iteration)

        # press save and complete to create a new version
        self.test_unit_page.save_and_create_new_version()

        # go back to test plans active table
        self.test_plan.get_test_plans_page()

         #create new testplan with this testunit after creating the new version
        second_testplan_name, payload2 = self.test_plan_api.create_testplan()
        self.info('Second test plan create with name: {}'.format(
            payload2['testPlan']['text']))

        # check the iteration and category to be the same as the new version
        # go to testplan edit to get the number of iterations and testunit category
        second_testplan_testunit_category, second_testplan_testunit_iteration = self.test_plan.get_testunit_category_iterations(
            payload2['testPlan']['text'], testunit['name'])

        self.base_selenium.LOGGER.info(
            'Asserting that the category of the testunit in the first testplan is not equal the category of the testunit in the second testplan')
        self.assertNotEqual(first_testplan_testunit_category,
                        second_testplan_testunit_category)
        self.base_selenium.LOGGER.info(
            'Asserting that the iterations of the testunit in the first testplan is not equal the iterations of the testunit in the second testplan')
        self.assertNotEqual(first_testplan_testunit_iteration,
                        second_testplan_testunit_iteration)
        self.base_selenium.LOGGER.info(
            'Asserting that the category of the testunit in the second testplan is the same as the updated category')
        self.assertEqual(second_testplan_testunit_category, new_category)
        self.base_selenium.LOGGER.info(
            'Asserting that the iterations of the testunit in the second testplan is the same as the updated iterations')
        self.assertEqual(second_testplan_testunit_iteration, new_iteration)