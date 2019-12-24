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
        deleted_test_unit_found = self.test_plan.check_if_deleted_testunit_is_available(all_testunits=all_testunits, deleted_test_unit=deleted_test_unit)
        
        self.assertFalse(deleted_test_unit_found)


    def test012_create_testplans_same_name_different_materialtype(self):
        '''
        LIMS-3498
        Testing the creation of two testplans with the same name, but different material type
        and article. It should be created successfully.
        '''

        # navigate to the articles page to create two new articles
        self.article_page.get_articles_page()
        first_article_data = self.article_page.create_new_article() # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info('The first new article is created successfully with name: {} and material type: {}'.format(first_article_data['name'], first_article_data['material_type']))
        
        second_article_data = self.article_page.create_new_article() # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info('The second new article is created successfully with name: {} and material type: {}'.format(second_article_data['name'], second_article_data['material_type']))

        # navigate to the testplans page
        self.test_plan.get_test_plans_page()
        testplan_name = self.test_plan.create_new_test_plan(material_type=first_article_data['material_type'], article=first_article_data['name'])
        self.base_selenium.LOGGER.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(testplan_name, first_article_data['name'], first_article_data['material_type']))

        self.base_selenium.LOGGER.info('Attempting to create another testplan with the same name as the previously created one, but with different material type and article name')

        # create another testplan with the same name, but with the second article's data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=second_article_data['material_type'], article=second_article_data['name'])
        self.base_selenium.LOGGER.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(testplan_name, second_article_data['name'], second_article_data['material_type']))

        data = self.test_plan.search(testplan_name)
        search_length = 0
        for d in data:
            if len(d.text) != 0:
                search_length += 1

        self.assertEqual(search_length, 2)