from ui_testing.pages.testunits_page import TstUnit


class TstUnit(TstUnit):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")
