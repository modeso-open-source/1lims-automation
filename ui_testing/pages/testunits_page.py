from ui_testing.pages.base_pages import BasePages
from random import randint


class TstUnits(BasePages):
    def __init__(self):
        super().__init__()
        self.test_units_url = "{}testUnits".format(self.base_selenium.url)

    def get_test_units_page(self):
        self.base_selenium.LOGGER.info(' + Get test units page.')
        self.base_selenium.get(url=self.test_units_url)
        self.wait_until_page_is_loaded()

    def get_random_test_units(self):
        row = self.get_random_test_units_row()
        self.open_edit_page(row=row)

    def get_random_test_units_row(self):
        return self.get_random_table_row(table_element='test_units:test_units_table')

    def archive_selected_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:archive')
        self.confirm_popup()
    
    def get_versions_table(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:version_table')
        self.sleep_small()

    def get_versions_of_selected_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:testunit_menu')
        self.sleep_small()
        self.base_selenium.click(element='test_units:versions')
        self.sleep_medium()

    def get_archived_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:archived')
        self.sleep_small()
    
    def open_configurations(self):
        self.info('open testunits configurations')
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:configurations')
        self.sleep_small()


    def is_test_unit_in_table(self, value):
        """
            - get_archived_test_units then call me to check if the test unit has been archived.
            - get_active_test_units then call me to check if the test unit is active.
        :param value: search value
        :return:
        """
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def restore_selected_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:restore')
        self.confirm_popup()

    def get_active_test_units(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.base_selenium.click(element='test_units:active')
        self.sleep_small()

    def duplicate_test_unit(self):
        self.info('duplicate the selected test unit')
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.base_selenium.click('orders:duplicate')
        self.sleep_small()
        self.save(sleep=True)
        
    def open_configurations(self):
        self.info('open testunits configurations')
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_units:right_menu')
        self.sleep_tiny()
        self.base_selenium.click(element='test_units:configurations')
        self.sleep_small()

    def open_testunit_name_configurations_options(self):
        self.info('open testunits name configurations options')
        self.base_selenium.click(element='configurations_page:display_options_menu')
        self.sleep_tiny()
        self.base_selenium.click(element='configurations_page:field_options')
        self.sleep_small()

    def clear_all_selected_view_and_search_options(self):
        self.info('clear selected view and search options of testunits name')
        self.base_selenium.click(element='configurations_page:clear_all')
        self.sleep_tiny()

    def check_all_options_of_search_view_menu(self):
        items = ['name','method', 'type', 'number']
        all_options_exist = True
        for item in items:
            self.clear_all_selected_view_and_search_options()
            all_options_exist = all_options_exist and self.base_selenium.is_item_in_drop_down(
                                                                        element='configurations_page:view_search_ddl',
                                                                        item_text=item)
        return all_options_exist

    def select_option_to_view_search_with(self, view_search_options):
        old_values_to_return = self.base_selenium.get_attribute(element='configurations_page:view_search_ddl',
                                                                attribute='innerText')

        self.clear_all_selected_view_and_search_options()
        for view_search_option in view_search_options:
            if view_search_option != '':
                self.base_selenium.select_item_from_drop_down(element='configurations_page:view_search_ddl',
                                                              item_text=view_search_option.replace('×',''))
        self.base_selenium.click(element='configurations_page:popup_save_button')
        self.sleep_small()
        self.base_selenium.click(element='configurations_page:save_button')
        self.sleep_small()

        return old_values_to_return

    def deselect_all_options_to_view_search_with(self):
        old_values_to_return = self.base_selenium.get_attribute(element='configurations_page:view_search_ddl',
                                                                attribute='innerText')

        self.clear_all_selected_view_and_search_options()
        self.base_selenium.click(element='configurations_page:popup_save_button')
        self.sleep_small()
        self.base_selenium.click(element='configurations_page:confirm_button')
        self.sleep_small()
        self.base_selenium.click(element='configurations_page:save_button')
        self.sleep_small()

        return old_values_to_return

    def get_active_fields_tab(self):
        self.info('get active fields tab')
        self.base_selenium.click(element='configurations_page:active_fields_tab')
        self.sleep_tiny()
    
    def get_archived_fields_tab(self):
        self.info('get archived fields tab')
        self.base_selenium.click(element='configurations_page:archived_fields_tab')
        self.sleep_tiny()

    def archive_quantification_limit_field(self):
        self.base_selenium.LOGGER.info('archive quantification limit field')
        self.get_active_fields_tab()
        element_exists = self.base_selenium.check_element_is_exist(element='test_unit:configuration_testunit_useQuantification')
        if element_exists == False:
            self.info('quantification already archived')
            return False
        self.base_selenium.click(element='configurations_page:grouped_fields_option_menu')
        self.base_selenium.click(element='configurations_page:archive_field')
        self.confirm_popup()
        self.sleep_tiny()
        return True

    def restore_quantification_limit_field(self):
        self.base_selenium.LOGGER.info('restore quantification limit field')
        self.get_archived_items()
        self.sleep_tiny()
        element_exists = self.base_selenium.check_element_is_exist(element='test_unit:configuration_testunit_useQuantification')
        if element_exists == False:
            self.info('quantification is not archived')
            return False
        self.base_selenium.click(element='configurations_page:grouped_fields_option_menu')
        self.base_selenium.click(element='configurations_page:restore_field')
        self.confirm_popup()
        self.sleep_tiny()
        return True

