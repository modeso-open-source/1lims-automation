from ui_testing.pages.base_pages import BasePages
from random import randint


class TestPlans(BasePages):
    def __init__(self):
        super().__init__()
        self.test_plans_url = "{}testPlans".format(self.base_selenium.url)

    def get_test_plans_page(self):
        self.base_selenium.get(url=self.test_plans_url)
        self.sleep_small()

    def get_random_test_plans(self):
        row = self.base_selenium.get_table_rows(element='test_plans:test_plans_table')
        row_id = randint(1, len(row) - 1)
        row = row[row_id]
        test_plans_edit_button = self.base_selenium.find_element_in_element(source=row,
                                                                            destination_element='test_plans:test_plans_edit_button')
        test_plans_edit_button.click()
        self.sleep_medium()

    def click_create_test_plan_button(self):
        self.base_selenium.click(element='test_plans:new_test_plan')
        self.sleep_small()
