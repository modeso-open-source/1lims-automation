from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re, random
from selenium.common.exceptions import NoSuchElementException


class TestPlansTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_plan.get_test_plans_page()

    def test001_test_plan_delete_testunit(self):
        '''
        LIMS-3504
        Testing deleting a test unit from testplan create or update step two
        It deletes the first test unit in the chosen test plan and saves this,
        then refreshes the page and checks if the deletion was done correctly.
        '''

        completed_test_plans = self.test_plan_api.get_completed_testplans()
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
        self.base_selenium.LOGGER.info('Refreshing the page')
        self.base_selenium.refresh()
        self.test_plan.sleep_small()

        self.test_plan.navigate_to_testunits_selection_page()
        all_testunits = self.test_plan.get_all_testunits_in_testplan()

        # checking if the data was saved correctly
        self.base_selenium.LOGGER.info('Checking if the changes were saved successfully')
        deleted_test_unit_found = self.test_plan.check_if_deleted_testunit_is_available(all_testunits=all_testunits,
                                                                                        deleted_test_unit=deleted_test_unit)

        self.assertFalse(deleted_test_unit_found)

    def test002_test_plan_inprogress_to_completed(self):
        '''
        LIMS-3502
        When the testplan status is converted from 'In-Progress' to 'Completed', no new version created
        '''

        self.base_selenium.LOGGER.info('Searching for test plans with In Progress status')
        in_progress_testplans = self.test_plan_api.get_inprogress_testplans()

        if in_progress_testplans is not None:
            self.base_selenium.LOGGER.info('Getting the first testplan')
            in_progress_testplan = in_progress_testplans[0]
            in_progress_testplan_name = in_progress_testplan['testPlanName']
            in_progress_testplan_version = in_progress_testplan['version']
            self.base_selenium.LOGGER.info(
                'Navigating to edit page of testplan: {} with version: {}'.format(in_progress_testplan_name,
                                                                                  in_progress_testplan_version))
            self.test_plan.get_test_plan_edit_page(name=in_progress_testplan_name)

            # go to step 2 and add testunit
            self.base_selenium.LOGGER.info('Going to step 2 to add testunit to this test plan')
            self.test_plan.set_test_unit()
            self.base_selenium.LOGGER.info('Saving and completing the testplan')
            self.test_plan.save(save_btn='test_plan:save_and_complete')

            # go back to the active table
            self.test_plan.get_test_plans_page()

            # get the testplan to check its version
            self.base_selenium.LOGGER.info('Getting the currently changed testplan to check its status and version')
            completed_testplan_version, testplan_row_data_status = self.test_plan.get_testplan_version_and_status(
                search_text=in_progress_testplan_name)

            self.assertEqual(in_progress_testplan_version, int(completed_testplan_version))
            self.assertEqual(testplan_row_data_status, 'Completed')

    def test003_test_plan_completed_to_completed(self):
        '''
        LIMS-3501
        When the testplan status doesn't change and a new version is created
        '''

        self.base_selenium.LOGGER.info('Searching for test plans with Completed status')
        completed_testplans = self.test_plan_api.get_completed_testplans()

        if completed_testplans is not None:
            self.base_selenium.LOGGER.info('Getting the first testplan')
            completed_testplan = completed_testplans[0]
            old_completed_testplan_name = completed_testplan['testPlanName']
            old_completed_testplan_version = completed_testplan['version']
            self.base_selenium.LOGGER.info(
                'Navigating to edit page of testplan: {} with version: {}'.format(old_completed_testplan_name,
                                                                                  old_completed_testplan_version))
            self.test_plan.get_test_plan_edit_page(name=old_completed_testplan_name)

            # go to step 2 and add testunit
            self.base_selenium.LOGGER.info('Going to step 2 to add testunit to this test plan')
            self.test_plan.set_test_unit(test_unit='a')
            self.test_plan.save_and_confirm_popup()

            # go back to the active table
            self.test_plan.get_test_plans_page()

            # get the testplan to check its version
            self.base_selenium.LOGGER.info('Getting the currently changed testplan to check its status and version')
            inprogress_testplan_version, testplan_row_data_status = self.test_plan.get_testplan_version_and_status(
                search_text=old_completed_testplan_name)

            # self.assertEqual(old_completed_testplan_version + 1, int(inprogress_testplan_version))
            self.assertGreater(int(inprogress_testplan_version), old_completed_testplan_version)
            self.assertEqual(testplan_row_data_status, 'Completed')

    def test004_archive_restore_test_plan_one_record(self):
        '''
        LIMS-3506 Case 1
        Archive and restore one record
        '''

        self.base_selenium.LOGGER.info('Choosing a random testplan table row')
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_number = row_data['Test Plan No.']
        self.test_plan.sleep_small()

        # archive and navigate to archived table
        self.base_selenium.LOGGER.info('Testplan number: {} will be archived'.format(testplan_number))

        self.base_selenium.LOGGER.info('Selecting the row')
        self.test_plan.click_check_box(source=row)
        self.test_plan.sleep_small()

        self.test_plan.archive_selected_items()
        self.test_plan.get_archived_items()

        archived_row = self.test_plan.search(testplan_number)
        self.test_plan.sleep_small()
        self.base_selenium.LOGGER.info('Checking if testplan number: {} is archived correctly'.format(testplan_number))
        self.assertIsNotNone(archived_row[0])
        self.base_selenium.LOGGER.info('Testplan number: {} is archived correctly'.format(testplan_number))

        # restore and navigate to active table
        self.base_selenium.LOGGER.info('Selecting the row')
        self.test_plan.click_check_box(source=archived_row[0])
        self.test_plan.sleep_small()

        self.test_plan.restore_selected_items()
        self.test_plan.get_active_items()

        restored_row = self.test_plan.search(testplan_number)
        self.base_selenium.LOGGER.info('Checking if testplan number: {} is restored correctly'.format(testplan_number))
        self.assertIsNotNone(restored_row[0])
        self.base_selenium.LOGGER.info('Testplan number: {} is restored correctly'.format(testplan_number))

    def test005_archive_restore_test_plan_multiple_records(self):
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

        self.test_plan.archive_selected_items()
        self.test_plan.get_archived_items()

        self.base_selenium.LOGGER.info(
            'Checking if testplan numbers: {} are archived correctly'.format(testplans_numbers))

        archived_rows = self.test_plan.search_for_multiple_rows(testplans_numbers, 1)

        self.assertIsNotNone(archived_rows)
        self.assertEqual(len(archived_rows), len(testplans_numbers))

        self.test_plan.sleep_small()

        self.base_selenium.LOGGER.info('Testplan numbers: {} are archived correctly'.format(testplans_numbers))

        # restore and navigate to active table
        self.test_plan.restore_selected_items()
        self.test_plan.get_active_items()

        self.base_selenium.LOGGER.info(
            'Checking if testplan numbers: {} are restored correctly'.format(testplans_numbers))

        restored_rows = self.test_plan.search_for_multiple_rows(testplans_numbers)
        self.assertIsNotNone(restored_rows)
        self.assertEqual(len(restored_rows), len(testplans_numbers))
        self.base_selenium.LOGGER.info('Testplan numbers: {} are restored correctly'.format(testplans_numbers))

    def test006_exporting_test_plan_one_record(self):
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

    def test007_exporting_test_plan_multiple_records(self):
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

    def test008_test_plan_duplicate(self):
        '''
        LIMS-3679
        Duplicate a test plan
        '''
        # get the maximum number given to the latest testplan
        latest_testplan_row_data = self.test_plan.get_the_latest_row_data()
        largest_number = latest_testplan_row_data['Test Plan No.']
        duplicated_test_plan_number = int(largest_number) + 1
        self.base_selenium.LOGGER.info(
            'The duplicated testplan should have the number: {}'.format(duplicated_test_plan_number))

        self.base_selenium.LOGGER.info('Choosing a random testplan table row')
        main_testplan_data, row_index = self.test_plan.select_random_table_row(element='test_plans:test_plans_table')
        testplan_number = main_testplan_data['Test Plan No.']
        self.base_selenium.LOGGER.info('Testplan number: {} will be duplicated'.format(testplan_number))

        self.base_selenium.LOGGER.info('Saving the child data of the main testplan')
        main_testplan_childtable_data = self.test_plan.get_child_table_data(index=row_index)

        self.base_selenium.LOGGER.info('Duplicating testplan number: {}'.format(testplan_number))
        self.test_plan.duplicate_selected_item()

        self.test_plan.duplicate_testplan(change=['name'])
        self.test_plan.sleep_small()

        duplicated_testplan_data, duplicated_testplan_childtable_data = self.test_plan.get_specific_testplan_data_and_childtable_data(
            filter_by='number', filter_text=duplicated_test_plan_number)
        data_changed = ['Test Plan No.', 'Test Plan Name', 'Version', 'Changed On', 'Changed By', 'Created On']
        main_testplan_data, duplicated_testplan_data = self.remove_unduplicated_data(data_changed=data_changed,
                                                                                     first_element=main_testplan_data,
                                                                                     second_element=duplicated_testplan_data)

        self.base_selenium.LOGGER.info('Asserting that the data is duplicated correctly')
        self.assertEqual(main_testplan_childtable_data, duplicated_testplan_childtable_data)
        self.assertEqual(main_testplan_data, duplicated_testplan_data)

    def test009_test_plan_completed_to_inprogress(self):
        '''
        LIMS-3503
        When the testplan status is converted from completed to in progress a new version is created
        '''
        self.base_selenium.LOGGER.info('Searching for test plans with Completed status')
        completed_testplans = self.test_plan_api.get_completed_testplans()

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

    def test010_create_testplans_same_name_article_materialtype(self):
        '''
        LIMS-3499
        Testing the creation of two testplans with the same name, material type
        and article, this shouldn't happen
        '''

        # navigate to the articles page to create a new article
        self.article_page.get_articles_page()
        article_data = self.article_page.create_new_article()  # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info(
            'New article is created successfully with name: {} and material type: {}'.format(article_data['name'],
                                                                                             article_data[
                                                                                                 'material_type']))

        # navigate to the testplans page
        self.test_plan.get_test_plans_page()
        testplan_name = self.test_plan.create_new_test_plan(material_type=article_data['material_type'],
                                                            article=article_data['name'])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, article_data['name'], article_data['material_type']))

        self.base_selenium.LOGGER.info(
            'Attempting to create another testplan with the same data as the previously created one')

        # create another testplan with the same data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=article_data['material_type'],
                                            article=article_data['name'])

        self.base_selenium.LOGGER.info(
            'Waiting for the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            'Assert the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article? {}'.format(
                validation_result))
        self.assertTrue(validation_result)

    def test011_create_testplans_same_name_different_materialtype(self):
        '''
        LIMS-3498
        Testing the creation of two testplans with the same name, but different material type
        and article. It should be created successfully.
        '''

        # navigate to the articles page to create two new articles
        self.article_page.get_articles_page()
        first_article_data = self.article_page.create_new_article()  # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info(
            'The first new article is created successfully with name: {} and material type: {}'.format(
                first_article_data['name'], first_article_data['material_type']))

        second_article_data = self.article_page.create_new_article()  # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info(
            'The second new article is created successfully with name: {} and material type: {}'.format(
                second_article_data['name'], second_article_data['material_type']))

        # navigate to the testplans page
        self.test_plan.get_test_plans_page()
        testplan_name = self.test_plan.create_new_test_plan(material_type=first_article_data['material_type'],
                                                            article=first_article_data['name'])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, first_article_data['name'], first_article_data['material_type']))

        self.base_selenium.LOGGER.info(
            'Attempting to create another testplan with the same name as the previously created one, but with different material type and article name')

        # create another testplan with the same name, but with the second article's data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=second_article_data['material_type'],
                                            article=second_article_data['name'])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, second_article_data['name'], second_article_data['material_type']))

        data = self.test_plan.search(testplan_name)
        search_length = 0
        for d in data:
            if len(d.text) != 0:
                search_length += 1

        self.assertEqual(search_length, 2)

    def test012_create_testplans_same_name_materialtype_all_article(self):
        '''
        New: Test plan: Creation Approach: I can't create two test plans
        with the same name & same materiel type & one with any article
        and the other one all

        LIMS-3500
        '''
        # navigate to the articles page to create a new article
        self.article_page.get_articles_page()
        article_data = self.article_page.create_new_article()  # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info(
            'New article is created successfully with name: {} and material type: {}'.format(article_data['name'],
                                                                                             article_data[
                                                                                                 'material_type']))

        # navigate to the testplans page
        self.test_plan.get_test_plans_page()
        testplan_name = self.test_plan.create_new_test_plan(material_type=article_data['material_type'],
                                                            article=article_data['name'])
        self.base_selenium.LOGGER.info(
            'New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                testplan_name, article_data['name'], article_data['material_type']))

        self.base_selenium.LOGGER.info(
            'Attempting to create another testplan with the same name and material type as the previously created one')

        # create another testplan with the same data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=article_data['material_type'],
                                            article='All')

        self.base_selenium.LOGGER.info(
            'Waiting for the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            'Assert the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article? {}'.format(
                validation_result))
        self.assertTrue(validation_result)
