from uuid import uuid4
from ui_testing.pages.base_selenium import BaseSelenium
import time, pyperclip
from random import randint


class BasePages:
    def __init__(self):
        self.base_selenium = BaseSelenium()

    def generate_random_text(self):
        return str(uuid4()).replace("-", "")[:10]

    def generate_random_number(self, lower=1, upper=100000):
        return randint(lower, upper)

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

    def result_table(self, element='general:table'):
        return self.base_selenium.get_table_rows(element=element)

    def clear_text(self, element):
        self.base_selenium.clear_element_text(element= element)

    def sleep_tiny(self):
        self.base_selenium.LOGGER.info(' Tiny sleep.')
        time.sleep(self.base_selenium.TIME_TINY)

    def sleep_small(self):
        self.base_selenium.LOGGER.info(' Small sleep.')
        time.sleep(self.base_selenium.TIME_SMALL)

    def sleep_medium(self):
        self.base_selenium.LOGGER.info(' Medium sleep.')
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def sleep_large(self):
        self.base_selenium.LOGGER.info(' Large sleep.')
        time.sleep(self.base_selenium.TIME_LARGE)

    def save(self, sleep=True, save_btn='general:save', logger_msg='save the changes'):
        self.base_selenium.LOGGER.info(logger_msg)
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
        self.base_selenium.LOGGER.info(' Open Filter')
        filter = self.base_selenium.find_element_in_element(source_element='general:menu_filter_view',
                                                            destination_element='general:filter')
        filter.click()

    def filter_by(self, filter_element, filter_text, field_type='drop_down'):
        if field_type=='drop_down':
            self.base_selenium.select_item_from_drop_down(element=filter_element, item_text=filter_text)
        else:
            self.base_selenium.set_text(element=filter_element, value = filter_text )

    def filter_apply(self):
        self.base_selenium.click(element='general:filter_btn')
        time.sleep(self.base_selenium.TIME_SMALL)

    def filter_reset(self):
        self.base_selenium.LOGGER.info(' Reset Filter')
        self.base_selenium.click(element='general:filter_reset_btn')
        time.sleep(self.base_selenium.TIME_SMALL)

    def select_random_multiple_table_rows(self, element='general:table'):
        _selected_rows_text = []
        selected_rows_data = []
        selected_rows = []
        rows = self.base_selenium.get_table_rows(element=element)
        no_of_rows = randint(min(1, len(rows)-1), min(5, len(rows)-1))
        count = 0
        self.base_selenium.LOGGER.info(' No. of selected rows {} '.format(no_of_rows))
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

    def select_random_table_row(self, element='general:table'):
        self.info("select random row")
        rows = self.base_selenium.get_table_rows(element=element)
        for _ in range(5):
            row = rows[randint(0, len(rows) - 1)]
            row_text = row.text
            if not row_text:
                continue
            self.click_check_box(source=row)
            return self.base_selenium.get_row_cells_dict_related_to_header(row)

    def click_check_box(self, source):
        check_box = self.base_selenium.find_element_in_element(
            destination_element='general:checkbox', source=source)
        check_box.click()

    def get_random_x(self, row):
        # x_cells = self.base_selenium.get_row_cells(row=row)
        #
        # for x_cell in x_cells:
        #     if x_cell.text:
        #         x_cell.click()
        #         break
        # self.sleep_medium()
        row.find_element_by_xpath('//span/a[@title="Edit details"]').click()
        self.sleep_small() # sleep for loading

    def get_archived_items(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archived')
        self.sleep_small()

    def get_active_items(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:active')
        self.sleep_small()

    def restore_selected_items(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:restore')
        self.confirm_popup()

    def delete_selected_item(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:delete')
        self.confirm_popup()

    def archive_selected_items(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archive')
        self.confirm_popup()

    def download_xslx_sheet(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.sheet = self.base_selenium.download_excel_file(element='general:xslx')

    def select_all_records(self):
        header_row = self.base_selenium.get_table_head_elements(element='general:table')
        self.click_check_box(source=header_row[0])

    def get_table_rows_data(self):
        return [row.text for row in self.base_selenium.get_table_rows(element='general:table')]                      

    def open_random_table_row_page(self, table_element):
        row = self.get_random_table_row(table_element)
        self.get_random_x(row=row)

    def get_random_table_row(self, table_element):
        rows = self.base_selenium.get_table_rows(element=table_element)
        row_id = randint(0, len(rows) - 2)
        row = rows[row_id]
        return row

    def get_table_info(self):
        return self.base_selenium.get_text(element='general:table_info')

    def get_table_records(self):
        self.base_selenium.LOGGER.info(' Get table records.')
        return int(self.get_table_info().split(' ')[5])

    def get_random_date(self):
        return '{:02d}.{:02d}.{}'.format(randint(1, 30), randint(1, 12), 2019)

    def filter(self,field_name, element, filter_text, type):
        self.base_selenium.LOGGER.info(' Filter by {} : {}'.format(field_name,filter_text))
        self.filter_by(filter_element= element, filter_text=filter_text, field_type = type)
        self.filter_apply()

    def _copy(self, value):
        pyperclip.copy(value)

    def _paste(self, element):
        self.base_selenium.LOGGER.info(' past. {}'.format(pyperclip.paste()))
        self.base_selenium.paste(element=element)

    def copy_paste(self, element, value):
        self._copy(value=value)
        self._paste(element=element)

    def open_child_table(self, source):
        childtable_arrow = self.base_selenium.find_element_in_element(destination_element='general:child_table_arrow', source=source)
        childtable_arrow.click()
        self.sleep_medium()

    def get_child_table_data(self, index=0):
        rows = self.result_table()
        self.open_child_table(source=rows[index])
        rows_with_childtable = self.result_table(element='general:table_child')
        headers = self.base_selenium.get_table_head_elements(element='general:table_child')

        child_table_data = []
        for subrecord in range(0,len(rows_with_childtable)):
            rows_with_headers=self.base_selenium.get_row_cells_dict_related_to_header(row=rows_with_childtable[subrecord], table_element='general:table_child')
            if rows_with_headers != {}:
                child_table_data.append(rows_with_headers)

        return child_table_data

    def info(self, message):
        self.base_selenium.LOGGER.info(message)
