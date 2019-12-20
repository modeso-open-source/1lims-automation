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

    def test005_archive_restore_test_plan_one_record(self):
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

        self.test_plan.right_menu_action('archive')
        self.test_plan.right_menu_action('archived')

              
        archived_row = self.test_plan.search(testplan_number)
        self.test_plan.sleep_small()
        self.base_selenium.LOGGER.info('Checking if testplan number: {} is archived correctly'.format(testplan_number))
        self.assertIsNotNone(archived_row[0])
        self.base_selenium.LOGGER.info('Testplan number: {} is archived correctly'.format(testplan_number))

        # restore and navigate to active table
        self.base_selenium.LOGGER.info('Selecting the row')
        self.test_plan.click_check_box(source=archived_row[0])
        self.test_plan.sleep_small()

        self.test_plan.right_menu_action('restore')
        self.test_plan.right_menu_action('active')

        restored_row = self.test_plan.search(testplan_number)
        self.base_selenium.LOGGER.info('Checking if testplan number: {} is restored correctly'.format(testplan_number))
        self.assertIsNotNone(restored_row[0])
        self.base_selenium.LOGGER.info('Testplan number: {} is restored correctly'.format(testplan_number))

    def test006_archive_restore_test_plan_multiple_records(self):
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

        self.test_plan.right_menu_action('archive')
        self.test_plan.right_menu_action('archived')

        self.base_selenium.LOGGER.info('Checking if testplan numbers: {} are archived correctly'.format(testplans_numbers))

        archived_rows = self.test_plan.search_for_multiple_rows(testplans_numbers, 1)

        self.assertIsNotNone(archived_rows)
        self.assertEqual(len(archived_rows), len(testplans_numbers))

        self.test_plan.sleep_small()
        
        self.base_selenium.LOGGER.info('Testplan numbers: {} are archived correctly'.format(testplans_numbers))

        # restore and navigate to active table
        self.test_plan.right_menu_action('restore')
        self.test_plan.right_menu_action('active')

        self.base_selenium.LOGGER.info('Checking if testplan numbers: {} are restored correctly'.format(testplans_numbers))

        restored_rows = self.test_plan.search_for_multiple_rows(testplans_numbers)
        self.assertIsNotNone(restored_rows)
        self.assertEqual(len(restored_rows), len(testplans_numbers))
        self.base_selenium.LOGGER.info('Testplan numbers: {} are restored correctly'.format(testplans_numbers))
