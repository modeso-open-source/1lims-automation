from ui_testing.pages.base_pages import BasePages
from random import randint


class TestPlans(BasePages):
    def __init__(self):
        super().__init__()
        self.test_plans_url = "{}testPlans".format(self.base_selenium.url)

    def get_test_plans_page(self):
        self.base_selenium.LOGGER.info(' + Get test plans page.')
        self.base_selenium.get(url=self.test_plans_url)
        self.sleep_small()

    def get_random_test_plans(self):
        row = self.get_random_table_row('test_plans:test_plans_table')
        self.open_edit_page(row=row)

    def click_create_test_plan_button(self):
        self.base_selenium.click(element='test_plans:new_test_plan')
        self.sleep_small()

    def get_test_plan_edit_page(self, name):
        self.base_selenium.LOGGER.info('Navigating to testplan {} edit page'.format(name))
        test_plan = self.search(value=name)[0]
        self.open_edit_page(row=test_plan)

    def get_testunits_in_testplans(self, test_plan_name=''):
        self.base_selenium.LOGGER.info('Filter by testplan name {}'.format(test_plan_name))
        self.search(value=test_plan_name)
        new_testplan_testunits=self.get_child_table_data(index=0)

        testplan_testunits = []
        for testunit in new_testplan_testunits:
            testplan_testunits.append(testunit['Test Unit Name'])
    
        return testplan_testunits

    def right_menu_action(self, action, row=''):

        self.base_selenium.LOGGER.info('Opening the right menu')
        self.base_selenium.click(element='test_plans:right_menu')
        self.sleep_small()
        self.base_selenium.LOGGER.info('Choosing {} from the right menu'.format(action))
        self.base_selenium.click(element='test_plans:{}'.format(action))
        self.sleep_small()

        if action == 'archive' or action == 'restore':
            self.confirm_popup()

    def search_for_multiple_rows(self, testplans_numbers, check=0):
        rows = []
        for tp_number in testplans_numbers:
            self.base_selenium.LOGGER.info('Searching for testplan number: {}'.format(tp_number))
            row = self.search(tp_number)
            rows.append(row[0])
            if check:
                self.base_selenium.LOGGER.info('Clicking the checkbox for testplan number: {}'.format(tp_number))
                self.click_check_box(row[0])
        return rows

