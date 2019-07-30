from ui_testing.pages.testplans_page import TestPlans


class TstPlan(TestPlans):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")

    def set_no(self, no):
        self.base_selenium.set_text(element="test_plan:no", value=no)

    def get_article(self):
        articles = self.base_selenium.get_value(element="test_plan:article")
        if "×" in articles:
            return articles.replace("× ", "").split('\n')
        else:
            return []

    def set_article(self, article='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='test_plan:article')
            return self.get_article()
        else:
            self.base_selenium.select_item_from_drop_down(element='test_plan:article', item_text=article)

    def clear_article(self):
        if self.get_article():
            self.base_selenium.clear_items_in_drop_down(element='test_plan:article')

    def get_material_type(self):
        return self.base_selenium.get_text(element='test_plans:material_type')

    def set_material_type(self, material_type='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='test_plan:material_type')
            return self.get_material_type()
        else:
            self.base_selenium.select_item_from_drop_down(element='test_plan:material_type', item_text=material_type)

    def get_test_plan(self):
        return self.base_selenium.get_text(element='test_plan:test_plan')

    def set_test_plan(self, name='', random=False):
        name = self.generate_random_text() if random else name
        self.base_selenium.set_text_in_drop_down(ng_select_element='test_plan:test_plan', text=name)
        return name

    def set_test_unit(self, test_unit='', **kwargs):
        self.base_selenium.click('test_plan:next')
        self.base_selenium.click('test_plan:add_test_units')
        self.base_selenium.select_item_from_drop_down(element='test_plan:test_units', item_text='Qualitative')
        self.base_selenium.click('test_plan:add')

    def create_new_test_plan(self, name='', material_type='', article='', test_unit='', **kwargs):
        self.base_selenium.LOGGER.info(' + Create new test plan')
        self.test_plan_name = name or self.generate_random_text()
        self.material_type = material_type
        self.article = article
        self.click_create_test_plan_button()
        self.set_test_plan(name=self.test_plan_name)
        if self.material_type:
            self.set_material_type(material_type=self.material_type)
        else:
            self.material_type = self.set_material_type(random=True)
        self.sleep_tiny()
        if self.article:
            self.set_article(article=article)
        else:
            self.article = self.set_article(random=True)

        if test_unit:
            self.set_test_unit(test_unit=test_unit, **kwargs)
            self.save(save_btn='test_plan:save')
        else:
            self.save()

        self.base_selenium.LOGGER.info(' + Test plan name : {}'.format(self.test_plan_name))

        return self.test_plan_name

    def is_article_existing(self, article):
        self.set_article(article=article)
        return self.base_selenium.check_item_partially_in_items(element='test_plan:article', item_text=article)


