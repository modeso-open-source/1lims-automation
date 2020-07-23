from ui_testing.pages.base_pages import BasePages

class AuditTrail(BasePages):
    def __init__(self):
        super().__init__()
        self.audit_trails_url = "{}auditTrails".format(self.base_selenium.url)

    def get_audit_trails_page(self):
        self.base_selenium.get(url=self.audit_trails_url)
        self.wait_until_page_is_loaded()

    def filter_audit_trail_by(self, filter_name, filter_text, field_type='drop_down'):
        self.base_selenium.LOGGER.info(' + Filter by test plan : {}'.format(filter_text))
        self.filter_by(filter_element='audit_trail:filter_{}'.format(filter_name),
                       filter_text=filter_text, field_type=field_type)
        self.filter_apply()
        self.sleep_tiny()
        return self.get_table_rows_data()[0]

    def get_random_mapped_audit_trail_data(self):
        # get random row in the table
        audit_trail_row = self.get_random_table_row(table_element='general:table')
        # map the header to the row data
        audit_trail_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=audit_trail_row)
        # get each column data from that row
        return {
            # 'action_date': audit_trail_row_data['Action Date'].split(',')[0], # get only the date
            'changed_by': audit_trail_row_data['Changed By'],
            'action': audit_trail_row_data['Action'],
            'entity': audit_trail_row_data['Entity'],
            'entity_number': audit_trail_row_data['Entity Number'],
        }