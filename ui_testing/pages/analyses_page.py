from ui_testing.pages.base_pages import BasePages


class AllAnalysesPage(BasePages):
    def __init__(self):
        super().__init__()
        self.analyses = "{}sample/analysis".format(self.base_selenium.url)

    def get_analysis_page(self):
        self.base_selenium.get(url=self.analyses)
        self.wait_until_page_is_loaded()

    def filter_by_analysis_number(self, filter_text):
        self.info('Filter by analysis number : {}'.format(filter_text))
        self.open_filter_menu()
        self.filter_by(filter_element='analysis_page:analysis_no_filter', filter_text=str(filter_text), field_type='text')
        self.filter_apply()

    def filter_by_order_no(self, filter_text):
        self.info('Filter by order number : {}'.format(filter_text))
        self.open_filter_menu()
        self.filter_by(filter_element='analysis_page:order_no_filter',
                       filter_text=str(filter_text), field_type='drop_down')
        self.filter_apply()

    def filter_by_order_no(self, filter_text):
        self.info('Filter by order no. : {}'.format(filter_text))
        self.open_filter_menu()
        self.filter_by(filter_element='orders:filter_order_no',
                       filter_text=filter_text.replace("'", ""), field_type='drop_down')
        self.filter_apply()
