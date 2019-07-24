from ui_testing.pages.orders_page import Orders
import pyperclip


class Order(Orders):
    def get_order(self):
        return self.base_selenium.get_text(element='order:order').split('\n')[0]

    def get_order_number(self):
        return self.base_selenium.get_text(element='order:order_number_add_form').split('\n')[0]

    def set_new_order(self):
        self.base_selenium.LOGGER.info(' + Set new order.')
        self.base_selenium.select_item_from_drop_down(
            element='order:order', item_text='New Order')

    def set_existing_order(self):
        self.base_selenium.select_item_from_drop_down(
            element='order:order', item_text='Existing Order')

    def set_material_type(self, material_type=''):
        if material_type:
            self.base_selenium.select_item_from_drop_down(
                element='order:material_type', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:material_type')
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
            self.base_selenium.select_item_from_drop_down(
                element='order:contact', item_text=contact)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='order:contact')
            return self.get_contact()

    def get_contact(self):
        return self.base_selenium.get_text(element='order:contact').split('\n')[0]

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
    
    def clear_test_unit(self):
        if self.get_test_unit():
            self.base_selenium.clear_items_in_drop_down(element='order:test_unit')
    
    def set_test_unit(self, test_unit):
        if test_unit:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit', item_text=test_unit)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:test_unit')
            return self.get_test_unit()

    def get_test_unit(self):
        test_units = self.base_selenium.get_text(element='order:test_unit')
        if "×" in test_units:
            return test_units.replace("× ", "").split('\n')
        else:
            return []

    def create_new_order(self, material_type='', article='', contact='', test_plans=[], test_units=[], multiple_suborders=0):
        self.base_selenium.LOGGER.info(' + Create new order.')
        self.click_create_order_button()
        self.set_new_order()
        self.set_material_type(material_type=material_type)
        self.set_article(article=article)
        self.set_contact(contact=contact)
        order_no = self.get_no()

        for test_plan in test_plans:
            self.set_test_plan(test_plan=test_plan)     
        for test_unit in test_units:
            self.set_test_unit(test_unit)      
        if multiple_suborders > 0:
            self.get_suborder_table()
            self.duplicate_from_table_view(number_of_duplicates=multiple_suborders)

        self.save(save_btn='order:save_btn')
        self.base_selenium.LOGGER.info(' + Order created with no : {} '.format(order_no))
        return order_no
    
    
    def create_existing_order(self, no='', material_type='', article='', contact='', test_units=[], multiple_suborders=0):
        self.base_selenium.LOGGER.info(' + Create new order.')
        self.click_create_order_button()
        self.set_existing_order()
        order_no = self.set_existing_number(no)
        self.set_material_type(material_type=material_type)
        self.set_article(article=article)
        self.set_contact(contact=contact)
        
        for test_unit in test_units:
            self.set_test_unit(test_unit)    
        if multiple_suborders > 0:
            self.get_suborder_table()
            self.duplicate_from_table_view(number_of_duplicates=multiple_suborders)

        self.save(save_btn='order:save_btn')
        self.base_selenium.LOGGER.info(' + Order created with no : {} '.format(order_no))
        return order_no
    
    
    def create_existing_order_with_auto_fill(self, no=''):
        self.base_selenium.LOGGER.info(' + Create new order.')
        self.click_create_order_button()
        self.set_existing_order()
        order_no = self.set_existing_number(no)
        self.sleep_tiny()
        self.click_auto_fill()
        self.base_selenium.LOGGER.info(' + Order Auto filled with data from order no : {} '.format(order_no))
        return order_no        
               
    def get_no(self):
        return self.base_selenium.get_value(element="order:no")

    def set_no(self, no):
        self.base_selenium.LOGGER.info(' + set no. {}'.format(no))
        self.base_selenium.set_text(element="order:no", value=no)
        
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
         #elif 'material_type' in edit_method:
            #self.set_material_type(edit_value)
        # elif '' in edit_method:
        # self.set_contact(edit_value)

        if save:
            self.save()
        else:
            self.cancel()

    def get_last_order_row(self):
        rows = self.result_table()
        return rows[0]

    def get_shipment_date(self):
        return self.base_selenium.get_value(element='order:shipment_date')

    def get_test_date(self):
        return self.base_selenium.get_value(element='order:test_date')

    def set_test_date(self, date=''):
        if not date:
            date = self.get_random_date()
        self.base_selenium.set_text(element='order:test_date', value=date)
        return date

    def set_shipment_date(self, date=''):
        if not date:
            date = self.get_random_date()
        self.base_selenium.set_text(element='order:shipment_date', value=date)
        return date
        
    def get_departments(self):
        departments = self.base_selenium.get_text(
            element='order:departments').split('\n')[0]
        if departments == 'Search':
            return ''
        return departments

    def get_department(self):
        return self.base_selenium.get_text(element='order:departments').split('\n')[0]

    def set_departments(self, departments=''):
        if departments:
            self.base_selenium.select_item_from_drop_down(element='order:departments', item_text=departments)
        else:
            self.base_selenium.select_item_from_drop_down(element='order:departments')
            return self.get_departments()
        
    def get_suborder_table(self):
        self.base_selenium.LOGGER.info(' + Get suborder table list.')
        self.base_selenium.click(element='order:suborder_list')

    def create_new_suborder(self, material_type='', article_name='', test_plan='', **kwargs):
        self.get_suborder_table()
        rows_before = self.base_selenium.get_table_rows(element='order:suborder_table')

        self.base_selenium.LOGGER.info(' + Add new suborder.')
        self.base_selenium.click(element='order:add_new_item')

        rows_after = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborder_row = rows_after[len(rows_before)]

        suborder_elements_dict = self.base_selenium.get_row_cells_elements_related_to_header(row=suborder_row,
                                                                                             table_element='order:suborder_table')
        self.base_selenium.LOGGER.info(' + Set material type : {}'.format(material_type))
        self.base_selenium.update_item_value(item=suborder_elements_dict['Material Type: *'], item_text=material_type.replace("'", ''))
        self.base_selenium.LOGGER.info(' + Set article name : {}'.format(article_name))
        self.base_selenium.update_item_value(item=suborder_elements_dict['Article: *'], item_text=article_name.replace("'", ''))
        self.base_selenium.LOGGER.info(' + Set test plan : {}'.format(test_plan))
        self.base_selenium.update_item_value(item=suborder_elements_dict['Test Plan: *'], item_text=test_plan.replace("'", ''))

        for key in kwargs:
            if key in suborder_elements_dict.keys():
                self.base_selenium.update_item_value(item=suborder_elements_dict[key], item_text=kwargs[key])
            else:
                self.base_selenium.LOGGER.info(' + {} is not a header element!'.format(key))
                self.base_selenium.LOGGER.info(' + Header keys : {}'.format(suborder_elements_dict.keys()))

    def duplicate_from_table_view(self, number_of_duplicates=1):
        for duplicate in range(number_of_duplicates):
            self.base_selenium.click(element='order:duplicate_table_view')    
        
    def duplicate_suborder(self):
        self.get_suborder_table()
        self.base_selenium.LOGGER.info(' + Duplicate order')
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        suborders_elements = self.base_selenium.get_row_cells_elements_related_to_header(row=suborders[0],
                                                                                         table_element='order:suborder_table')
        duplicate_element = self.base_selenium.find_element_in_element(source=suborders_elements['Options'],
                                                                       destination_element='order:duplicate_table_view')
        duplicate_element.click()

    def archive_suborder(self, index, check_pop_up=False):
        self.get_suborder_table()
        self.sleep_tiny()
        self.base_selenium.LOGGER.info('archive suborder with index {}'.format(index+1))
        suborders = self.base_selenium.get_table_rows(element='order:suborder_table')
        self.base_selenium.LOGGER.info(' + Archive order no #{}'.format(index+1))
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
