from ui_testing.pages.orders_page import Orders


class Order(Orders):
    def get_order(self):
        return self.base_selenium.get_text(element='order:order').split('\n')[0]

    def set_new_order(self):
        self.base_selenium.select_item_from_drop_down(element='order:order', item_text='New Order')

    def set_existing_order(self):
        self.base_selenium.select_item_from_drop_down(element='order:order', item_text='Existing Order')

    def set_material_type(self, material_type=''):
        if material_type:
            self.base_selenium.select_item_from_drop_down(element='order:material_type', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:material_type')
            return self.get_material_type()

    def get_material_type(self):
        return self.base_selenium.get_text(element='order:material_type').split('\n')[0]

    def get_article(self):
        return self.base_selenium.get_text(element='order:article').split('\n')[0]

    def set_article(self, article=''):
        if article:
            self.base_selenium.select_item_from_drop_down(element='order:article', item_text=article)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:article')
            return self.get_article()

    def is_article_existing(self, article):
        self.set_article(article=article)
        return self.base_selenium.check_item_in_items(element='order:article', item_text=article)

    def set_contact(self, contact=''):
        if contact:
            self.base_selenium.select_item_from_drop_down(element='order:contact', item_text=contact)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:contact')
            return self.get_contact()

    def get_contact(self):
        return self.base_selenium.get_text(element='order:contact').split('\n')[0]

    def set_test_plan(self, test_plan=''):
        # test_plan_btn = self.base_selenium.find_element_in_element(destination_element='order:test_plan_btn',
        #                                                            source_element='order:tests')
        # test_plan_btn.click()
        if test_plan:
            self.base_selenium.select_item_from_drop_down(element='order:test_plan', item_text=test_plan)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_plan')
            return self.get_test_plan()

    def get_test_plan(self):
        return self.base_selenium.get_text(element='order:test_plan').split('\n')[0]

    def set_test_unit(self, test_unit):
        # test_unit_btn = self.base_selenium.find_element_in_element(destination_element='order:test_unit_btn',
        #                                                            source_element='order:tests')
        # test_unit_btn.click()
        if test_unit:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit', item_text=test_unit)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit')
            return self.get_test_unit()

    def get_test_unit(self):
        return self.base_selenium.get_text(element='order:test_unit').split('\n')[0]

    def create_new_order(self, material_type='', article='', contact='', test_plan='', test_unit=''):
        self.set_new_order()
        self.set_material_type(material_type=material_type)
        self.set_article(article=article)
        self.set_contact(contact=contact)
        if test_plan:
            self.set_test_plan(test_plan=test_plan)
        elif test_unit:
            self.set_test_unit(test_unit=test_unit)
        self.save(save_btn='order:save')
