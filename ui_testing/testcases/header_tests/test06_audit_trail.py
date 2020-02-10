from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
from unittest import skip
import re


class AuditTrailTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.audit_trail_page.get_audit_trails_page()

    @skip('https://modeso.atlassian.net/browse/LIMS-6399')
    def test001_download_audit_trail_sheet(self):
        """
        Header: Audit trail: Make sure that you can export all the fields in the active table

        ** NB ** Everybody using the system should stop while this test case is running, because
        the export gets the latest info in the server while the rows are not the latest ** NB ** 

        LIMS-6357
        """
        self.audit_trail_page.info(' + Download XSLX sheet')
        self.audit_trail_page.download_xslx_sheet()
        rows_data = self.audit_trail_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.audit_trail_page.info(
                ' + Comparing the audit trail no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.audit_trail_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)

    def test002_audit_trail_filter_by_action_date(self):
        """
        Header: Audit trail Approach: Make sure that I can filter by all the following fields 
        ( action date & entity & action & entity no & changed by )

        LIMS-6357
        """
        # get random row data
        audit_trail = self.audit_trail_page.get_random_mapped_audit_trail_data()
        # open filter menu
        self.audit_trail_page.open_filter_menu()
        # filter by Action Date
        result = self.audit_trail_page.filter_audit_trail_by(
            filter_name='action_date', filter_text=audit_trail['action_date'], field_type='text')
        self.assertIn(audit_trail['action_date'], result)

    def test003_audit_trail_filter_by_changed_by(self):
        """
        Header: Audit trail Approach: Make sure that I can filter by all the following fields 
        ( action date & entity & action & entity no & changed by )

        LIMS-6357
        """
        # get random row data
        audit_trail = self.audit_trail_page.get_random_mapped_audit_trail_data()
        # open filter menu
        self.audit_trail_page.open_filter_menu()
        # filter by Change By
        result = self.audit_trail_page.filter_audit_trail_by(
            filter_name='changed_by', filter_text=audit_trail['changed_by'], field_type='drop_down')
        self.assertIn(audit_trail['changed_by'], result)

    def test004_audit_trail_filter_by_action(self):
        """
        Header: Audit trail Approach: Make sure that I can filter by all the following fields 
        ( action date & entity & action & entity no & changed by )

        LIMS-6357
        """
        # get random row data
        audit_trail = self.audit_trail_page.get_random_mapped_audit_trail_data()
        # open filter menu
        self.audit_trail_page.open_filter_menu()
        # filter by Action
        result = self.audit_trail_page.filter_audit_trail_by(
            filter_name='action', filter_text=audit_trail['action'], field_type='drop_down')
        self.assertIn(audit_trail['action'], result)

    def test005_audit_trail_filter_by_entity(self):
        """
        Header: Audit trail Approach: Make sure that I can filter by all the following fields 
        ( action date & entity & action & entity no & changed by )

        LIMS-6357
        """
        # get random row data
        audit_trail = self.audit_trail_page.get_random_mapped_audit_trail_data()
        # open filter menu
        self.audit_trail_page.open_filter_menu()
        # filter by Change By
        result = self.audit_trail_page.filter_audit_trail_by(
            filter_name='entity', filter_text=audit_trail['entity'], field_type='drop_down')
        self.assertIn(audit_trail['entity'], result)

    def test006_audit_trail_filter_by_entity_number(self):
        """
        Header: Audit trail Approach: Make sure that I can filter by all the following fields 
        ( action date & entity & action & entity no & changed by )

        LIMS-6357
        """
        # get random row data
        audit_trail = self.audit_trail_page.get_random_mapped_audit_trail_data()
        # open filter menu
        self.audit_trail_page.open_filter_menu()
        # filter by Change By
        result = self.audit_trail_page.filter_audit_trail_by(
            filter_name='entity_number', filter_text=audit_trail['entity_number'], field_type='text')
        self.assertIn(audit_trail['entity_number'], result)

    @parameterized.expand(['changed_by', 'action', 'entity', 'entity_number'])
    def test003_search_audit_trail(self, search_feild):
        """
        Header: Audit trail: Approach: Make sure that you can search by all the followings entities 
        ( entity & action & entity no & changed by )

        LIMS-6356
        """
        # get random row data
        audit_trail = self.audit_trail_page.get_random_mapped_audit_trail_data()
        # search by changed by
        result = self.audit_trail_page.search(audit_trail[search_feild])[0].text
        self.assertIn(audit_trail[search_feild], result)