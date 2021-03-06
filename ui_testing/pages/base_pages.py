from uuid import uuid4
from ui_testing.pages.base_selenium import BaseSelenium
import time, pyperclip, os
from random import randint
import datetime
import pymysql


class BasePages:
    def __init__(self):
        self.base_selenium = BaseSelenium()
        self.pagination_elements_array = ['10', '20', '25', '50', '100']

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
        table = self.base_selenium.get_table_rows(element=element)
        return table

    def clear_text(self, element):
        self.base_selenium.clear_element_text(element=element)

    def sleep_tiny(self):
        self.base_selenium.LOGGER.debug('wait up to 0.5 sec')
        self.base_selenium.wait_until_page_load_resources(expected_counter=5)

    def sleep_small(self):
        self.base_selenium.LOGGER.debug('wait up to 1 sec')
        self.base_selenium.wait_until_page_load_resources(expected_counter=10)

    def sleep_medium(self):
        self.base_selenium.LOGGER.debug('wait up to 2 sec')
        self.base_selenium.wait_until_page_load_resources(expected_counter=20)

    def sleep_large(self):
        self.base_selenium.LOGGER.debug('wait up to 4 sec')
        self.base_selenium.wait_until_page_load_resources(expected_counter=40)

    def save(self, sleep=True, save_btn='general:save', logger_msg='save the changes'):
        self.info(logger_msg)
        if sleep:
            self.sleep_tiny()
        self.base_selenium.click(element=save_btn)
        if sleep:
            self.sleep_tiny()

    def save_and_wait(self, save_btn='general:save'):
        self.save(save_btn=save_btn)
        self.info('Refresh to make sure that data are saved correctly')
        self.base_selenium.refresh()
        self.wait_until_page_is_loaded()

    def cancel(self, force=True):
        if self.base_selenium.check_element_is_exist(element='general:cancel'):
            self.base_selenium.click(element='general:cancel')
        else:
            self.base_selenium.click(element='my_profile:cancel_button')
        self.confirm_popup(force)

    def confirm_popup(self, force=True, check_only=False):
        """
        :param check_only: this parameter (when true) is to check the existence of popup only without clicking ok/cancel
        """
        self.info('confirming the popup')
        if self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'):
            if check_only:
                return True
            if force:
                self.base_selenium.click(element='general:confirm_pop')
            else:
                self.base_selenium.click(element='general:confirm_cancel')
        self.sleep_small()

    def get_confirmation_pop_up_text(self):
        if self.base_selenium.wait_element(element='general:confirmation_pop_up'):
            return self.base_selenium.get_text(element='general:confirmation_pop_up')

    def open_filter_menu(self):
        self.info('open Filter')
        filter = self.base_selenium.find_element_in_element(source_element='general:menu_filter_view',
                                                            destination_element='general:filter')
        filter.click()

    def close_filter_menu(self):
        filter = self.base_selenium.find_element_in_element(source_element='general:menu_filter_view',
                                                            destination_element='general:filter')
        filter.click()

    def filter_by(self, filter_element, filter_text, field_type='drop_down'):
        if field_type == 'drop_down':
            self.base_selenium.select_item_from_drop_down(element=filter_element,
                                                          item_text=filter_text, avoid_duplicate=True)
        else:
            self.base_selenium.set_text(element=filter_element, value=filter_text)

    def filter_apply(self):
        self.base_selenium.click(element='general:filter_btn')
        self.wait_until_page_is_loaded()

    def apply_filter_scenario(self, filter_element, filter_text, field_type='drop_down'):
        self.open_filter_menu()
        self.sleep_tiny()
        self.base_selenium.wait_element(element=filter_element)
        self.filter_by(filter_element=filter_element, filter_text=filter_text, field_type=field_type)
        self.filter_apply()
        self.sleep_tiny()

    def filter_reset(self):
        self.info(' Reset Filter')
        self.base_selenium.click(element='general:filter_reset_btn')
        time.sleep(self.base_selenium.TIME_SMALL)

    def select_random_multiple_table_rows(self, element='general:table'):
        _selected_rows_text = []
        selected_rows_data = []
        selected_rows = []
        rows = self.base_selenium.get_table_rows(element=element)
        no_of_rows = randint(min(2, len(rows) - 1), min(5, len(rows) - 1))
        count = 0
        self.info(' No. of selected rows {} '.format(no_of_rows))
        while count < no_of_rows:
            self.base_selenium.scroll()
            row = rows[randint(0, len(rows) - 2)]
            row_text = row.text
            if not row_text:
                continue
            if row_text in _selected_rows_text:
                continue
            count = count + 1
            self.click_check_box(source=row)
            self.sleep_tiny()
            _selected_rows_text.append(row_text)
            selected_rows.append(row)
            selected_rows_data.append(self.base_selenium.get_row_cells_dict_related_to_header(row=row))
        return selected_rows_data, selected_rows

    def select_random_ordered_multiple_table_rows(self, element='general:table'):
        _selected_rows_text = []
        selected_rows_data = []
        selected_rows = []
        rows = self.base_selenium.get_table_rows(element=element)
        no_of_rows = randint(min(2, len(rows)-1), min(5, len(rows)-1))
        count = 0
        self.info(' No. of selected rows {} '.format(no_of_rows))
        while count < no_of_rows:
            self.base_selenium.scroll()
            row = rows[count]

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
            row_index = randint(0, len(rows) - 2)
            row = rows[row_index]
            row_text = row.text
            if not row_text:
                continue
            self.click_check_box(source=row)
            return self.base_selenium.get_row_cells_dict_related_to_header(row)

    def click_check_box(self, source):
        check_box = self.base_selenium.find_element_in_element(
            destination_element='general:checkbox', source=source)
        check_box.click()

    def open_edit_page(self, row, xpath=''):
        if xpath == '':
            xpath = '//span[@class="mr-auto"]/a'
        row.find_element_by_xpath(xpath).click()
        self.wait_until_page_is_loaded()

    def open_edit_page_by_css_selector(self, row, css_selector=''):
        if css_selector == '':
            css_selector = '[title="Edit details"]'
        row.find_element_by_css_selector(css_selector).click()
        self.wait_until_page_is_loaded()

    def get_archived_items(self):
        self.sleep_tiny()
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archived')
        self.sleep_tiny()

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
        self.sleep_tiny()

    def delete_selected_item(self, confirm_pop_up=True):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:delete')
        if confirm_pop_up:
            self.confirm_popup()

    def archive_selected_items(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:archive')
        self.confirm_popup()
        self.sleep_tiny()

    def download_xslx_sheet(self):
        self.info("download XSLX sheet")
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
        self.open_edit_page(row=row)

    def get_random_table_row(self, table_element):
        rows = self.base_selenium.get_table_rows(element=table_element)
        if len(rows) > 1:
            row_id = randint(0, len(rows) - 2)
            row = rows[row_id]
            return row
        return ''

    def get_table_info(self):
        return self.base_selenium.get_text(element='general:table_info')

    def get_table_records(self):
        self.info(' Get table records.')
        return int(self.get_table_info().split(' ')[5])

    def get_random_date(self):
        return '{:02d}.{:02d}.{}'.format(randint(1, 30), randint(1, 12), 2019)

    def filter(self, field_name, element, filter_text, type):
        self.info(' Filter by {} : {}'.format(field_name, filter_text))
        self.filter_by(filter_element=element, filter_text=filter_text, field_type=type)
        self.filter_apply()

    def _copy(self, value):
        pyperclip.copy(value)

    def _paste(self, element):
        self.info(' past. {}'.format(pyperclip.paste()))
        self.base_selenium.paste(element=element)

    def copy_paste(self, element, value):
        self._copy(value=value)
        self._paste(element=element)

    def open_row_options(self, row):
        self.info('open record options menu')
        row_options = self.base_selenium.find_element_in_element(
            destination_element='general:table_menu_options', source=row)
        row_options.click()
        self.sleep_tiny()

    def open_child_table(self, source):
        childtable_arrow = self.base_selenium.find_element_in_element(
            destination_element='general:child_table_arrow', source=source)
        childtable_arrow.click()
        self.sleep_medium()

    def close_child_table(self, source):
        childtable_arrow = self.base_selenium.find_element_in_element(
            destination_element='general:child_table_arrow', source=source)
        childtable_arrow.click()

    def get_child_table_data(self, index=0, open_child=True):
        rows = self.result_table()
        if open_child:
            self.open_child_table(source=rows[index])
        return self.get_table_data()

    def get_table_data(self, table_element='general:table_child'):
        rows_with_childtable = self.result_table(element=table_element)
        headers = self.base_selenium.get_table_head_elements(element=table_element)

        child_table_data = []
        for subrecord in range(0, len(rows_with_childtable)):
            rows_with_headers = self.base_selenium.get_row_cells_dict_related_to_header(
                row=rows_with_childtable[subrecord], table_element='general:table_child')
            if rows_with_headers != {}:
                child_table_data.append(rows_with_headers)

        return child_table_data

    @property
    def info(self):
        return self.base_selenium.LOGGER.info

    @property
    def debug(self):
        return self.base_selenium.LOGGER.debug

    def generate_random_email(self):
        name = str(uuid4()).replace("-", "")[:10]
        server = "@" + str(uuid4()).replace("-", "")[:6] + "." + 'com'

        return name + server

    def generate_random_website(self):
        return "www." + str(uuid4()).replace("-", "")[:10] + "." + str(uuid4()).replace("-", "")[:3]

    def generate_random_string(self):
        return str(uuid4()).replace("-", "")[:10]

    def generate_random_number(self, lower=1, upper=100000):
        return randint(lower, upper)

    def open_configuration(self):
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:configurations')
        self.base_selenium.wait_until_element_located(element='general:fields_panel')

    def open_archived_configuration(self):
        self.open_configuration()
        self.sleep_tiny()
        self.base_selenium.click(element='general:configurations_archived')

    def open_analysis_configuration(self):
        self.base_selenium.refresh()
        self.sleep_tiny()
        self.open_configuration()
        self.sleep_tiny()
        self.base_selenium.click(element='general:configurations_analysis')

    def open_configure_table(self):
        self.info('open configure table')
        configure_table_menu = self.base_selenium.find_element(element='general:configure_table')
        configure_table_menu.click()
        self.sleep_tiny()

    def close_configure_table(self):
        self.info('open configure table')
        configure_table_menu = self.base_selenium.find_element(element='general:configure_table')
        configure_table_menu.click()

    def navigate_to_child_table_configuration(self):
        self.open_configure_table()
        configure_child_table_menu = self.base_selenium.find_element(element='general:configure_child_table')
        configure_child_table_menu.click()
        self.sleep_tiny()
        active_columns = self.base_selenium.find_elements_in_element(
            source_element='general:configure_child_table_items', destination_element='general:li')
        coulmns_text = [column.text for column in active_columns]
        self.close_configure_table()
        return coulmns_text

    def hide_columns(self, random=True, count=3, index_arr=[], always_hidden_columns=[]):
        self.open_configure_table()
        total_columns = self.base_selenium.find_elements_in_element(source_element='general:configure_table_items',
                                                                    destination_element='general:li')
        # total_columns = self.base_selenium.find_element_by_xpath(xpath='//ul[@class="m-nav sortable sortable-table1 ui-sortable"]').find_elements_by_tag_name('li')
        random_indices_arr = index_arr
        hidden_columns_names = []
        if random:
            random_indices_arr = self.generate_random_indices(max_index=len(total_columns) - 2, count=count)

        for index in random_indices_arr:
            if total_columns[index].get_attribute('id') and total_columns[index].get_attribute('id') != 'id' and \
                    total_columns[index].get_attribute('id') not in always_hidden_columns:
                column_name = self.change_column_view(column=total_columns[index], value=False,
                                                      always_hidden_columns=always_hidden_columns)
                if column_name != '':
                    hidden_columns_names.append(column_name)

        self.press_apply_in_configure_table()
        self.info(hidden_columns_names)
        return hidden_columns_names

    def change_column_view(self, column, value, always_hidden_columns=[]):
        if column.get_attribute('id') and column.get_attribute('id') != 'id' and column.get_attribute(
                'id') not in always_hidden_columns:
            try:
                new_checkbox_value = "//li[@id='" + column.get_attribute('id') + "']//input[@type='checkbox']"
                new_label_xpath = "//li[@id='" + column.get_attribute('id') + "']//label[@class='sortable-label']"
                new_checkbox_xpath = "//li[@id='" + column.get_attribute('id') + "']//span[@class='checkbox']"
                column_name = self.base_selenium.find_element_by_xpath(new_label_xpath).text
                checkbox = self.base_selenium.find_element_by_xpath(new_checkbox_xpath)
                checkbox_value = self.base_selenium.find_element_by_xpath(new_checkbox_value)
                if checkbox_value.is_selected() != value:
                    checkbox.click()
                    return column_name
            except Exception as e:
                self.info(
                    "element with the id '{}' doesn't  exit in the configure table".format(column.get_attribute('id')))
                self.base_selenium.LOGGER.exception(' * %s Exception ' % (str(e)))
                return ''

    def set_specific_configure_table_column_to_specific_value(self, fields=[''], value=True, child=False,
                                                              element='general:configure_table_items'):
        """
        :param fields: list of items to select or deslect in table
        :param value: True to select, False to deselect
        :param child: true if want child table
        :param element: configure_child_table_items if child table selected
        :return:
        """
        self.open_configure_table()
        if child:
            self.base_selenium.click(element='general:configure_child_table')
        total_columns = self.base_selenium.find_elements_in_element(
            source_element=element, destination_element='general:li')
        for column in total_columns:
            if column.text in fields:
                self.change_column_view(column=column, value=value)
        self.press_apply_in_configure_table()
        self.sleep_tiny()
        self.base_selenium.refresh()
        self.sleep_tiny()
        if child:
            self.open_child_table(self.result_table()[0])
            headers = self.base_selenium.get_table_head_elements(element='general:table_child')
            child_table_headings = [i.text for i in headers]
            return child_table_headings
        else:
            return self.base_selenium.get_table_head_elements_with_tr(element='general:table')[0].text.split('\n')

    def generate_random_indices(self, max_index=3, count=3):
        counter = 0
        indices_arr = []
        while counter < count:
            random_index = self.generate_random_number(lower=0, upper=max_index - 1)
            if random_index not in indices_arr:
                indices_arr.append(random_index)
                counter = counter + 1

        return indices_arr

    def press_apply_in_configure_table(self):
        apply_button = self.base_selenium.find_element(element="general:apply_configure_table")
        if apply_button:
            apply_button.click()

    def set_all_configure_table_columns_to_specific_value(self, value=True, always_hidden_columns=['']):
        self.open_configure_table()
        total_columns = self.base_selenium.find_elements_in_element(
            source_element='general:configure_table_items',
            destination_element='general:li')
        for column in total_columns:
            self.change_column_view(column=column, value=value, always_hidden_columns=always_hidden_columns)
        self.press_apply_in_configure_table()

    def deselect_all_configurations(self):
        self.open_configure_table()
        self.info('deselect all configuration')
        active_columns = self.base_selenium.find_elements_in_element(
            source_element='general:configure_table_items', destination_element='general:li')
        for column in active_columns:
            if column.text:
                self.change_column_view(column=column, value=False)

        archived_coloums = self.base_selenium.find_elements_in_element(
            source_element='general:configure_table_archive_items', destination_element='general:li')
        for column in archived_coloums:
            if column.text:
                self.change_column_view(column=column, value=False)
        parent_class = self.base_selenium.driver.find_element_by_xpath('//*[contains(text(), "Apply")]//parent::a')
        class_string = parent_class.get_attribute('class')
        if 'disabled' in class_string:
            self.info("can't apply")
            return False
        else:
            self.info("can apply")
            return True

    def click_overview(self):
        # click on Overview, this will display an alert to the user
        self.base_selenium.scroll()
        self.info('click on Overview')
        self.base_selenium.click_by_script(element='general:overview')
        self.sleep_tiny()

    def confirm_overview_pop_up(self):
        self.base_selenium.click(element='general:confirm_overview')
        self.sleep_tiny()

    def cancel_overview_pop_up(self):
        self.base_selenium.click(element='general:cancel_overview')
        self.sleep_tiny()

    def duplicate_selected_item(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:duplicate')
        self.sleep_small()

    '''
    archives this item and tries to delete it
    returns True if it's deleted and False otherwise
    '''

    def delete_selected_item_from_active_table_and_from_archived_table(self, item_name):

        # archive this item
        row = self.search(item_name)
        self.info('Selecting the row')
        self.click_check_box(source=row[0])
        self.sleep_small()
        self.info('Archiving the selected row')
        self.archive_selected_items()
        self.info('Navigating to the Archived table')
        self.get_archived_items()

        # try to delete it
        archived_row = self.search(item_name)
        self.sleep_small()
        self.info('Selecting the row')
        self.click_check_box(source=archived_row[0])
        self.sleep_small()
        self.info('Attempting to delete item: {}'.format(item_name))
        self.delete_selected_item()

        if self.base_selenium.check_element_is_exist(element='general:cant_delete_message'):
            self.base_selenium.click(element='general:confirm_pop')
            return False
        return True

    def is_next_page_button_enabled(self, element='general:next_page'):
        _class = self.base_selenium.get_attribute('general:next_page', 'class')
        if 'disabled' in _class:
            return False
        else:
            return True

    def upload_file(self, file_name, drop_zone_element, remove_current_file=False, save=True):
        """
        Upload single file to a page that only have 1 drop zone


        :param file_name: name of the file to be uploaded
        :param drop_zone_element: the dropZone element
        :return:
        """
        self.info(" uploading file")

        # remove the current file and save
        if remove_current_file:
            self.info(" remove current file")
            is_the_file_exist = self.base_selenium.check_element_is_exist(element='general:file_upload_success_flag')
            if is_the_file_exist:
                self.sleep_tiny()
                self.base_selenium.click('general:remove_file')
                self.base_selenium.click('general:close_uploader_popup')
                if save:
                    self.save()
            else:
                self.info(" there is no current file")

        # get the absolute path of the file
        file_path = os.path.abspath('ui_testing/assets/{}'.format(file_name))

        # check if the file exist
        if os.path.exists(file_path) == False:
            raise Exception(
                "The file you are trying to upload doesn't exist localy")
        else:
            self.info(
                "The {} file is ready for upload".format(file_name))

        # silence the click event of file input to prevent the opening of (Open  Files) Window
        self.base_selenium.driver.execute_script(
            """
            HTMLInputElement.prototype.click = function() {
                if(this.type !== 'file') 
                {
                    HTMLElement.prototype.click.call(this); 
                }
            }
            """)

        # click on the dropZone component
        self.base_selenium.click(element=drop_zone_element)

        # the input tag will be appended to the HTML by dropZone after the click
        # find the <input type="file"> tag
        file_field = self.base_selenium.find_element(element='general:file_input_field')

        # send the path of the file to the input tag
        file_field.send_keys(file_path)
        self.info("Uploading {}".format(file_name))
        # wait until the file uploads
        self.base_selenium.wait_until_element_located(element='general:file_upload_success_flag')
        self.info(
            "{} file is uploaded successfully".format(file_name))

    def open_pagination_menu(self):
        self.base_selenium.wait_element(element='general:pagination_button')
        self.base_selenium.click(element='general:pagination_button')

    def set_page_limit(self, limit='20'):
        self.info('set the pagination limit to {}'.format(limit))
        self.open_pagination_menu()
        limit_index = self.pagination_elements_array.index(limit)
        self.base_selenium.wait_element(element='general:pagination_menu')
        pagination_elements = self.base_selenium.find_elements_in_element(source_element='general:pagination_menu',
                                                                          destination_element='general:li')
        if limit_index >= 0:
            pagination_elements[limit_index].click()
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def get_current_pagination_limit(self):
        return self.base_selenium.find_element(element='general:pagination_button').text.split('\n')[0]

    def wait_until_page_is_loaded(self):
        self.debug('wait until page is loaded')
        self.base_selenium.wait_until_element_is_not_displayed('general:loading')
        self.sleep_tiny()

    def get_table_info_data(self):
        self.info('get table information')
        table_info = self.base_selenium.find_element('general:table_info')
        table_info_data = table_info.text
        table_info_elements = table_info_data.split(' ')
        start = table_info_elements[1]
        end = table_info_elements[3]
        count = table_info_elements[5]
        page_limit = str((int(end) - int(start)) + 1)
        current_pagination_limit = self.get_current_pagination_limit()
        return {'start': start,
                'end': end,
                'count': count,
                'page_limit': page_limit,
                'pagination_limit': current_pagination_limit
                }

    def convert_to_dot_date_format(self, date):
        date_in_days = date[0:10]
        date_parameters = date_in_days.split('-')
        date_parameters.reverse()
        return '.'.join(date_parameters)

    def get_the_latest_row_data(self):
        latest_row = (self.result_table()[0])
        return self.base_selenium.get_row_cells_dict_related_to_header(latest_row)

    def open_connection_with_database(self):
        db = pymysql.connect(host='52.28.249.166', user='root', passwd='modeso@test', database='automation')
        cursor = db.cursor()
        return cursor, db

    def close_connection_with_database(self, db):
        db.close()

    def get_current_year(self):
        current_year = datetime.datetime.now()
        return str(current_year.year)
