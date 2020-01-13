from ui_testing.pages.analyses_page import AllAnalysesPage

class SingleAnalysisPage(AllAnalysesPage):

    '''
    Opens the accordion for a specific analysis given its index
    '''
    def open_accordion_for_analysis_index(self, index=0):
        all_accordion_items = self.base_selenium.find_element('analysis_page:all_rows')  
        required_row = all_accordion_items[index + 1] # index is increased by 1 because index 0 is the header element
        required_accordion_item_clickable_item = self.base_selenium.find_element_in_element(source=required_row, destination_element='analysis_page:accordion_item')
        required_accordion_item_clickable_item.click()
        self.sleep_medium()

        return required_row
        
    def get_testunits_in_analysis(self, source):
        testunits = []
        testunits_table = self.base_selenium.find_element_in_element(source=source, destination_element='analysis_page:testunits_table')
        rows = self.base_selenium.get_table_rows(source=testunits_table)
        for row in rows:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(table_element='analysis_page:testunits_table', row=row)
            testunits.append(row_data)

        return testunits
