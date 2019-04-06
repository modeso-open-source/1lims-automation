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
            self.base_selenium.select_item_from_drop_down(element='order:material_type', random=True)
            return self.get_material_type()

    def get_material_type(self):
        return self.base_selenium.get_text(element='order:material_type').split('\n')[0]

    def get_article(self):
        return self.base_selenium.get_text(element='order:article').split('\n')[0]

    def set_article(self, article=''):
        if article:
            self.base_selenium.select_item_from_drop_down(element='order:article', item_text=article)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:article', random=True)
            return self.get_article()

    def is_article_existing(self, article):
        return self.base_selenium.check_item_in_items(element='order:article', item_text=article)


