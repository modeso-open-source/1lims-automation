from ui_testing.pages.base_pages import BasePages
from random import randint


class Orders(BasePages):
    def __init__(self):
        super().__init__()
        self.orders_url = "{}orders".format(self.base_selenium.url)

    def get_orders_page(self):
        self.base_selenium.get(url=self.orders_url)

    def get_random_orders(self):
        row = self.base_selenium.get_table_rows(element='orders:orders_table')
        self.get_random_x(row=row)

    def click_create_order_button(self):
        self.base_selenium.click(element='orders:new_order')
        self.sleep_small()
