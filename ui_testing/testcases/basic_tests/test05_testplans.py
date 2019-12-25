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

    def test012_test_unit_update_version_in_testplan(self):
        '''
        LIMS-3703
        Create two testplans the first one with the testunit before updating its version, while
        the second is after updating the version (category and iteration)
        The updates should be only available in the second testplan
        '''
        
        # get all the testunits and choose a random testunit to create the first testplan with
        testunits = self.get_all_testunits()
        random_testunit = random.choice(testunits)
        self.base_selenium.LOGGER.info('A random testunit is chosen, its name: {}, category: {} and number of iterations: {}'.format(random_testunit['name'], random_testunit['categoryName'], random_testunit['iterations']))

        # get all articles and choose a random one to take its information
        articles = self.get_all_articles()
        random_article = random.choice(articles)
        self.base_selenium.LOGGER.info('A random article is chosen, its name: {} and its material type: {}'.format(random_article['name'], random_article['materialType']))

        # create the first testplan
        first_testplan_name = self.test_plan.create_new_test_plan(material_type=random_article['materialType'], article=random_article['name'], test_unit=random_testunit['name'])
        self.base_selenium.LOGGER.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(first_testplan_name, random_article['name'], random_article['materialType']))

        # go to testplan edit to get the number of iterations and testunit category
        first_testplan_testunit_category, first_testplan_testunit_iteration = self.test_plan.get_testunit_category_and_iterations(first_testplan_name)

        # go to testunits active table and search for this testunit-
        self.test_unit_page.get_test_units_page()
        self.base_selenium.LOGGER.info('Navigating to testunit {} edit page'.format(random_testunit['name']))
        testunit = self.test_unit_page.search(value=random_testunit['name'])[0]
        self.test_unit_page.open_edit_page(row=testunit)
        
        # update the iteration and category
        new_iteration = str(int(first_testplan_testunit_iteration) + 1)
        self.test_unit_page.update_testunit(number=None, name=None, category='', iterations=new_iteration, random=False)
        new_category = self.test_unit_page.get_category()

        # press save and complete to create a new version
        self.test_unit_page.save_and_create_new_version()

        # go back to testplans active table
        self.test_plan.get_test_plans_page()

        # create new testplan with this testunit after creating the new version
        second_testplan_name = self.test_plan.create_new_test_plan(material_type=random_article['materialType'], article=random_article['name'], test_unit=random_testunit['name'])
        self.base_selenium.LOGGER.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(second_testplan_name, random_article['name'], random_article['materialType']))

        # check the iteration and category to be the same as the new version
        # go to testplan edit to get the number of iterations and testunit category
        second_testplan_testunit_category, second_testplan_testunit_iteration = self.test_plan.get_testunit_category_and_iterations(second_testplan_name)

        self.base_selenium.LOGGER.info('Asserting that the category of the testunit in the first testplan is not equal the category of the testunit in the second testplan')
        self.assertNotEqual(first_testplan_testunit_category, second_testplan_testunit_category)
        self.base_selenium.LOGGER.info('Asserting that the iterations of the testunit in the first testplan is not equal the iterations of the testunit in the second testplan')
        self.assertNotEqual(first_testplan_testunit_iteration, second_testplan_testunit_iteration)
        self.base_selenium.LOGGER.info('Asserting that the category of the testunit in the second testplan is the same as the updated category')
        self.assertEqual(second_testplan_testunit_category, new_category)
        self.base_selenium.LOGGER.info('Asserting that the iterations of the testunit in the second testplan is the same as the updated iterations')
        self.assertEqual(second_testplan_testunit_iteration, new_iteration)