from ui_testing.pages.base_pages import BasePages

class AuditTrail(BasePages):
    def __init__(self):
        super().__init__()
        self.audit_trails_url = "{}auditTrails".format(self.base_selenium.url)

    def get_audit_trails_page(self):
        self.base_selenium.get(url=self.audit_trails_url)
        self.sleep_small()

    def download_xslx_sheet(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='general:right_menu')
        self.sheet = self.base_selenium.download_excel_file(element='general:xslx')

    def get_table_rows_data(self):
        return [row.text for row in self.base_selenium.get_table_rows(element='general:table')]                      

    def filter_audit_trail_by(self, filter_name , filter_text, field_type='drop_down'):
        self.base_selenium.LOGGER.info(' + Filter by test plan : {}'.format(filter_text))
        self.filter_by(filter_element='audit_trail:filter_{}'.format(filter_name), filter_text=filter_text, field_type=field_type)
        self.filter_apply()
        self.sleep_tiny()

    def get_random_audit_trail_row(self):
         return self.get_random_table_row(table_element='general:table')
