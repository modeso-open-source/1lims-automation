from ui_testing.pages.orders_page import Orders
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random


class Order(Orders):
    def get_order_id(self):
        current_splited_url = self.base_selenium.get_url().split('/')
        order_id = current_splited_url[(len(current_splited_url) - 1)]
        return order_id

    def navigate_to_analysis_tab(self):
        self.base_selenium.scroll()
        self.base_selenium.click('orders:analysis_order_tab')
        self.wait_until_page_is_loaded()

    def get_table_with_add(self):
        table = self.base_selenium.find_element(element='order:suborder_table')
        return table

    def check_suborders_appear(self):
        is_suborder_exist = self.base_selenium.check_element_is_exist(
            element='table_element=general:table_child')
        return is_suborder_exist

    def get_data_first_row(self, index=0):
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborders[index]
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        return suborders_elements

    def set_new_order(self):
        self.info('Set new order.')
        self.base_selenium.select_item_from_drop_down(element='order:order', item_text='New Order')

    def set_existing_order(self):
        self.base_selenium.select_item_from_drop_down(element='order:order', item_text='Existing Order')

    def click_auto_fill(self):
        button = self.base_selenium.find_element_in_element(source_element='order:auto_fill_container',
                                                            destination_element='order:auto_fill')
        button.click()

    def create_existing_order_check_order_no_suggestion_list(self, no):
        self.info('press on create new order button')
        self.click_create_order_button()
        self.set_existing_order()
        self.sleep_small()
        self.info('checking if the order number is in the existing order numbers list')
        return self.base_selenium.is_item_in_drop_down(element='order:existing_order_number', item_text=no)

    def get_order_no(self):
        return self.base_selenium.get_value(element="order:order_number").replace("'", "")

    def set_order_no(self, no):
        self.info('set no. {}'.format(no))
        self.base_selenium.set_text(element="order:order_number", value=no)
        self.sleep_small()
        return self.get_order_no()

    def create_existing_order_with_auto_fill(self, no=''):
        self.info('Create order from existing order')
        self.click_create_order_button()
        self.set_existing_order()
        order_no = self.set_existing_number(no)
        self.sleep_tiny()
        self.click_auto_fill()
        self.info('Order Auto filled with data from order no : {} '.format(order_no))
        return order_no

    def set_existing_number(self, no=''):
        if no:
            self.base_selenium.select_item_from_drop_down(
                element='order:existing_order_number', item_text=no)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:existing_order_number')
            return self.get_order_number_existing_order()

    def get_order_number_existing_order(self):
        return self.base_selenium.get_text(element='order:existing_order_number').split('\n')[0]

    def set_contacts(self, contacts=[''], remove_old=False):
        if remove_old:
            self.base_selenium.clear_items_in_drop_down(element='order:contact')
        if contacts:
            for name in contacts:
                self.base_selenium.select_item_from_drop_down(element='order:contact', item_text=name)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:contact', avoid_duplicate=True)
        return self.get_contacts()

    def get_contacts(self):
        """
        This function implemented with contact name configured to be searchable by "name and number"
        :return: selected contacts names only
        """
        contacts = self.base_selenium.get_text(element='order:contact').split("\n")
        all_contacts = []
        for contact in contacts:
            if "×" in contact:
                all_contacts.append(contact.replace("×", "").split(' No')[0])
        return all_contacts

    def clear_contact(self):
        if self.get_contacts():
            self.base_selenium.clear_items_in_drop_down(element='order:contact')

    def is_contact_existing(self, contact):
        self.set_contacts(contacts=[contact])
        return self.base_selenium.check_item_in_items(element='order:contact', item_text=contact)

    def duplicate_main_order_from_order_option(self, order_number):
        super().duplicate_main_order_from_order_option()
        self.set_order_no(order_number)

