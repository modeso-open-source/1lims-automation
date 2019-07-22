from ui_testing.pages.testunits_page import TestUnits


class TestUnit(TestUnits):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")
