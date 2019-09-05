from ui_testing.pages.testunits_page import TstUnits


class TstUnit(TstUnits):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")

    def set_method(self, method=''):
        self.base_selenium.set_text(element='test_unit:method', value=method)

    def get_method(self):
        return self.base_selenium.get_text(element='order:article').split('\n')[0]
    
    def saveAndCreateNewVersion (self, confirm=True):
        self.save(save_btn='general:saveAndComplete', loggerMsg='Save And Create New Version')
        self.sleep_small()
        self.confirm_popup(force=confirm)
        self.sleep_small()
        