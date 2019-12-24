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


    def test011_create_testplans_same_name_article_materialtype(self):
        '''
        LIMS-3499
        Testing the creation of two testplans with the same name, material type
        and article, this shouldn't happen
        '''

        # navigate to the articles page to create a new article
        self.article_page.get_articles_page()
        article_data = self.article_page.create_new_article() # dictionary of 'name' and 'material_type'
        self.base_selenium.LOGGER.info('New article is created successfully with name: {} and material type: {}'.format(article_data['name'], article_data['material_type']))

        # navigate to the testplans page
        self.test_plan.get_test_plans_page()
        testplan_name = self.test_plan.create_new_test_plan(material_type=article_data['material_type'], article=article_data['name'])
        self.base_selenium.LOGGER.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(testplan_name, article_data['name'], article_data['material_type']))

        self.base_selenium.LOGGER.info('Attempting to create another testplan with the same data as the previously created one')

        # create another testplan with the same data
        self.test_plan.create_new_test_plan(name=testplan_name, material_type=article_data['material_type'], article=article_data['name'])
        
        self.base_selenium.LOGGER.info(
            'Waiting for the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')

        self.base_selenium.LOGGER.info(
            'Assert the error message to make sure that validation forbids the creation of two testplans having the same name, material type and article? {}'.format(
                validation_result))
        self.assertTrue(validation_result)