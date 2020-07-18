from ui_testing.pages.orders_page import Orders
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from random import randint


class Order(Orders):
    def get_order(self):
        return self.base_selenium.get_text(element='order:order').split('\n')[0]

    def get_order_number(self):
        return self.base_selenium.get_text(element='order:order_number_add_form').split('\n')[0]

    def set_order_number(self, no):
        self.base_selenium.set_text(element="order:order_number", value=no)

    def set_new_order(self):
        self.base_selenium.LOGGER.info('Set new order.')
        self.base_selenium.select_item_from_drop_down(
            element='order:order', item_text='New Order')

    def set_existing_order(self):
        self.base_selenium.select_item_from_drop_down(
            element='order:order', item_text='Existing Order')

    def open_suborder_edit(self, sub_order_index=0):
        suborder_table_rows = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborder_table_rows[sub_order_index]
        suborder_row.click()

    def set_material_type(self, material_type=''):
        if material_type:
            self.base_selenium.select_item_from_drop_down(element='order:material_type', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:material_type', avoid_duplicate=True)
            self.sleep_tiny()
            return self.get_material_type()

    def get_material_type(self):
        return self.base_selenium.get_text(element='order:material_type').split('\n')[0]

    def get_article(self):
        article = self.base_selenium.get_text(element='order:article').split(' No')[0]
        if article == 'Search':
            return None
        else:
            return article

    def set_article(self, article=''):
        if article:
            self.base_selenium.select_item_from_drop_down(element='order:article', item_text=article)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:article')
            self.sleep_tiny()
            return self.get_article()

    def is_article_existing(self, article):
        self.set_article(article=article)
        return self.base_selenium.check_item_in_items(element='order:article', item_text=article)

    def is_testunit_existing(self, test_unit):
        self.set_test_unit(test_unit=test_unit)
        return self.base_selenium.check_item_partially_in_items(element='order:test_unit', item_text=test_unit)

    def set_contact(self, contact='', remove_old=False):
        if remove_old:
           self.base_selenium.clear_items_in_drop_down(element='order:contact')
        if contact:
           self.base_selenium.select_item_from_drop_down(element='order:contact', item_text=contact)
        else:
           self.base_selenium.select_item_from_drop_down(element='order:contact', avoid_duplicate=True)
        return self.get_contact()

    def get_contact(self):
        contacts = self.base_selenium.get_text(element='order:contact')
        if "×" in contacts:
            return contacts.replace("×", "").split('\n')
        else:
            return []

    def set_test_plan(self, test_plan=''):
        if test_plan:
            self.base_selenium.select_item_from_drop_down(element='order:test_plan', item_text=test_plan)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_plan')
            return self.get_test_plan()

    def get_test_plan(self):
        test_plans = self.base_selenium.get_text(element='order:test_plan')
        if "×" in test_plans:
            return test_plans.replace("× ", "").split('\n')
        else:
            return []

    def clear_test_plan(self):
        if self.get_test_plan():
            self.base_selenium.clear_items_in_drop_down(element='order:test_plan')

    def clear_test_unit(self, confirm=True):
        if self.get_test_unit():
            self.base_selenium.clear_items_in_drop_down(element='order:test_unit', confirm_popup=confirm)

    def set_test_unit(self, test_unit=''):
        if test_unit:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit', item_text=test_unit)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit')
            return self.get_test_unit()

    def get_test_unit(self):
        test_units = self.base_selenium.get_text(element='order:test_unit')
        if test_units and test_units != 'Search':
            return test_units.replace("×", "").split("\n")
        else:
            return []

    def create_new_order(self, material_type='', article='', contact='', test_plans=[''], test_units=[''],
                         multiple_suborders=0, departments=''):
        self.info(' Create new order.')
        self.click_create_order_button()
        self.set_new_order()
        self.set_contact(contact=contact)
        self.sleep_small()
        self.set_departments(departments=departments)
        self.set_material_type(material_type=material_type)
        self.sleep_small()
        self.set_article(article=article)
        self.sleep_small()
        order_no = self.get_no()

        for test_plan in test_plans:
            self.set_test_plan(test_plan=test_plan)
        for test_unit in test_units:
            self.set_test_unit(test_unit=test_unit)
        self.sleep_small()
        
        if multiple_suborders > 0:
            self.get_suborder_table()
            self.duplicate_from_table_view(number_of_duplicates=multiple_suborders)

        self.save(save_btn='order:save_btn')
        self.info(' Order created with no : {} '.format(order_no))

    def create_multiple_contacts_new_order(self, contacts):
        self.click_create_order_button()
        self.sleep_small()
        self.set_new_order()
        self.sleep_tiny()
        for contact in contacts:
            self.set_contact(contact)
            self.sleep_tiny()
        self.set_material_type('Raw Material')
        self.sleep_small()
        self.set_article('')
        self.sleep_small()
        self.set_test_unit('')
        self.sleep_small()

    def get_department_suggestion_lists(self, open_suborder_table=False, contacts=[]):
        """
        :param open_suborder_table:

        in create mode let open_suborder_table = false
        in edit mode let open_suborder_table = True
        :return: 2 lists , departments with contacts and departments only
        """
        if open_suborder_table:
            suborder_row = self.base_selenium.get_table_rows(element='order:suborder_table')[0]
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
                if suggested_department_list.index(item) == len(suggested_department_list)-1:
                    contact_dep_list.append(contact_dict)

        return contact_dep_list, departments_only_list

    def create_existing_order(self, no='', material_type='', article='', contact='', test_units=[],
                              multiple_suborders=0):
        self.base_selenium.LOGGER.info(' Create new order.')
        self.click_create_order_button()
        self.set_existing_order()
        order_no = self.set_existing_number(no)
        self.set_material_type(material_type=material_type)

        self.sleep_small()
        self.set_article(article=article)
        self.sleep_small()
        self.set_contact(contact=contact)
        self.sleep_small()

        for test_unit in test_units:
            self.set_test_unit(test_unit=test_unit)

        self.sleep_small()
        self.save(save_btn='order:save_btn')
        self.base_selenium.LOGGER.info(' Order created with no : {} '.format(order_no))
        return order_no

    def create_existing_order_with_auto_fill(self, no=''):
        self.info(' Create new order.')
        self.click_create_order_button()
        self.set_existing_order()
        order_no = self.set_existing_number(no)
        self.sleep_tiny()
        self.click_auto_fill()
        self.info(' Order Auto filled with data from order no : {} '.format(order_no))
        return order_no

    def get_no(self, order_row=None):
        if order_row:
            return order_row['Order No.']
        else:
            return self.base_selenium.get_value(element="order:no")

    def set_no(self, no):
        self.info(' set no. {}'.format(no))
        self.base_selenium.set_text(element="order:no", value=no)
        self.sleep_small()

    def set_existing_number(self, no=''):
        if no:
            self.base_selenium.select_item_from_drop_down(
                element='order:order_number_add_form', item_text=no)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:order_number_add_form')
            return self.get_order_number()

    def edit_random_order(self, edit_method, edit_value, save=True):
        if 'contact' in edit_method:
            self.set_contact(edit_value)
        elif 'departments' in edit_method:
            self.set_departments(edit_value)
        # elif 'material_type' in edit_method:
        # self.set_material_type(edit_value)
        # elif '' in edit_method:
        # self.set_contact(edit_value)

        if save:
            self.save()
        else:
            self.cancel()

    def get_last_order_row(self):
        rows = self.result_table()
        return rows[0]

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

    def get_departments(self):
        departments = self.base_selenium.get_text(element='order:departments').replace('×', '').split('\n')
        if departments == ['Search']: #empty
            return []
        return departments

    def get_department(self):
        return self.base_selenium.get_text(element='order:departments').split('\n')[0]

    def set_departments(self, departments=''):
        if departments:
            self.base_selenium.select_item_from_drop_down(element='order:departments', item_text=departments)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:departments')
            self.sleep_small()
            return self.get_departments()

    def get_suborder_table(self):
        self.base_selenium.LOGGER.info(' Get suborder table list.')
        self.base_selenium.click(element='order:suborder_list')

    def create_new_suborder(self, material_type='', article_name='', test_plan='', test_unit='',
                            add_new_suborder_btn='order:add_new_item'):
        # self.get_suborder_table()
        rows_before = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.info('Add new suborder.')
        self.base_selenium.click(element=add_new_suborder_btn)
        rows_after = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = rows_after[len(rows_before)]
        suborder_elements_dict = self.base_selenium.get_row_cells_elements_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        self.info('Set material type : {}'.format(material_type))
        self.set_material_type(material_type)
        self.sleep_tiny()
        self.info('Set article name : {}'.format(article_name))
        if article_name == 'all':
            self.set_article('')
        else:
            self.set_article(article_name)
        self.sleep_tiny()
        self.info('Set test plan : {}'.format(test_plan))
        self.set_test_plan(test_plan)
        self.sleep_tiny()
        self.set_test_unit(test_unit)
        self.sleep_tiny()
        return self.get_suborder_data()

    def duplicate_from_table_view(self, number_of_duplicates=1, index_to_duplicate_from=0):
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(
            row=suborders[index_to_duplicate_from],
            table_element='order:suborder_table')

        duplicate_element = self.base_selenium.find_element_in_element(source=suborders_elements['Options'],
                                                                       destination_element='order:duplicate_table_view')
        for duplicate in range(0, number_of_duplicates):
            duplicate_element.click()

    def duplicate_suborder(self):
        self.get_suborder_table()
        self.base_selenium.LOGGER.info(' Duplicate order')
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(row=suborders[0],
                                                                                         table_element='order:suborder_table')
        duplicate_element = self.base_selenium.find_element_in_element(source=suborders_elements['Options'],
                                                                       destination_element='order:duplicate_table_view')
        duplicate_element.click()


    # this method to be used while you are order's table with add page ONLY, and you can get the required data by sending the index, and the needed fields of the suborder
    def get_suborder_data(self):
        webdriver.ActionChains(self.base_selenium.driver).send_keys(Keys.ESCAPE).perform()
        table_suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.base_selenium.LOGGER.info('getting main order data')
        order_data = {
            "orderNo": self.get_no(),
            "contacts": self.get_contact(),
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

            testunits =[]
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

    def remove_testplan_by_name(self, index, testplan_name):
        suborder_table_rows = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborder_table_rows[index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_elements_related_to_header(row=suborder_row,
                                                                                                table_element='order:suborder_table')
        self.base_selenium.update_item_value(item=suborder_elements_dict['testPlans'],
                                             item_text=testplan_name.replace("'", ''))

    def remove_testunit_by_name(self, index, testunit_name):
        suborder_table_rows = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborder_table_rows[index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_elements_related_to_header(row=suborder_row,
                                                                                                table_element='order:suborder_table')
        self.base_selenium.update_item_value(item=suborder_elements_dict['testUnits'],
                                             item_text=testunit_name.replace("'", ''))

    def update_suborder(self, sub_order_index=0, contacts=False, departments=[], material_type=False, articles=False,
                        test_plans=[], test_units=[], shipment_date=False, test_date=False, remove_old=False,
                        confirm_pop_up=False):

        suborder_table_rows = \
            self.base_selenium.get_table_rows(element='order:suborder_table')

        suborder_row = suborder_table_rows[sub_order_index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_dict_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        contacts_record = 'contact with many departments'
        suborder_row.click()
        self.base_selenium.scroll()
        if material_type:
            self.info('Set material type : {}'.format(material_type))
            self.set_material_type(material_type=material_type)
            self.confirm_popup(True)
            self.sleep_small()

        for article in articles:
            if remove_old:
                self.sleep_small()
                self.remove_article(testplans=suborder_elements_dict['testPlans'])
                self.info('Set article name : {}'.format(articles))
                self.set_article(article=articles)
                self.sleep_small()
            self.set_article(article=article)
            self.sleep_small()

        self.info(' Set test plan : {} for {} time(s)'.format(test_plans, len(test_plans)))
        for testplan in test_plans:
            if remove_old:
                self.clear_test_plan()
                self.confirm_popup()
                self.sleep_small()
            self.set_test_plan(test_plan=testplan)
            self.sleep_small()

        self.info(' Set test unit : {} for {} time(s)'.format(test_units, len(test_units)))
        for testunit in test_units:
            if remove_old:
                self.clear_test_unit(confirm_pop_up)
                self.sleep_small()
            self.set_test_unit(test_unit=testunit)
            self.sleep_small()

        if shipment_date:
            return self.set_shipment_date(row_id=sub_order_index)
        if test_date:
            return self.set_test_date(row_id=sub_order_index)
        if contacts:
            self.set_contact(contact=contacts_record)
        if departments:
            self.info(' Set departments : {}'.format(departments))
            self.set_departments(departments=departments)
            self.sleep_small()

    def update_material_type_suborder(self, row, material_type):
        self.base_selenium.LOGGER.info(' Set material type : {}'.format(material_type))
        self.base_selenium.update_item_value(item=row['materialType'],
                                             item_text=material_type.replace("'", ''))

    def update_article_suborder(self, row, article):
        self.base_selenium.LOGGER.info(' Set article name : {}'.format(article))
        self.base_selenium.update_item_value(item=row['article'],
                                             item_text=article.replace("'", ''))

    def add_multiple_testplans_suborder(self, row, testplans):
        self.base_selenium.LOGGER.info(' Set test plan : {} for {} time(s)'.format(testplans, len(testplans)))
        for testplan in testplans:
            self.base_selenium.update_item_value(item=row['testUnits'],
                                                 item_text=testplan.replace("'", ''))

    def add_multiple_testunits_suborder(self, row, testunits):
        self.base_selenium.LOGGER.info(' Set test unit : {} for {} time(s)'.format(testunits, len(testunits)))
        for testunit in testunits:
            self.base_selenium.update_item_value(item=row['testUnits'],
                                                 item_text=testunit.replace("'", ''))

    def update_departments_suborder(self, row, departments):
        self.base_selenium.LOGGER.info(' Set departments : {}'.format(departments))
        for department in departments:
            self.base_selenium.update_item_value(item=row['departments'], item_text=department)

    def archive_suborder(self, index, check_pop_up=False):
        self.get_suborder_table()
        self.sleep_tiny()
        self.base_selenium.LOGGER.info('archive suborder with index {}'.format(index + 1))
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.base_selenium.LOGGER.info(' Archive order no #{}'.format(index + 1))
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(row=suborders[index],
                                                                                         table_element='order:suborder_table')
        archive_element = self.base_selenium.find_element_in_element(source=suborders_elements['Options'],
                                                                     destination_element='order:delete_table_view')

        archive_element.click()
        self.sleep_tiny()
        if check_pop_up:
            self.base_selenium.LOGGER.info('confirm archiving')
            self.base_selenium.click(element='articles:confirm_archive')
        else:
            self.base_selenium.LOGGER.info('cancel archiving')
            self.base_selenium.click(element='articles:cancel_archive')

    def click_auto_fill(self):
        button = self.base_selenium.find_element_in_element(source_element='order:auto_fill_container',
                                                            destination_element='order:auto_fill')
        button.click()

    def create_new_suborder_with_test_units(self, material_type='', article_name='', test_unit='', **kwargs):
        rows_before = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.info(' Add new suborder.')
        self.base_selenium.click(element='order:add_new_item')

        rows_after = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.info(' Set material type : {}'.format(material_type))
        self.set_material_type(material_type=material_type)
        self.sleep_tiny()
        self.info(' Set article name : {}'.format(article_name))
        self.set_article(article=article_name)
        self.sleep_tiny()
        self.info(' Set Test Unit  : {}'.format(test_unit))
        self.set_test_unit(test_unit=test_unit)
        self.sleep_tiny()

    def get_order_id(self):
        current_splited_url = self.base_selenium.get_url().split('/')
        order_id = current_splited_url[(len(current_splited_url) - 1)]
        return order_id

    def navigate_to_analysis_tab(self):
        self.base_selenium.scroll()
        self.base_selenium.click('orders:analysis_order_tab')
        self.wait_until_page_is_loaded()

    def set_material_type_of_first_suborder(self, material_type='', sub_order_index=0):
        suborder_table_rows = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborder_table_rows[sub_order_index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_dict_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        suborder_row.click()
        if material_type:
            self.base_selenium.select_item_from_drop_down(
                element='order:material_type', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:material_type')
            return self.get_material_type_of_first_suborder()

    def get_material_type_of_first_suborder(self, sub_order_index=0):
        suborder_table_rows = self.base_selenium.get_table_rows(
            element='order:suborder_table')
        suborder_row = suborder_table_rows[sub_order_index]
        suborder_elements_dict = self.base_selenium.get_row_cells_id_dict_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        suborder_row.click()
        return self.base_selenium.get_text(element='order:material_type').split('\n')[0]

    def remove_article(self, testplans=''):
        self.info('clear article data')
        self.base_selenium.clear_single_select_drop_down(element='order:article')
        if testplans:
            self.base_selenium.wait_element(element='general:form_popup_warning_window')
            self.base_selenium.click(element='general:confirmation_button')
        self.sleep_small()

    def get_contact_field(self):
        return self.base_selenium.get_text(element='order:contact').split('\n')[0]

    def get_data_first_row(self, index=0):
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborders[index]
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(
            row=suborder_row, table_element='order:suborder_table')
        return suborders_elements

    def match_format_to_sheet_format(self, list_of_orders=[]):
        formatted_orders_list = []
        orders_list = []
        for order in list_of_orders:
            for key in order:
                if key in ['', 'Options']:
                    continue
                if key in ['Contact Name', 'Test Plans', 'Departments', 'Test Units']:
                    formatted_orders_list.append(order[key].replace(',\n', ' & ').replace("'", ""))
                else:
                    formatted_orders_list.append(order[key].replace("'", ""))
            orders_list.append(formatted_orders_list)
            formatted_orders_list = []

        return orders_list

    def get_sub_order_data_first_row(self, index=0):
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = suborders[index]
        suborder_data = self.get_suborder_data()
        return  suborder_data

    def upload_attachment(self, file_name, drop_zone_element, remove_current_file=False, save=False):
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
            
    def get_testplan_pop_up(self):
        self.base_selenium.click(element='order:testplan_popup_btn')
        self.sleep_small()
        results = []
        elements = self.base_selenium.find_elements('order:popup_data')
        for element in elements:
            test_plan, test_units = element.text.split('\n')[0], element.text.split('\n')[1:]
            results.append({'test_plan': test_plan, 'test_units': test_units})
        return results
