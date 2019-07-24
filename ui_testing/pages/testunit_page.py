from ui_testing.pages.testunits_page import TstUnits


class TstUnit(TstUnits):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")
