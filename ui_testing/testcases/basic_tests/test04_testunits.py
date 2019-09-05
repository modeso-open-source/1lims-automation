from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re


class TestUnitsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_unit_page.get_test_units_page()

    @skip('https://modeso.atlassian.net/browse/LIMS-5237')
    def test001_test_units_search(self):
        """
        New: Test units: Search Approach: I can search by any field in the table view

        LIMS-3674
        :return:
        """
        row= self.test_unit_page.get_random_test_units_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.article_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test002_archive_test_units(self):
        """
        New: Test units: Archive Approach: I can archive any test unit successfully.

        LIMS-3670
        :return:
        """
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        self.test_unit_page.archive_selected_test_units()
        self.test_unit_page.get_archived_test_units()
        for test_unit in selected_test_units_data:
            test_unit_name = test_unit['Test Unit Name']
            self.base_selenium.LOGGER.info(' + {} Test Unit should be activated.'.format(test_unit_name))
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit_name))

    def test003_restore_test_units(self):
        """
         New: Test units: Restore Approach: I can restore any test unit successfully.

        LIMS-5262
        :return:
        """
        test_unit_names = []
        self.test_unit_page.get_archived_test_units()
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        for test_unit in selected_test_units_data:
            test_unit_names.append(test_unit['Test Unit Name'])

        self.test_unit_page.restore_selected_test_units()
        self.test_unit_page.get_active_test_units()
        for test_unit_name in test_unit_names:
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit_name))

    def test004_check_version_after_update(self):
        """
        After I update any field then press on save , new version created in the active table.

        LIMS-3676

        After the user edit any of the followings fields

        test unit name 
        test unit number 
        category
        method
        iteration
        materiel type 
        specification 

        the should updated successfully when I enter one more time 

        LIMS-5288
        """

        self.base_selenium.LOGGER.info('Generate random data for update')
        newRandomNumber = self.generate_random_number(limit=100000)
        newRandomName = self.generate_random_string()
        newRandomMethod = self.generate_random_string()
        newRandomCategry = self.generate_random_string()
        newRandomIterations = self.generate_random_number(limit=4)

        self.base_selenium.LOGGER.info('Getting data of the first testunit')
        testunitsRecords = self.order_page.result_table()
        firstTestunitData = self.base_selenium.get_row_cells_dict_related_to_header(row=testunitsRecords[0])
        
        oldVersion = firstTestunitData['Version']
        self.base_selenium.LOGGER.info('old version: {}'.format(oldVersion))
        self.base_selenium.LOGGER.info('Open the first record to update it')
        self.test_unit_page.get_random_x(row=testunitsRecords[0])
        
        self.base_selenium.LOGGER.info('Set the method to be: {}'.format(newRandomMethod))
        self.test_unit_page.set_method(method=newRandomMethod)

        self.base_selenium.LOGGER.info('Set new material type')        
        self.test_unit_page.set_material_type()

        self.base_selenium.LOGGER.info('Set the new category to be: {}'.format(newRandomCategry))
        self.test_unit_page.set_category(category=newRandomCategry)

        self.base_selenium.LOGGER.info('Set the new testunit name to be: {}'.format(newRandomName))
        self.test_unit_page.set_testunit_name(name=newRandomName)

        self.base_selenium.LOGGER.info('Set the new testunit number to be: {}'.format(newRandomNumber))
        self.test_unit_page.set_testunit_number(number=newRandomNumber)

        self.base_selenium.LOGGER.info('Set the new testunit iteartions to be: {}'.format(newRandomIterations))
        self.test_unit_page.set_testunit_iteration(iteration=newRandomIterations)

        self.base_selenium.LOGGER.info('pressing save and create new version')
        self.test_unit_page.saveAndCreateNewVersion(confirm=True)

        self.base_selenium.LOGGER.info('Refresh to make sure that the new data are saved')
        self.base_selenium.refresh()
        self.test_unit_page.sleep_small()
        
        self.base_selenium.LOGGER.info('checking that data are saved correctly after refresh')
        updatedTestunitName = self.test_unit_page.get_testunit_name()
        updateTestunitNumber = self.test_unit_page.get_testunit_number()

        self.test_unit_page.get_test_units_page()
        testunitsRecords = self.order_page.result_table()
        firstTestunitData = self.base_selenium.get_row_cells_dict_related_to_header(row=testunitsRecords[0])
        newVersion = firstTestunitData['Version']
        self.base_selenium.LOGGER.info('old version: {}, new version: {}'.format(oldVersion, newVersion))


