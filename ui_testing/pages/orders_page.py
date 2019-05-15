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
        row_id = randint(1, len(row) - 1)
        row = row[row_id]
        orders_edit_button = self.base_selenium.find_element_in_element(source=row,
                                                                        destination_element='orders:orders_edit_button')
        orders_edit_button.click()
        self.sleep_medium()

    def click_create_order_button(self):
        self.base_selenium.click(element='orders:new_order')
        self.sleep_small()

    def archive_selected_orders(self, check_pop_up = False):
        self.base_selenium.scroll()
        self.base_selenium.click(element='orders:right_menu')
        self.base_selenium.click(element='orders:archive')
        self.confirm_popup()
        if check_pop_up:
            if self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'):
                return False
        return True    
