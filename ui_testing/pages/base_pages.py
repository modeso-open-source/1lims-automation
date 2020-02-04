from uuid import uuid4
from ui_testing.pages.base_selenium import BaseSelenium
import time, pyperclip, os
from random import randint
import datetime
import pymysql


class BasePages:
    def __init__(self):
        self.base_selenium = BaseSelenium()
        self.pagination_elements_array=['10', '20', '25', '50', '100']

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
        table=self.base_selenium.get_table_rows(element=element)
        return table

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
        if self.base_selenium.check_element_is_exist(element=save_btn):
            self.base_selenium.click(element=save_btn)
        else:            
            self.base_selenium.click(element='my_profile:save_button')
        if sleep:
            time.sleep(self.base_selenium.TIME_MEDIUM)

    def cancel(self, force=True):
        if self.base_selenium.check_element_is_exist(element='general:cancel'):
            self.base_selenium.click(element='general:cancel')
        else:            
            self.base_selenium.click(element='my_profile:cancel_button')
        self.confirm_popup(force)

    def confirm_popup(self, force=True):
        self.base_selenium.LOGGER.info('Confirming the popup')
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

    def apply_filter_scenario(self, filter_element, filter_text, field_type='drop_down'):
        self.open_filter_menu()
        self.base_selenium.wait_element(element=filter_element)
        self.filter_by(filter_element=filter_element, filter_text=filter_text, field_type=field_type)
        self.filter_apply()

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
        self.info(' No. of selected rows {} '.format(no_of_rows))
        while count < no_of_rows:
            self.base_selenium.scroll()
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
            row_index = randint(0, len(rows) - 1)
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
        self.sleep_small() # sleep for loading

    def open_edit_page_by_css_selector(self, row, css_selector=''):
        if css_selector == '':
            css_selector = '[title="Edit details"]'
        row.find_element_by_css_selector(css_selector).click()
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
        self.open_edit_page(row=row)

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

    def generate_random_email(self):
        name = str(uuid4()).replace("-", "")[:10]
        server = "@" + str(uuid4()).replace("-", "")[:6] + "." + 'com'

        return name+server
      
    def generate_random_website(self):
        return "www."+str(uuid4()).replace("-", "")[:10]+"."+str(uuid4()).replace("-", "")[:3]
    
    def open_configuration(self):
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='general:configurations')
        self.sleep_medium()
        
    def open_configure_table(self):
        self.base_selenium.LOGGER.info('open configure table')
        configure_table_menu = self.base_selenium.find_element(element='general:configure_table')
        configure_table_menu.click()
        self.sleep_small()

    
    def hide_columns(self, random=True, count=3, index_arr=[], always_hidden_columns=[]):
        self.open_configure_table()
        total_columns = self.base_selenium.find_elements_in_element(source_element='general:configure_table_items', destination_element='general:li')
        # total_columns = self.base_selenium.find_element_by_xpath(xpath='//ul[@class="m-nav sortable sortable-table1 ui-sortable"]').find_elements_by_tag_name('li')
        random_indices_arr = index_arr
        hidden_columns_names = []
        if random:
            random_indices_arr = self.generate_random_indices(max_index=len(total_columns)-2, count=count)

        for index in random_indices_arr:
            if total_columns[index].get_attribute('id') and total_columns[index].get_attribute('id') != 'id' and total_columns[index].get_attribute('id') not in always_hidden_columns:
                column_name = self.change_column_view(column=total_columns[index], value=False, always_hidden_columns=always_hidden_columns)
                if column_name != '':
                    hidden_columns_names.append(column_name)

        
        self.press_apply_in_configure_table()
        self.base_selenium.LOGGER.info(hidden_columns_names)
        return hidden_columns_names

    def change_column_view(self, column, value, always_hidden_columns=[]):
        if column.get_attribute('id') and column.get_attribute('id') != 'id' and column.get_attribute('id') not in always_hidden_columns  :
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
                self.base_selenium.LOGGER.info("element with the id '{}' doesn't  exit in the configure table".format(column.get_attribute('id')))
                self.base_selenium.LOGGER.exception(' * %s Exception ' % (str(e)))
                return ''


    def generate_random_indices(self, max_index=3, count=3):
        counter = 0
        indices_arr = []
        while counter < count:
            random_index = self.generate_random_number(lower=0, upper=max_index-1)
            if random_index not in indices_arr:
                indices_arr.append(random_index)
                counter = counter +1
        
        return indices_arr

    def press_apply_in_configure_table(self):
        apply_button = self.base_selenium.find_element(element="general:apply_configure_table")
        if apply_button:
            apply_button.click()
            
    def set_all_configure_table_columns_to_specific_value(self, value=True, always_hidden_columns=['']):
        self.open_configure_table()
        total_columns = self.base_selenium.find_elements_in_element(source_element='general:configure_table_items', destination_element='general:li')
        for column in total_columns:
            self.change_column_view(column=column, value=True, always_hidden_columns=always_hidden_columns)
        self.press_apply_in_configure_table()

    def deselect_all_configurations(self):
        self.open_configure_table()
        active_columns = self.base_selenium.find_elements_in_element(source_element='general:configure_table_items',
                                                                     destination_element='general:li')
        for column in active_columns:
            if column.text:
                self.change_column_view(column=column, value=False)

        archived_coloums = self.base_selenium.find_elements_in_element(
            source_element='general:configure_table_archive_items',
            destination_element='general:li')
        for column in archived_coloums:
            if column.text:
                self.change_column_view(column=column, value=False)

        return self.base_selenium.element_is_displayed(element="general:apply_configure_table")

    def click_overview(self):
        # click on Overview, this will display an alert to the user
        self.base_selenium.LOGGER.info('click on Overview')
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
        self.base_selenium.LOGGER.info('Selecting the row')
        self.click_check_box(source=row[0])
        self.sleep_small()
        self.base_selenium.LOGGER.info('Archiving the selected row')
        self.archive_selected_items()
        self.base_selenium.LOGGER.info('Navigating to the Archived table')
        self.get_archived_items()

        # try to delete it
        archived_row = self.search(item_name)
        self.sleep_small()
        self.base_selenium.LOGGER.info('Selecting the row')
        self.click_check_box(source=archived_row[0])
        self.sleep_small()
        self.base_selenium.LOGGER.info('Attempting to delete item: {}'.format(item_name))
        self.delete_selected_item()

        if self.base_selenium.check_element_is_exist(element='general:cant_delete_message'):
            self.base_selenium.click(element='general:confirm_pop')
            return False
        return True

    def open_connection_with_database(self):
        db = pymysql.connect(host='52.28.249.166', user='root', passwd='modeso@test', database='automation')
        cursor = db.cursor()
        return cursor, db

    def close_connection_with_database(self, db):
        db.close()

    def is_next_page_button_enabled(self, element='general:next_page'):
        _class = self.base_selenium.get_attribute('general:next_page', 'class')
        if 'disabled' in _class:
            return False
        else:
            return True
        
    def upload_file(self, file_name, drop_zone_element, save=True, remove_current_file=False):
        """
        Upload single file to a page that only have 1 drop zone
        
        
        :param file_name: name of the file to be uploaded
        :param drop_zone_element: the dropZone element 
        :return:
        """
        self.base_selenium.LOGGER.info("+ Uploading file")

        # remove the current file and save
        if remove_current_file:
            self.base_selenium.LOGGER.info("Remove current file")
            is_the_file_exist = self.base_selenium.check_element_is_exist(
            element='general:file_upload_success_flag')
            if is_the_file_exist:
                self.base_selenium.click('general:remove_file')
                self.save()      
            else:
                self.base_selenium.LOGGER.info("There is no current file")

        # get the absolute path of the file
        file_path = os.path.abspath('ui_testing/assets/{}'.format(file_name))

        # check if the file exist
        if os.path.exists(file_path) == False:
            raise Exception(
                "The file you are trying to upload doesn't exist localy")
        else:
            self.base_selenium.LOGGER.info(
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
        file_field = self.base_selenium.find_element(
            element='general:file_input_field')

        # send the path of the file to the input tag
        file_field.send_keys(file_path)

        self.base_selenium.LOGGER.info("Uploading {}".format(file_name))

        # wait until the file uploads
        self.base_selenium.wait_until_element_located(
            element='general:file_upload_success_flag')

        self.base_selenium.LOGGER.info(
            "{} file is uploaded successfully".format(file_name))

        # save the form or cancel
        if save:
            self.save()
            # show the file name
            self.base_selenium.driver.execute_script("document.querySelector('.dz-details').style.opacity = 'initial';")
            # get the file name
            uploaded_file_name = self.base_selenium.find_element(element='general:uploaded_file_name').text
            return uploaded_file_name
        else:
            self.cancel(True)
            return True

    def open_pagination_menu(self):
        self.base_selenium.wait_element(element='general:pagination_button')
        self.base_selenium.click(element='general:pagination_button')

    def set_page_limit(self, limit='20'):
        self.base_selenium.LOGGER.info('set the pagination limit to {}'.format(limit))
        self.open_pagination_menu()
        limit_index = self.pagination_elements_array.index(limit)
        self.base_selenium.wait_element(element='general:pagination_menu')
        pagination_elements = self.base_selenium.find_elements_in_element(source_element='general:pagination_menu', destination_element='general:li')
        if limit_index >= 0:
            pagination_elements[limit_index].click()
        time.sleep(self.base_selenium.TIME_MEDIUM)
        
        

    def get_current_pagination_limit(self):
        return self.base_selenium.find_element(element='general:pagination_button').text.split('\n')[0]

    # eslam, i'll need your check on this function
    def wait_for_loading_msg(self):
        self.base_selenium.LOGGER.info('wait for loading msg to disappear')
        self.base_selenium.wait_element('general:loading_msg')
        self.base_selenium.wait_until_element_is_not_displayed('general:loading_msg')

    def get_table_info_data(self):
        self.base_selenium.LOGGER.info('get table information')
        table_info = self.base_selenium.find_element('general:table_info')
        table_info_data = table_info.text
        table_info_elements = table_info_data.split(' ')
        start = table_info_elements[1]
        end = table_info_elements[3]
        count = table_info_elements[5]
        page_limit = str((int(end) - int(start)) +1)
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
        
    def get_current_date_formated(self):
        current_time = datetime.datetime.now()
        date = str(current_time.year)+'-'+str(current_time.month)+'-'+str(current_time.day)
        return date

    def get_current_year(self):
        current_year = datetime.datetime.now()
        return str(current_year.year)

    def get_the_latest_row_data(self):
        latest_row = (self.result_table()[0])
        return self.base_selenium.get_row_cells_dict_related_to_header(latest_row)