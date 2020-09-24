from ui_testing.pages.analyses_page import AllAnalysesPage


class SingleAnalysisPage(AllAnalysesPage):
    '''
    Opens the accordion for a specific analysis given its index
    '''
    def open_accordion_for_analysis_index(self, index=0):
        all_accordion_items = self.base_selenium.find_element('analysis_page:all_rows')
        required_row = all_accordion_items[index + 1] # index is increased by 1 because index 0 is the header element
        required_accordion_item_clickable_item = self.base_selenium.find_element_in_element(
            source=required_row, destination_element='analysis_page:accordion_item')
        required_accordion_item_clickable_item.click()
        self.sleep_medium()

        return required_row
        
    def get_testunits_in_analysis(self, source):
        testunits = []
        testunits_table = self.base_selenium.find_element_in_element(
            source=source, destination_element='analysis_page:testunits_table')
        rows = self.base_selenium.get_table_rows(source=testunits_table)
        for row in rows:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(
                table_element='analysis_page:testunits_table', row=row)
            testunits.append(row_data)

        return testunits

    def get_analysis_count(self):
        all_accordion_items = self.base_selenium.find_element('analysis_page:all_rows')
        return len(all_accordion_items)-1

    def navigate_to_order_tab(self):
        self.base_selenium.click('orders:order_analysis_tab')
        self.sleep_small()

    def get_all_analysis_records(self):
        headers = self.get_analysis_headers()
        analysis_count = self.get_analysis_count()

        full_analysis_main_data = self.get_records_data(analysis_count)
        analysis_mapped_data = []
        for record in full_analysis_main_data:
            temp_record = {}
            for header in headers:
                temp_record[header] = record[headers.index(header)]
            analysis_mapped_data.append(temp_record)
        
        return analysis_mapped_data

    def get_analysis_headers(self):
        headers = self.base_selenium.find_elements_in_element(
            source_element='analysis_page:headers', destination_element='general:th')
        header_list = []
        for header in headers:
            if header.text != 'Attachments' and header.text != 'Save' and \
                    header.text != 'Arrival Date' and header.text != '':
                header_list.append(header.text)

        return header_list

    def get_records_data(self, analysis_count):
        records_data = []
        for i in range(0, analysis_count):
            analysis_record = self.base_selenium.find_element_by_xpath(
                xpath='//div[@id="m_accordion_7_item_head_{}"]'.format(i))
            cells = self.base_selenium.find_elements_in_element(
                source=analysis_record, destination_element='general:td')
            temp_record = []
            for cell in cells:
                if cell.text != '':
                    temp_record.append(cell.text)
            records_data.append(temp_record)
        return records_data

    def set_testunit_values(self, lower=0, upper=100, save= True):
        self.open_accordion_for_analysis_index()
        testunit_value_fields = self.base_selenium.find_elements(element='analysis_page:testunits_analysis')
        value = self.generate_random_number(lower=lower, upper=upper)
        for field in testunit_value_fields:
            field.clear()
            field.send_keys(value)
        if save:
            self.base_selenium.click(element='general:save')
        return value

    def change_validation_options(self, text=''):
        if text:
            self.base_selenium.select_item_from_drop_down(
                element='analysis_page:validation_options', item_text=text, options_element='general:drop_down_div')
        else:
            self.base_selenium.select_item_from_drop_down(
                element='analysis_page:validation_options', options_element='general:drop_down_div')

        self.base_selenium.click(element='analysis_page:save_analysis')
        self.sleep_small()
        return self.get_validation_option().split('\n')[0]

    def get_validation_option(self):
        return self.base_selenium.get_text(element='analysis_page:validation_options')