class SubOrders(Order):
    def get_suborder_table(self):
        self.info('Get suborder table list.')
        self.base_selenium.click(element='order:suborder_list')

    def open_suborder_edit_mode(self, suborder_index=0):
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        suborder_row.click()
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        return suborder_row

    def set_departments(self, departments=[''], remove_old=False, suborder_index=0):
        self.open_suborder_edit_mode(suborder_index)
        if remove_old and self.get_departments():
            self.base_selenium.clear_items_in_drop_down(element='order:departments')
        if departments:
            for dep in departments:
                self.base_selenium.select_item_from_drop_down(element='order:departments', item_text=dep)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:departments')
            self.sleep_small()
            return self.get_departments()

    def get_departments(self, suborder_index=0):
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        suborder_data = self.base_selenium.get_row_cells_dict_related_to_header(
            suborder_row, table_element='order:suborder_table')
        if suborder_data['Departments:'] == 'Search':
            return None
        else:
            return suborder_data['Departments:'].replace('×', '').split('\n')

    def get_department_suggestion_lists(self, open_suborder_table=False, contacts=[], index=0):
        """
        :param open_suborder_table:
                            in create mode let open_suborder_table = false
                            in edit mode let open_suborder_table = True
        :return: 2 lists , departments with contacts and departments only
        """
        if open_suborder_table:
            suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[index]
            suborder_row.click()
        department = self.base_selenium.find_element(element='order:departments')
        department.click()
        suggested_department_list = self.base_selenium.get_drop_down_suggestion_list(
            element='order:departments', item_text='', options_element='general:drop_down_div')[0].split('\n')
        departments_only_list = self.base_selenium.get_drop_down_suggestion_list(
            element='order:departments', item_text='')
        contact_dict = {'contact': '', 'departments': []}
        contact_dep_list = []
        for item in suggested_department_list:
            if item in contacts:
                if suggested_department_list.index(item) != 0:
                    contact_dep_list.append(contact_dict)
                    contact_dict = {'contact': '', 'departments': []}
                contact_dict['contact'] = item
            else:
                contact_dict['departments'].append(item)
                if suggested_department_list.index(item) == len(suggested_department_list) - 1:
                    contact_dep_list.append(contact_dict)

        return contact_dep_list, departments_only_list

    def set_material_type(self, material_type='', suborder_index=0):
        self.open_suborder_edit_mode(suborder_index)
        if material_type:
            self.base_selenium.select_item_from_drop_down(element='order:material_type', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:material_type', avoid_duplicate=True)
            self.sleep_tiny()
            return self.get_material_type()

    def get_material_type(self, suborder_index=0):
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        suborder_data = self.base_selenium.get_row_cells_dict_related_to_header(
            suborder_row, table_element='order:suborder_table')
        if suborder_data['Material Type: *'] == 'Search':
            return None
        else:
            return suborder_data['Material Type: *'].replace('\n×', '')

    def get_testplan_according_to_material_type(self, material_type, article, index=0):
        self.set_material_type(material_type=material_type, suborder_index=index)
        self.set_article(article=article)
        return self.base_selenium.get_drop_down_suggestion_list(element='order:test_plan', item_text=' ')

    def set_article(self, article='', suborder_index=0):
        if article is None:
            return
        self.open_suborder_edit_mode(suborder_index)
        if article:
            self.base_selenium.select_item_from_drop_down(element='order:article', item_text=article)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:article')
            return self.get_article()

    def get_article(self, suborder_index=0):
        """
        this function implemented while article name set to be searchable by name and number
        """
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        suborder_data = self.base_selenium.get_row_cells_dict_related_to_header(
            suborder_row, table_element='order:suborder_table')
        if suborder_data['Article: *'] == 'Search':
            return None
        else:
            return suborder_data['Article: *'].split(' No:')

    def remove_article(self, testplans=''):
        self.info('clear article data')
        self.base_selenium.clear_single_select_drop_down(element='order:article')
        if testplans:
            self.base_selenium.wait_element(element='general:form_popup_warning_window')
            self.base_selenium.click(element='general:confirmation_button')
        self.sleep_small()

    def is_article_existing(self, article, suborder_index=0):
        self.open_suborder_edit_mode(suborder_index)
        self.set_article(article=article)
        return self.base_selenium.check_item_in_items(element='order:article', item_text=article)

    def set_test_plans(self, test_plans=[''], suborder_index=0):
        self.open_suborder_edit_mode(suborder_index)
        if test_plans:
            for tp in test_plans:
                self.base_selenium.select_item_from_drop_down(element='order:test_plan', item_text=tp)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_plan')
            self.sleep_small()
            return self.get_test_plans()

    def get_test_plans(self, suborder_index=0):
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        suborder_data = self.base_selenium.get_row_cells_dict_related_to_header(
            suborder_row, table_element='order:suborder_table')

        if 'Test Plan:' in suborder_data.keys():
            key = 'Test Plan:'
        else:
            key = 'Test Plan: *'

        if suborder_data[key] == 'Search':
            return None
        else:
            return suborder_data[key].replace('×', '').split('\n')

    def clear_test_plan(self, suborder_index=0, confirm_pop_up=False):
        self.open_suborder_edit_mode(suborder_index)
        if self.get_test_plans():
            self.base_selenium.clear_items_in_drop_down(element='order:test_plan', confirm_popup=confirm_pop_up)

    def remove_testplan_by_name(self, index, testplan_name):
        suborder_table_rows = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborder_table_rows[index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_elements_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        self.base_selenium.update_item_value(item=suborder_elements_dict['testPlans'],
                                             item_text=testplan_name.replace("'", ''))

    def get_test_plans_pop_up_content(self, index=0):
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(
            row=suborders[index], table_element='order:suborder_table')

        if 'Test Plan:' in suborders_elements.keys():
            popup_element = self.base_selenium.find_element_in_element(
                source=suborders_elements['Test Plan:'], destination_element='order:testplan_popup_btn')
        else:
            popup_element = self.base_selenium.find_element_in_element(
                source=suborders_elements['Test Plan: *'], destination_element='order:testplan_popup_btn')
        popup_element.click()
        self.sleep_small()
        results = []
        elements = self.base_selenium.find_elements('order:popup_data')
        for element in elements:
            test_plan, test_units = element.text.split('\n')[0], element.text.split('\n')[1:]
            results.append({'test_plan': test_plan, 'test_units': test_units})
        return results

    def set_test_units(self, test_units=[''], remove_old=False, suborder_index=0):
        if remove_old:
            self.base_selenium.clear_items_in_drop_down(element='order:test_unit')
        self.open_suborder_edit_mode(suborder_index)
        if test_units:
            for tu in test_units:
                self.base_selenium.select_item_from_drop_down(element='order:test_unit', item_text=tu)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit')
            return self.get_test_units()

    def get_test_units(self, suborder_index=0):
        suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[suborder_index]
        suborder_data = self.base_selenium.get_row_cells_dict_related_to_header(
            suborder_row, table_element='order:suborder_table')

        if 'Test Unit:' in suborder_data.keys():
            key = 'Test Unit:'
        else:
            key = 'Test Unit: *'

        if suborder_data[key] == 'Search':
            return None
        else:
            return suborder_data[key].replace('×', '').split('\n')

    def is_testunit_existing(self, test_unit, suborder_index=0):
        self.open_suborder_edit_mode(suborder_index)
        self.set_test_units(test_units=[test_unit])
        return self.base_selenium.check_item_partially_in_items(element='order:test_unit', item_text=test_unit)

    def clear_test_unit(self, confirm=True):
        if self.get_test_units():
            self.base_selenium.clear_items_in_drop_down(element='order:test_unit', confirm_popup=confirm)

    def remove_testunit_by_name(self, index, testunit_name):
        suborder_table_rows = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborder_table_rows[index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_elements_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        self.base_selenium.update_item_value(item=suborder_elements_dict['testUnits'],
                                             item_text=testunit_name.replace("'", ''))

    def search_test_unit_not_set(self, test_unit='', suborder_index=0):
        webdriver.ActionChains(self.base_selenium.driver).send_keys(Keys.ESCAPE).perform()
        self.open_suborder_edit_mode(suborder_index)
        if self.get_test_units():
            self.info("clear test unit")
            self.clear_test_unit()
        self.info("Try to set test unit to {} and check if option exist".format(test_unit))
        is_option_exist = self.base_selenium.select_item_from_drop_down(element='order:test_unit', item_text=test_unit)
        return is_option_exist

    def get_testunit_multiple_line_properties(self):
        dom_element = self.base_selenium.find_element(element='order:test_unit')
        multiple_line_properties = dict()
        multiple_line_properties['textOverflow'] = self.base_selenium.driver.execute_script('return '
                                                                                            'window'
                                                                                            '.getComputedStyle('
                                                                                            'arguments[0], '
                                                                                            '"None").textOverflow',
                                                                                            dom_element)
        multiple_line_properties['lineBreak'] = self.base_selenium.driver.execute_script('return '
                                                                                         'window'
                                                                                         '.getComputedStyle('
                                                                                         'arguments[0], '
                                                                                         '"None").lineBreak',
                                                                                         dom_element)
        return multiple_line_properties

    def get_test_date(self, row_id=None):
        # open the row in edit mode
        suborder_table_rows = self.base_selenium.get_table_rows(
            element='order:suborder_table')
        suborder_row = suborder_table_rows[row_id]
        suborder_row.click()
        self.info('Get the test date value')
        # get the test_date field of the selected row
        test_date = self.base_selenium.find_element_by_xpath('//*[@id="date_testDate_{}"]'.format(row_id))
        return test_date.get_attribute('value')

    def set_test_date(self, date='', row_id=None):
        # set random date
        date = date or self.get_random_date()
        self.info('Set the test date value to {}'.format(date))
        # get the test_date field of the selected row
        test_date = self.base_selenium.find_element_by_xpath('//*[@id="date_testDate_{}"]'.format(row_id))
        # update the field
        test_date.clear()
        test_date.send_keys(date)
        self.sleep_small()
        return date

    def get_shipment_date(self, row_id=None):
        # open the row in edit mode
        suborder_table_rows = self.base_selenium.get_table_rows(
            element='order:suborder_table')
        suborder_row = suborder_table_rows[row_id]
        suborder_row.click()
        self.info('Get the shipment date value')
        # get the test_date field of the selected row
        shipment_date = self.base_selenium.find_element_by_xpath('//*[@id="date_shipmentDate_{}"]'.format(row_id))
        return shipment_date.get_attribute('value')

    def set_shipment_date(self, date='', row_id=None):
        # set random date
        date = date or self.get_random_date()
        self.info('Set the shipment date value to {}'.format(date))
        # get the test_date field of the selected row
        shipment_date = self.base_selenium.find_element_by_xpath('//*[@id="date_shipmentDate_{}"]'.format(row_id))
        # update the field
        shipment_date.clear()
        shipment_date.send_keys(date)
        self.sleep_small()
        return date

    def set_analysis_no(self, anaylsis_no):
        self.base_selenium.set_text(element='order:analysis_no', value=anaylsis_no)

    def create_new_order(self, material_type='', article='', contacts=[''], test_plans=[''], test_units=[''],
                         multiple_suborders=0, departments=[''], order_no='', save=True,
                         check_testunits_testplans=False):

        self.info('Create new order.')
        self.click_create_order_button()
        self.sleep_small()
        self.set_new_order()
        self.sleep_small()
        self.info("set contacts to {}".format(contacts))
        self.set_contacts(contacts=contacts)
        self.sleep_small()
        if departments:
            self.info("set departments to {}".format(departments))
            self.set_departments(departments=departments)
        self.info("set material type to {}".format(material_type))
        self.set_material_type(material_type=material_type)
        self.sleep_small()
        self.info("set article to {}".format(article))
        self.set_article(article=article)
        self.sleep_small()
        if order_no:
            self.info("set order number to {}".format(order_no))
            self.set_order_no(order_no)  # else it is autogenerated
        else:
            order_no = random.randint(999, 99999)
            order_no_with_year = str(order_no)+"-2020"
            self.set_order_no(order_no_with_year)

        order_no = self.get_order_no()
        if check_testunits_testplans:
            # return test plan and test unit suggestion list according to selected material type and article
            suggested_testplans = self.base_selenium.get_drop_down_suggestion_list(element='order:test_plan',
                                                                                   item_text=' ')
            suggested_test_units = self.base_selenium.get_drop_down_suggestion_list(element='order:test_unit',
                                                                                    item_text=' ')

        if test_plans:
            self.info("set test plans to {}".format(test_plans))
            self.set_test_plans(test_plans=test_plans)
        if test_units:
            self.info("set test units to {}".format(test_units))
            self.set_test_units(test_units=test_units)
            self.sleep_tiny()

        if multiple_suborders > 0:
            self.info("duplicate first suborder to {} copies".format(multiple_suborders))
            self.duplicate_from_table_view(number_of_duplicates=multiple_suborders)

        if save:
            self.save(save_btn='order:save_btn')

        self.info('Order created with no : {} '.format(order_no))
        if check_testunits_testplans:
            return order_no, suggested_test_units, suggested_testplans
        else:
            return order_no

    def create_new_order_get_test_unit_suggetion_list(self, material_type='', test_unit_name=' ', check_option=False):
        self.info('Create new order.')
        self.click_create_order_button()
        self.sleep_small()
        self.set_new_order()
        self.set_contacts(contacts=[''])
        self.sleep_tiny()
        self.set_material_type(material_type=material_type)
        self.sleep_small()
        self.set_article(article='')
        self.sleep_small()
        self.info('get test unit suggestion list')
        if check_option:
            is_option_exist = self.base_selenium.select_item_from_drop_down(element='order:test_unit',
                                                                            item_text=test_unit_name)
            return is_option_exist
        else:
            test_units = self.base_selenium.get_drop_down_suggestion_list(element='order:test_unit',
                                                                          item_text=test_unit_name)
            return test_units

    def create_existing_order(self, no='', material_type='', article='', contacts=[''], test_units=['']):
        self.info('Create new order.')
        self.click_create_order_button()
        self.set_existing_order()
        order_no = self.set_existing_number(no)
        self.set_material_type(material_type=material_type)
        self.sleep_small()
        self.set_article(article=article)
        self.sleep_small()
        self.set_contacts(contacts=contacts)
        self.sleep_small()
        self.set_test_units(test_units=test_units)
        self.sleep_small()
        self.save(save_btn='order:save_btn')
        self.info('Order created with no : {} '.format(order_no))
        return order_no

    def add_new_suborder(self, material_type='', article_name='', test_plans=[''], test_units=['']):
        self.info('Add new suborder.')
        self.base_selenium.click(element='order:add_new_item')
        self.info('Set material type : {}'.format(material_type))
        self.set_material_type(material_type=material_type, suborder_index=-1)
        self.sleep_tiny()
        self.info('Set article name : {}'.format(article_name))
        if article_name == 'all':
            self.set_article(article='', suborder_index=-1)
        else:
            self.sleep_tiny()
            self.set_article(article=article_name, suborder_index=-1)
        self.sleep_tiny()
        self.info('Set test plan : {}'.format(test_plans))
        if test_plans:
            self.set_test_plans(test_plans=test_plans, suborder_index=-1)
        self.sleep_tiny()
        if test_units:
            self.set_test_units(test_units=test_units, suborder_index=-1)
        self.sleep_tiny()
        return self.get_suborder_data()

    def update_suborder(self, sub_order_index=0, contacts=[], departments=[], material_type='', article='',
                        test_plans=[], test_units=[], shipment_date='', test_date='',
                        remove_old=False, confirm_pop_up=False):

        suborder_table_rows = \
            self.base_selenium.get_table_rows(element='order:suborder_table')

        suborder_row = suborder_table_rows[sub_order_index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_dict_related_to_header(
            row=suborder_row, table_element='order:suborder_table')

        if contacts:
            self.set_contacts(contacts=contacts)
        if departments:
            self.info('Set departments : {}'.format(departments))
            self.set_departments(departments=departments, suborder_index=sub_order_index)
            self.sleep_small()

        suborder_row.click()
        self.base_selenium.scroll()
        self.sleep_small()
        if material_type:
            self.info('Set material type : {}'.format(material_type))
            self.set_material_type(material_type=material_type, suborder_index=sub_order_index)
            if confirm_pop_up:
                self.confirm_popup(True)

        if article:
            if remove_old:
                self.sleep_small()
                self.remove_article(testplans=suborder_elements_dict['testPlans'])

            self.info('Set article name : {}'.format(article))
            self.set_article(article=article, suborder_index=sub_order_index)
            if confirm_pop_up:
                self.confirm_popup(True)
            self.sleep_small()

        self.info('Set test plan : {} for {} time(s)'.format(test_plans, len(test_plans)))
        if test_plans:
            if remove_old:
                self.clear_test_plan(suborder_index=sub_order_index)
                self.confirm_popup()
                self.sleep_small()
            self.set_test_plans(test_plans=test_plans, suborder_index=sub_order_index)
            self.sleep_small()

        self.info('Set test unit : {} for {} time(s)'.format(test_units, len(test_units)))
        if test_units:
            if remove_old:
                self.clear_test_unit(confirm_pop_up)
                self.sleep_small()
            self.set_test_units(test_units=test_units, suborder_index=sub_order_index)
            self.sleep_small()

        anaysis_no = self.generate_random_number(99, 999999)
        self.info(f'update the analysis no {anaysis_no} ')
        self.set_analysis_no(anaysis_no)

        if shipment_date:
            return self.set_shipment_date(row_id=sub_order_index)
        if test_date:
            return self.set_test_date(row_id=sub_order_index)

    def get_suborder_data(self):
        webdriver.ActionChains(self.base_selenium.driver).send_keys(Keys.ESCAPE).perform()
        table_suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.info('getting main order data')
        order_data = {
            "orderNo": self.get_order_no(),
            "contacts": self.get_contacts(),
            "suborders": []
        }
        suborders_data = []
        self.info('getting suborders data')
        for suborder in table_suborders:
            suborder_data = self.base_selenium.get_row_cells_id_dict_related_to_header(
                row=suborder, table_element='order:suborder_table')

            article = \
                {"name": suborder_data['article'].split(' No:')[0], "no": suborder_data['article']
                    .split(' No:')[1]} if len(suborder_data['article'].split(' No:')) > 1 else '-'

            testunits = []
            rawTestunitArr = suborder_data['testUnits'].split(',\n')
            for testunit in rawTestunitArr:
                if 'Type' in testunit:
                    if len(testunit.split(' Type:')) > 1:
                        testunits.append({
                            "name": testunit.split(' Type: ')[0],
                            "Type": testunit.split(' Type: ')[1]
                        })
                elif 'No' in testunit:
                    if len(testunit.split(' No:')) > 1:
                        testunits.append({
                            "name": testunit.split(' No: ')[0],
                            "No": testunit.split(' No: ')[1]
                        })
                elif len(rawTestunitArr):
                    testunits.append({
                        "name": testunit
                    })
                else:
                    testunits = []

            temp_suborder_data = {
                'analysis_no': suborder_data['analysisNo'],
                'departments': suborder_data['departments'].split(',\n'),
                'material_type': suborder_data['materialType'],
                'article': article,
                'testplans': suborder_data['testPlans'].split(',\n'),
                'testunits': testunits,
                'shipment_date': suborder_data['shipmentDate'],
                'test_date': suborder_data['testDate']
            }
            suborders_data.append(temp_suborder_data)
        order_data['suborders'] = suborders_data
        return order_data

    def duplicate_from_table_view(self, number_of_duplicates=1, index_to_duplicate_from=0):
        for duplicate in range(0, number_of_duplicates):
            suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
            suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(
                row=suborders[index_to_duplicate_from],
                table_element='order:suborder_table')
            duplicate_element = self.base_selenium.find_element_in_element(
                source=suborders_elements['Options'], destination_element='order:duplicate_table_view')
            duplicate_element.click()
            self.sleep_tiny()

    def upload_attachment(self, file_name, drop_zone_element, remove_current_file=False, save=False, index=0):
        self.open_suborder_edit_mode(suborder_index=index)
        self.base_selenium.click(element='order:attachment_btn')
        super().upload_file(file_name, drop_zone_element, remove_current_file)
        if save:
            self.base_selenium.driver.execute_script("document.querySelector('.dz-details').style.opacity = 'initial';")
            self.sleep_tiny()
            uploaded_file_name = self.base_selenium.find_element(element='general:uploaded_file_name').text
            self.base_selenium.click('order:uploader_close_btn')
            self.save(save_btn='order:save_btn')
            return uploaded_file_name
        else:
            self.base_selenium.click('order:uploader_close_btn')
            self.cancel(True)
