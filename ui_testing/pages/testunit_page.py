from ui_testing.pages.testunits_page import TstUnits
class TstUnit(TstUnits):

    def set_method(self, method=''):
        self.base_selenium.LOGGER.info('Set testunit method to be: {}'.format(method))
        self.base_selenium.set_text(element='test_unit:method', value=method)

    def get_method(self):
        self.base_selenium.LOGGER.info('Get testunit method')
        return self.base_selenium.get_value(element='test_unit:method').split('\n')[0]

    def click_create_new_testunit(self):
        self.base_selenium.LOGGER.info('Click Create New Test Unit')
        self.base_selenium.click(element='test_units:newTestunit')
        self.sleep_tiny()

    def create_new_testunit(self, name='', materialType='', category='', testunitType='', specOrQuan='', upperLimit='', lowerLimit='', unit='', iteration='', method=''):
        self.click_create_new_testunit()
        self.set_testunit_name(name=name)
        self.set_material_type(material_type=materialType)
        self.set_category(category=category)
        self.set_testunit_type(testunitType=testunitType)

        if testunitType == 'Quantitative':
            self.use_specification_or_quantification(typeToUse=specOrQuan)
            if specOrQuan == 'spec':
                self.set_spec_upper_limit(value=upperLimit)
                self.set_spec_lower_limit(value=lowerLimit)
                self.set_spec_unit(value=unit)
            elif specOrQuan == 'quan':
                self.set_quan_upper_limit(value=upperLimit)
                self.set_quan_lower_limit(value=lowerLimit)
                self.set_quan_unit(value=unit)

        self.set_testunit_iteration(iteration=iteration)
        self.set_method(method=method)

    
    def set_material_type(self, material_type=''):
        self.base_selenium.LOGGER.info('Set material type to be " {} ", if it is empty, then it will be random'.format(material_type))
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
        self.base_selenium.LOGGER.info('Set category to be " {} ", if it is empty, then it will be random'.format(category))
        if category:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:category', item_text=category)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:category')
            return self.get_category()

    def get_category(self):
        self.base_selenium.LOGGER.info('Get Testunit category')
        return self.base_selenium.get_text(element='test_unit:category').split('\n')[0]

    def set_testunit_name(self, name=''):
        self.base_selenium.LOGGER.info('Set testunit name to be: {}'.format(name))
        self.base_selenium.set_text(element='test_unit:testunitName', value=name)

    def get_testunit_name(self):
        self.base_selenium.LOGGER.info('Get Testunit name')
        return self.base_selenium.get_value(element='test_unit:testunitName').split('\n')[0]

    def set_testunit_number(self, number=''):
        self.base_selenium.LOGGER.info('Set testunit number to be: {}'.format(number))
        self.base_selenium.set_text(element='test_unit:testunitNumber', value=number)

    def get_testunit_number(self):
        self.base_selenium.LOGGER.info('Get testunit number')
        return self.base_selenium.get_value(element='test_unit:testunitNumber').split('\n')[0].replace("'", "")

    def set_testunit_iteration(self, iteration=''):
        self.base_selenium.LOGGER.info('Set testunit iterations to be: {}'.format(iteration))
        self.base_selenium.set_text(element='test_unit:iteration', value=iteration)

    def get_testunit_iteration(self):
        self.base_selenium.LOGGER.info('Get testunit iterations')
        return self.base_selenium.get_value(element='test_unit:iteration').split('\n')[0]
    
    def saveAndCreateNewVersion (self, confirm=True):
        self.save(save_btn='general:saveAndComplete', loggerMsg='Save And Create New Version')
        self.sleep_small()
        self.confirm_popup(force=confirm)
        self.sleep_small()

    def set_testunit_type (self, testunitType=''):
        self.base_selenium.LOGGER.info('Set testunit type to be {}'.format(testunitType))
        if testunitType:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:type', item_text=testunitType)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:type')

    def use_specification_or_quantification(self, typeToUse='spec'):
        self.base_selenium.LOGGER.info('Check to use {}'.format(typeToUse))
        if typeToUse == 'spec':
            self.base_selenium.click(element='test_unit:useSpecification')
        elif typeToUse == 'quan':
            self.base_selenium.click(element='test_unit:useQuantification')
        self.sleep_tiny()

    def set_spec_upper_limit(self, value=''):
        self.base_selenium.LOGGER.info('Set specification upper limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:specUpperLimit', value=value)
    
    def set_spec_lower_limit(self, value=''):
        self.base_selenium.LOGGER.info('Set specification lower limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:sepcLowerLimit', value=value)

    def set_spec_unit(self, value=''):
        self.base_selenium.LOGGER.info('Set specification unit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:specUnit', value=value)

    def set_quan_upper_limit(self, value=''):
        self.base_selenium.LOGGER.info('Set quantification upper limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:quanUpperLimit', value=value)

    def set_quan_lower_limit(self, value=''):
        self.base_selenium.LOGGER.info('Set quantification lower limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:quanLowerLimit', value=value)

    def set_quan_unit(self, value=''):
        self.base_selenium.LOGGER.info('Set quantification unit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:quanUnit', value=value)

    def get_spec_upper_limit(self):
        self.base_selenium.LOGGER.info('Get testunit specification upper limit')
        return self.base_selenium.get_value(element='test_unit:specUpperLimit').split('\n')[0]
    
    def get_spec_lower_limit(self):
        self.base_selenium.LOGGER.info('Get testunit specification lower limit')
        return self.base_selenium.get_value(element='test_unit:sepcLowerLimit').split('\n')[0]

    def get_spec_unit(self):
        self.base_selenium.LOGGER.info('Get testunit specification unit')
        return self.base_selenium.get_value(element='test_unit:specUnit').split('\n')[0]

    def get_quan_upper_limit(self):
        self.base_selenium.LOGGER.info('Get testunit quantification upper limit')
        return self.base_selenium.get_value(element='test_unit:quanUpperLimit').split('\n')[0]

    def get_quan_lower_limit(self):
        self.base_selenium.LOGGER.info('Get testunit quantification lower limit')
        return self.base_selenium.get_value(element='test_unit:quanLowerLimit').split('\n')[0]

    def get_quan_unit(self):
        self.base_selenium.LOGGER.info('Get testunit qunatification unit')
        return self.base_selenium.get_value(element='test_unit:quanUnit').split('\n')[0]