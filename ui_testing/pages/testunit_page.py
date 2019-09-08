from ui_testing.pages.testunits_page import TstUnits
class TstUnit(TstUnits):

    def set_method(self, method=''):
        self.base_selenium.set_text(element='test_unit:method', value=method)

    def get_method(self):
        return self.base_selenium.get_value(element='test_unit:method').split('\n')[0]
    
    def set_material_type(self, material_type=''):
        if material_type:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:materialType', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:materialType')
            return self.get_material_type()

    def get_material_type(self):
        return self.base_selenium.get_text(element='test_unit:materialType').split('\n')

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
        return self.base_selenium.get_value(element='test_unit:testunitName').split('\n')[0]

    def set_testunit_number(self, number=''):
        self.base_selenium.set_text(element='test_unit:testunitNumber', value=number)

    def get_testunit_number(self):
        return self.base_selenium.get_value(element='test_unit:testunitNumber').split('\n')[0].replace("'", "")

    def set_testunit_iteration(self, iteration=''):
        self.base_selenium.set_text(element='test_unit:iteration', value=iteration)

    def get_testunit_iteration(self):
        return self.base_selenium.get_value(element='test_unit:iteration').split('\n')[0]
    
    def saveAndCreateNewVersion (self, confirm=True):
        self.save(save_btn='general:saveAndComplete', loggerMsg='Save And Create New Version')
        self.sleep_small()
        self.confirm_popup(force=confirm)
        self.sleep_small()

    def set_testunit_type (self, testunitType=''):
        if testunitType:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:type', item_text=testunitType)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:type')

    def use_specification_or_quantification(self, typeToUse='spec'):
        if typeToUse == 'spec':
            self.base_selenium.click(element='test_unit:useSpecification')
        else:
            self.base_selenium.click(element='test_unit:useQuantification')
        self.sleep_tiny()

    def set_spec_upper_limit(self, value=''):
        self.base_selenium.set_text(element='test_unit:specUpperLimit', value=value)
    
    def set_spec_lower_limit(self, value=''):
        self.base_selenium.set_text(element='test_unit:sepcLowerLimit', value=value)

    def set_spec_unit(self, value=''):
        self.base_selenium.set_text(element='test_unit:specUnit', value=value)

    def set_quan_upper_limit(self, value=''):
        self.base_selenium.set_text(element='test_unit:quanUpperLimit', value=value)

    def set_quan_lower_limit(self, value=''):
        self.base_selenium.set_text(element='test_unit:quanLowerLimit', value=value)

    def set_quan_unit(self, value=''):
        self.base_selenium.set_text(element='test_unit:quanUnit', value=value)

    def get_spec_upper_limit(self):
        return self.base_selenium.get_value(element='test_unit:specUpperLimit').split('\n')[0]
    
    def get_spec_lower_limit(self):
        return self.base_selenium.get_value(element='test_unit:sepcLowerLimit').split('\n')[0]

    def get_spec_unit(self):
        return self.base_selenium.get_value(element='test_unit:specUnit').split('\n')[0]

    def get_quan_upper_limit(self):
        return self.base_selenium.get_value(element='test_unit:quanUpperLimit').split('\n')[0]

    def get_quan_lower_limit(self):
        return self.base_selenium.get_value(element='test_unit:quanLowerLimit').split('\n')[0]

    def get_quan_unit(self):
        return self.base_selenium.get_value(element='test_unit:quanUnit').split('\n')[0]