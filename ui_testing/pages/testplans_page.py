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
        self.base_selenium.LOGGER.info('Search by testplan name {}'.format(test_plan_name))
        self.search(value=test_plan_name)
        new_testplan_testunits=self.get_child_table_data(index=0)

        testplan_testunits = []
        for testunit in new_testplan_testunits:
            testplan_testunits.append(testunit['Test Unit Name'])
    
        return testplan_testunits

    def get_specific_testplan_data_and_childtable_data(self, filter_by='number', filter_text=''):
        if filter_by == 'number':
            self.filter_by_testplan_number(filter_text)
        found_testplan = self.result_table()[0]
        found_testplan_data = self.base_selenium.get_row_cells_dict_related_to_header(row=found_testplan)
        found_testplan_childtable_data = self.get_child_table_data(index=0)

        return found_testplan_data, found_testplan_childtable_data

    def filter_by_testplan_number(self, filter_text):
        self.base_selenium.LOGGER.info('Filtering by testplan number: {}'.format(filter_text))
        self.open_filter_menu()
        self.filter_by(filter_element='test_plans:testplan_number_filter', filter_text=filter_text, field_type='text')
        self.filter_apply()

