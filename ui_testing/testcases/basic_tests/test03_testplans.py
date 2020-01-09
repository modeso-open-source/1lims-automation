from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
from ui_testing.pages.articles_page import Articles
import random


class TestPlansTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.articles_page = Articles()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_plan.get_test_plans_page()

    @parameterized.expand(['ok', 'cancel'])
    def test001_create_approach_overview_button(self, ok):
        self.test_plan.click_create_test_plan_button()
        self.test_plan.sleep_tiny()
        # click on Overview, this will display an alert to the user
        self.base_page.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.base_page.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
            self.base_selenium.LOGGER.info('clicking on Overview confirmed')
        else:
            self.base_page.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans/add'.format(self.base_selenium.url))
            self.base_selenium.LOGGER.info('clicking on Overview cancelled')

    def test002_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202
        """
        self.test_plan.get_random_test_plans()
        testplans_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info('testplans_url : {}'.format(testplans_url))
        # click on Overview, it will redirect you to articles' page
        self.base_selenium.LOGGER.info('click on Overview')
        self.base_page.click_overview()
        self.test_plan.sleep_tiny()
        self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
        self.base_selenium.LOGGER.info('clicking on Overview confirmed')

    def test003_testplans_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page
        LIMS-6201

        """
        testplans = self.get_all_test_plans()
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

     def test004_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration

        LIMS-6288
        """
        assert (self.test_unit_page.deselect_all_configurations(), False)
