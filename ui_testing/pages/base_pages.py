from uuid import uuid4
from ui_testing.pages.base_selenium import BaseSelenium
import time
from random import randint


class BasePages:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def generate_random_text(self):
        return str(uuid4()).replace("-", "")[:10]

    def search(self, value):
        """
        Search for a specific value
        :param value:
        :return: The first element in the search table
        """
        self.base_selenium.set_text(element='general:search', value=value)
        self.base_selenium.click(element='general:search')
        time.sleep(self.base_selenium.TIME_MEDIUM)
        return self.result_table()

    def result_table(self):
        rows = self.base_selenium.get_table_rows(element='general:table')
        if len(rows) > 0:
            return rows
        else:
            return []

    def clear_search(self):
        self.base_selenium.clear_element_text(element='general:search')

    def sleep_tiny(self):
        time.sleep(self.base_selenium.TIME_TINY)

    def sleep_small(self):
        time.sleep(self.base_selenium.TIME_SMALL)

    def sleep_medium(self):
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def sleep_large(self):
        time.sleep(self.base_selenium.TIME_LARGE)

    def save(self, sleep=True, save_btn='general:save'):
        self.base_selenium.click(element=save_btn)
        if sleep:
            time.sleep(self.base_selenium.TIME_MEDIUM)

    def cancel(self, force=True):
        self.base_selenium.click(element='general:cancel')
        self.confirm_popup(force)

    def confirm_popup(self, force=True):
        if self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'):
            if force:
                self.base_selenium.click(element='general:confirm_pop')
            else:
                self.base_selenium.click(element='general:confirm_cancel')
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def open_filter_menu(self):
        filter = self.base_selenium.find_element_in_element(source_element='general:menu_filter_view',
                                                            destination_element='general:filter')
        filter.click()

    def filter_by(self, filter_element, filter_text):
        self.open_filter_menu()
        self.base_selenium.select_item_from_drop_down(element=filter_element, item_text=filter_text)

    def filter_apply(self):
        self.base_selenium.find_element_in_element(destination_element='article:filter_apply_btn',
                                                   source_element='article:filter_actions').click()

    def filter_reset(self):
        self.base_selenium.find_element_in_element(destination_element='article:filter_reset_btn',
                                                   source_element='article:filter_actions').click()
        time.sleep(self.base_selenium.TIME_SMALL)

    def filter_result(self):
        return self.result_table()

    def select_random_multiple_table_rows(self, element='general:table'):
        _selected_rows_text = []
        selected_rows_data = []
        selected_rows = []
        rows = self.base_selenium.get_table_rows(element=element)
        no_of_rows = randint(1, 5)
        count = 0
        self.base_selenium.LOGGER.info(' * No. of selected rows {} '.format(no_of_rows))
        while count < no_of_rows:
            row = rows[randint(0, len(rows) - 1)]
            row_text = row.text
            if not row_text:
                continue
            if row_text in _selected_rows_text:
                continue
            count = count + 1
            self.click_check_box(source=row)
            _selected_rows_text.append(row_text)
            selected_rows.append(row)
            selected_rows_data.append(self.base_selenium.get_row_cells_dict_related_to_header(row=row))
        return selected_rows_data, selected_rows

    def click_check_box(self, source):
        check_box = self.base_selenium.find_element_in_element(destination_element='general:checkbox', source=source)
        check_box.click()

    def get_random_x(self, row):
        x_cells = self.base_selenium.get_row_cells(row=row)

        for x_cell in x_cells:
            if x_cell.text:
                x_cell.click()
                break
        self.sleep_medium()
