from ui_testing.pages.base_pages import BasePages
from random import randint
import time


class Orders(BasePages):
    def __init__(self):
        super().__init__()
        self.orders_url = "{}sample/orders".format(self.base_selenium.url)

    def get_orders_page(self):
        self.base_selenium.get(url=self.orders_url)
        self.wait_until_page_is_loaded()

    def get_order_edit_page_by_id(self, id):
        url_text = "{}sample/orders/" + str(id)
        self.base_selenium.get(url=url_text.format(self.base_selenium.url))
        self.wait_until_page_is_loaded()

    def click_create_order_button(self):
        self.base_selenium.LOGGER.info('Press create order button')
        self.base_selenium.click(element='orders:new_order')
        self.wait_until_page_is_loaded()

    def archive_selected_orders(self, check_pop_up=False):
        self.base_selenium.scroll()
        self.base_selenium.click(element='orders:right_menu')
        self.base_selenium.click(element='orders:archive')
        self.confirm_popup()
        if check_pop_up:
            if self.base_selenium.wait_element(element='general:confirmation_pop_up'):
                return False
        return True

    def is_order_exist(self, value):
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def is_order_archived(self, value):
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def duplicate_order_from_table_overview(self, number_of_copies):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click(element='orders:duplicate')
        self.base_selenium.set_text(
            element='orders:number_of_copies', value=number_of_copies)
        self.base_selenium.click(element='orders:create_copies')
        self.sleep_medium()

    def duplicate_main_order_from_table_overview(self):
        self.info('Duplicate the main order')
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.sleep_tiny()
        self.base_selenium.click(element='orders:duplicate')
        self.sleep_medium()

    def duplicate_main_order_from_order_option(self, index=0):
        self.info('duplicate main order from the order\'s active table')
        table_records = self.result_table(element='general:table')
        self.open_row_options(row=table_records[index])
        self.base_selenium.click(element='orders:mainorder_duplicate')
        self.wait_until_page_is_loaded()

    def duplicate_sub_order_from_table_overview(self, index=0, number_of_copies=1):
        self.info('duplicate suborder from the order\'s active table')
        child_table_records = self.result_table(element='general:table_child')
        self.open_row_options(row=child_table_records[index])
        self.base_selenium.click(element='orders:suborder_duplicate')
        self.base_selenium.set_text(element='orders:number_of_copies', value=number_of_copies)
        self.base_selenium.click(element='orders:create_copies')
        self.sleep_medium()

    def archive_sub_order_from_active_table(self, index=0):
        self.info('archive suborder from the order\'s active table')
        child_table_records = self.result_table(element='general:table_child')
        self.open_row_options(row=child_table_records[index])
        self.base_selenium.click(element='orders:suborder_archive')
        self.confirm_popup()

    def delete_sub_order(self, analysis_no, confirm_popup=True):
        self.info('navigate to archived order table')
        self.get_archived_items()
        sub_orders = self.get_table_data(table_element='general:table_child')
        child_table_records = self.result_table(element='general:table_child')
        index = 0
        if len(sub_orders) == 1:
            index = 0
        else:   # in case that order has more than one archived suborder
            for suborder in sub_orders:
                if suborder['Analysis No.'] == analysis_no:
                    break
                index = index+1
        self.info("delete suborder with index {} and analysis_no {}".format(index, analysis_no))
        self.open_row_options(row=child_table_records[index])
        self.base_selenium.click(element='orders:suborder_delete')
        self.confirm_popup()
        if confirm_popup:
            self.confirm_popup()
        else:
            self.info('Cancel the popup')
            self.cancel()

    def get_random_order(self):
        self.base_selenium.LOGGER.info(' + Get random order.')
        row = self.get_random_order_row()
        order_dict = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        self.open_edit_page(row=row)
        return order_dict

    def get_random_order_row(self):
        return self.get_random_table_row(table_element='orders:orders_table')

    def filter_by_order_no(self, filter_text):
        self.open_filter_menu()
        self.info('Filter by order no. : {}'.format(filter_text))
        self.filter_by(filter_element='orders:order_filter', filter_text=filter_text, field_type='text')
        self.filter_apply()

    def open_filter_menu(self):
        self.base_selenium.scroll()
        filter = self.base_selenium.find_element_in_element(source_element='general:menu_filter_view',
                                                            destination_element='general:filter')
        filter.click()

    def filter_by_analysis_number(self, filter_text):
        self.open_filter_menu()
        self.info('Filter by analysis number : {}'.format(filter_text))
        self.filter_by(filter_element='orders:analysis_filter', filter_text=filter_text, field_type='text')
        self.filter_apply()
        
    def filter_by_date(self, first_filter_element, first_filter_text, second_filter_element, second_filter_text):
        self.open_filter_menu()
        self.sleep_tiny()
        self.base_selenium.set_text(element=first_filter_element, value=first_filter_text)
        self.sleep_tiny()
        self.base_selenium.set_text(element=second_filter_element, value=second_filter_text)
        self.filter_apply()

    def get_orders_duplicate_data(self, order_no):
        self.base_selenium.LOGGER.info(' + Get orders duplicate data with no : {}.'.format(order_no))
        orders = self.search(order_no)[:-1]
        orders_data = [self.base_selenium.get_row_cells_dict_related_to_header(order) for order in orders]
        self.base_selenium.LOGGER.info(' + {} duplicate orders.'.format(len(orders)))
        return orders_data, orders

    # Return all filter fields used in order
    def order_filters_element(self, key='all'):
        filter_fileds = {'orderNo': {'element': 'orders:order_filter', 'type': 'text'},
                         'analysis': {'element': 'orders:analysis_filter', 'type': 'text','result_key': 'Analysis No.'},
                         'Contact Name': {'element': 'orders:contact_filter', 'type': 'drop_down'},
                         'lastModifiedUser': {'element': 'orders:changed_by', 'type': 'drop_down',
                                             'result_key':'Changed By'},
                         'materialType': {'element': 'orders:material_type_filter', 'type': 'drop_down',
                                          'result_key':'Material Type'},
                         'article': {'element': 'orders:article_filter', 'type': 'drop_down',
                                     'result_key': 'Article Name'},
                         'shipmentDate': {'element': ['orders:shipment_date_filter', 'orders:shipment_date_filter_end'],
                                          'type': 'text',
                                          'result_key': 'Shipment Date'},
                         'testDate': {'element': ['orders:test_date_filter', 'orders:test_date_filter_end'],
                                      'type': 'text',
                                      'result_key': 'Test Date'},
                         'createdAt': {'element': ['orders:created_on_filter','orders:created_on_filter_end'],
                                       'type': 'text',
                                       'result_key': 'Created On'},
                         'testUnit': {'element': 'orders:test_units_filter', 'type': 'drop_down',
                                      'result_key': 'Test Units'},
                         'testPlans': {'element': 'orders:test_plans_filter', 'type': 'drop_down',
                                       'result_key': 'Test Plans'}
                         }

        if key == 'all':
            return filter_fileds
        else:
            return filter_fileds[key]

    def archive_table_suborder(self, index=0):
        self.info('archive suborder from the order\'s active table')
        child_table_records = self.result_table(element='general:table_child')
        self.open_row_options(row=child_table_records[0])
        self.base_selenium.click('orders:suborder_archive')
        self.confirm_popup()
        self.sleep_small()
    
    def restore_table_suborder(self, index=0):
        self.info('restore suborder from the order\'s active table')
        child_table_records = self.result_table(element='general:table_child')
        self.open_row_options(row=child_table_records[0])
        self.base_selenium.click('orders:suborder_restore')
        self.confirm_popup()
        self.sleep_small()

    def construct_main_order_from_table_view(self, order_row=None):
        order_data = {
            "orderNo": self.get_no(order_row),
            "contacts": self.get_contact(order_row),
            "suborders": []
        }

        suborders_data = []

        self.base_selenium.LOGGER.info('getting suborders data')

        for suborder in order_row['suborders']:
            suborder_data = suborder
            article = {
                "name": suborder_data['Article Name'],
                "no": suborder_data['Article No.'].replace("'", '').replace('"', '')
            }

            testunits =[]
            testunit = {}

            # get all the testunit names
            testunits_names = suborder_data['Test Units'].split(',\n') or []
            
            # map the testunit to name and number
            for testunit_name in testunits_names:
                testunit['name'] = testunit_name
                testunit['no'] = None

            # append the testunit to the testunits list
            testunits.append(testunit)

            mapped_suborder_data = {
                'analysis_no': suborder_data['Analysis No.'],  # suborder_data['Analysis No.'],
                'departments': suborder_data['Departments'].split(', '),
                'material_type': suborder_data['Material Type'],
                'article': article,
                'testplans': suborder_data['Test Plans'].split(',\n') if suborder_data['Test Plans'] != '-' else [''],              
                'testunits': testunits if suborder_data['Test Units'] != '-' else [],
                'shipment_date': suborder_data['Shipment Date'],
                'test_date': suborder_data['Test Date']
            }
            
            suborders_data.append(mapped_suborder_data)

        order_data['suborders'] = suborders_data
        return order_data

    def get_random_main_order_with_sub_orders_data(self):
        self.info('+ Get Main order data with related subOrders')
        # get all the order rows
        all_orders = self.base_selenium.get_table_rows(element='orders:orders_table')
        # select random order
        row_id = randint(0, len(all_orders) - 2)
        # get the main order data
        main_order = self.base_selenium.get_row_cells_dict_related_to_header(row=all_orders[row_id])
        # get its sub orders
        sub_orders = self.get_child_table_data(row_id)
        # attach the sub orders to the main order
        main_order['suborders'] = sub_orders
        # construct the order object
        main_order = self.construct_main_order_from_table_view(main_order)
        # attach the row element
        main_order['row_element'] = all_orders[row_id]
        # return the main order
        return main_order

    def get_orders_and_suborders_data(self, order_no):
        self.base_selenium.LOGGER.info(' + Get orders duplicate data with no : {}.'.format(order_no))
        orders = self.search(order_no)[:-1]
        orders_data = self.get_child_table_data()

        return orders_data, orders

    def navigate_to_analysis_active_table(self):
        self.base_selenium.click(element='orders:analysis_tab')
        self.sleep_small()
        
    def search_by_analysis_number(self,analysis_number):
        self.base_selenium.click(element='general:filter_button')
        self.base_selenium.set_text(element='orders:analysis_filter',value=analysis_number)
        self.base_selenium.click(element='general:filter_btn')
        time.sleep(self.base_selenium.TIME_MEDIUM)

    def is_order_in_table(self, value):
        results = self.base_selenium.get_table_rows(element='general:table')
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False 

