from ui_testing.pages.base_pages import BasePages


class TestPlans(BasePages):
    def __init__(self):
        super().__init__()
        self.test_plans_url = "{}testPlans".format(self.base_selenium.url)

    def get_test_plans_page(self):
        self.info(' Get test plans page.')
        self.base_selenium.get(url=self.test_plans_url)
        self.wait_until_page_is_loaded()

    def get_test_plan_edit_page_by_id(self, id):
        url_text = "{}testPlans/edit/" + str(id)
        self.base_selenium.get(url=url_text.format(self.base_selenium.url))
        self.wait_until_page_is_loaded()

    def get_random_test_plans(self):
        row = self.get_random_table_row('test_plans:test_plans_table')
        self.open_edit_page(row=row)

    def click_create_test_plan_button(self):
        self.base_selenium.click(element='test_plans:new_test_plan')
        self.sleep_small()

    def get_test_plan_edit_page(self, name):
        self.info('Navigating to testplan {} edit page'.format(name))
        test_plan = self.search(value=name)[0]
        self.sleep_small()
        self.open_edit_page_by_css_selector(row=test_plan, css_selector='')
        self.wait_until_page_is_loaded()

    def get_testunits_in_testplans(self, test_plan_name=''):
        self.info('Search by testplan name {}'.format(test_plan_name))
        self.search(value=test_plan_name)
        new_testplan_testunits=self.get_child_table_data(index=0)

        testplan_testunits = []
        for testunit in new_testplan_testunits:
            testplan_testunits.append(testunit['Test Unit Name'])
    
        return testplan_testunits

    def get_testplan_version_and_status(self, search_text):
        testplan = self.search(search_text)[0]
        testplan_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=testplan)
        testplan_version = testplan_row_data['Version']
        testplan_status = testplan_row_data['Status']
        return testplan_version, testplan_status
        
    def get_specific_testplan_data_and_childtable_data(self, filter_by='number', filter_text=''):
        if filter_by == 'number':
            self.filter_by_testplan_number(filter_text=filter_text)
        found_testplan = self.result_table()[0]
        found_testplan_data = self.base_selenium.get_row_cells_dict_related_to_header(row=found_testplan)
        found_testplan_childtable_data = self.get_child_table_data(index=0)

        return found_testplan_data, found_testplan_childtable_data

    def filter_by_testplan_number(self, filter_text, open_filter_menu=True):
        if open_filter_menu:
            self.open_filter_menu()
        self.info('Filtering by testplan number: {}'.format(filter_text))
        self.filter_by(filter_element='test_plans:testplan_number_filter', filter_text=filter_text, field_type='text')
        self.filter_apply()

    def get_the_latest_row_data(self):
        latest_testplan_row = (self.result_table()[0])
        return self.base_selenium.get_row_cells_dict_related_to_header(latest_testplan_row)

    def filter_multiple_rows_by_testplans_numbers(self, testplans_numbers, check=0):
        """
            Searches for multiple rows with the testplans numbers as array of numbers
            The parameter check is a boolean to either allow selecting those rows or not
        """
        rows = []
        self.open_filter_menu()
        for tp_number in testplans_numbers:
            self.filter_by_testplan_number(filter_text=tp_number, open_filter_menu=False)
            row = self.result_table()
            rows.append(row[0])
            if check:
                self.info('Clicking the checkbox for testplan number: {}'.format(tp_number))
                self.click_check_box(row[0])
        return rows

    def filter_by_element_and_get_results(self, fieldName, element, filter_text, fieldType):
        self.open_filter_menu()
        self.filter(fieldName, element, filter_text, fieldType)
        self.sleep_tiny()
        results_found = self.result_table()
        self.close_filter_menu()
        return results_found

    def filter_by_element_and_get_text(self, fieldName, element, filter_text, fieldType):
        testplans_found = self.filter_by_element_and_get_results(fieldName, element, filter_text, fieldType)
        testplans_found_text = [tp.text for tp in testplans_found]
        self.base_selenium.click_by_script('general:last_page')
        self.sleep_tiny()
        testplans_found_text.extend([tp.text for tp in self.result_table()])
        return filter(None, testplans_found_text)

    def search_and_get_childtable_data_for_testplan(self, testplan_name):
        self.search(testplan_name)
        self.info('Saving the child data of the main testplan')
        return self.get_child_table_data()

    def delete_selected_item_from_active_table_and_from_archived_table(self, item_name):
        self.apply_filter_scenario(filter_element='test_plans:testplan_name_filter', filter_text=item_name)
        self.close_filter_menu()
        self.sleep_small()
        row = self.result_table()
        self.info('Selecting the row')
        self.click_check_box(source=row[0])
        self.sleep_tiny()
        self.info('Archiving the selected row')
        self.archive_selected_items()
        self.info('Navigating to the Archived table')
        self.get_archived_items()
        self.apply_filter_scenario(filter_element='test_plans:testplan_name_filter', filter_text=item_name)
        self.close_filter_menu()
        archived_row = self.result_table()
        self.sleep_small()
        self.info('Selecting the row')
        self.click_check_box(source=archived_row[0])
        self.sleep_tiny()
        self.info('Attempting to delete item: {}'.format(item_name))
        self.delete_selected_item()

        if self.base_selenium.check_element_is_exist(element='general:cant_delete_message'):
            self.base_selenium.click(element='general:confirm_pop')
            return False
        return True
