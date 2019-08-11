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
        row = self.base_selenium.get_table_rows(element='test_plans:test_plans_table')
        self.get_random_x(row=row)

    def click_create_test_plan_button(self):
        self.base_selenium.click(element='test_plans:new_test_plan')
        self.sleep_small()

    def get_test_plan_edit_page(self, name):
        test_plan = self.search(value=name)[0]
        self.get_random_x(row=test_plan)

    def get_testunits_in_testplans(self, test_plan_name=''):
        self.base_selenium.LOGGER.info('Filter by testplan name {}'.format(test_plan_name))
        self.search(value=test_plan_name)
        new_testplan_testunits=self.get_child_table_data(index=0)

        testplan_testunits = []
        for testunit in new_testplan_testunits:
            testplan_testunits.append(testunit['Test Unit Name'])
    
        return testplan_testunits

