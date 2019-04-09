from ui_testing.pages.testplans_page import TestPlans
from random import randint
import time


class TestPlan(TestPlans):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")

    def set_no(self, no):
        self.base_selenium.set_text(element="test_plan:no", value=no)

    def get_article(self):
        return self.base_selenium.get_value(element="test_plans:article")

    def set_article(self, article='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='test_plan:article', random=True)
            return self.get_article()
        else:
            self.base_selenium.select_item_from_drop_down(element='test_plan:article', item_text=article)

    def get_material_type(self):
        return self.base_selenium.get_text(element='test_plans:material_type')

    def set_material_type(self, material_type='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='test_plan:material_type', random=True)
            return self.get_material_type()
        else:
            self.base_selenium.select_item_from_drop_down(element='test_plan:material_type', item_text=material_type)

    def create_new_test_plan(self, name='', material_type='', article=''):
        self.test_plan_name = name or self.generate_random_text()
        self.material_type = material_type
        self.article = article
        self.click_create_test_plan_button()
        self.base_selenium.set_text(element='test_plan:test_plan', value=name)
        self.base_selenium.click(element='test_plan:add_test_plan')

        if self.material_type:
            self.set_material_type(material_type=self.material_type)
        else:
            self.material_type = self.set_material_type(random=True)

        #TODO
        # ADD test uintes
        # SAVE

    def is_article_existing(self, article):
        return self.base_selenium.check_item_in_items(element='test_plan:article', item_text=article)


