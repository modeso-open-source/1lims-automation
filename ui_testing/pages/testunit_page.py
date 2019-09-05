from ui_testing.pages.testunits_page import TstUnits
class TstUnit(TstUnits):

    def set_method(self, method=''):
        self.base_selenium.set_text(element='test_unit:method', value=method)

    def get_method(self):
        return self.base_selenium.get_text(element='test_unit:article').split('\n')[0]
    
    def set_material_type(self, material_type=''):
        if material_type:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:materialType', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:materialType')
            return self.get_material_type()

    def get_material_type(self):
        return self.base_selenium.get_text(element='test_unit:materialType').split('\n').join(',')

    def set_category(self, category=''):
        if category:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:category', item_text=category)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:category')
            return self.get_category()

    def get_category(self):
        return self.base_selenium.get_text(element='test_unit:category').split('\n')[0]

    def set_testunit_name(self, name=''):
        self.base_selenium.set_text(element='test_unit:testunitName', value=name)

    def get_testunit_name(self):
        return self.base_selenium.get_text(element='test_unit:testunitName').split('\n')[0]

    def set_testunit_number(self, number=''):
        self.base_selenium.set_text(element='test_unit:testunitNumber', value=number)

    def get_testunit_number(self):
        return self.base_selenium.get_text(element='test_unit:testunitNumber').split('\n')[0]

    def set_testunit_iteration(self, iteration=''):
        self.base_selenium.set_text(element='test_unit:iteration', value=iteration)

    def get_testunit_iteration(self):
        return self.base_selenium.get_text(element='test_unit:iteration').split('\n')[0]
    
    def saveAndCreateNewVersion (self, confirm=True):
        self.save(save_btn='general:saveAndComplete', loggerMsg='Save And Create New Version')
        self.sleep_small()
        self.confirm_popup(force=confirm)
        self.sleep_small()
        