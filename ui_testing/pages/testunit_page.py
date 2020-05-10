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
        self.base_selenium.click(element='test_units:new_testunit')
        self.sleep_tiny()

    def create_new_testunit(self, name='', material_type='', category='', testunit_type='', spec_or_quan='',
                            upper_limit='', lower_limit='', unit='', iteration=1, method='', selected_cons=''):
        self.click_create_new_testunit()
        self.set_testunit_name(name=name)
        self.set_material_type(material_type=material_type)
        self.set_category(category=category)
        self.set_testunit_type(testunit_type=testunit_type)

        if testunit_type == 'Quantitative':
            self.use_specification_or_quantification(type_to_use=spec_or_quan)
            if spec_or_quan == 'spec':
                self.set_spec_upper_limit(value=upper_limit)
                self.set_spec_lower_limit(value=lower_limit)
                self.set_spec_unit(value=unit)
            elif spec_or_quan == 'quan':
                self.set_quan_upper_limit(value=upper_limit)
                self.set_quan_lower_limit(value=lower_limit)
                self.set_quan_unit(value=unit)
        elif testunit_type == 'Quantitative MiBi':
            self.set_spec_upper_limit(value=upper_limit)
            self.set_selected_concs(selected_cons=selected_cons)

        self.set_testunit_iteration(iteration=iteration)
        self.set_method(method=method)

    def create_qualitative_testunit(self, name='', material_type='', category='', value='', unit='', iteration=1,
                                    method=''):
        self.base_selenium.LOGGER.info('create_qualitative_testunit')
        self.click_create_new_testunit()
        self.set_testunit_name(name=name)
        self.set_material_type(material_type=material_type)
        self.set_category(category=category)
        self.set_testunit_type(testunit_type='Qualitative')
        self.set_qualitative_value(value=value)
        self.base_selenium.set_text(element='test_unit:spec_unit', value=unit)
        self.set_testunit_iteration(iteration=iteration)
        self.set_method(method=method)

    def create_quantitative_mibi_testunit(self, name='', material_type='', category='', upper_limit='',
                                          selected_cons='', iteration='1', method=''):
        self.base_selenium.LOGGER.info('create_quantitative_mibi_testunit')
        self.click_create_new_testunit()
        self.set_testunit_name(name=name)
        self.set_material_type(material_type=material_type)
        self.set_category(category=category)
        self.set_testunit_type(testunit_type='Quantitative MiBi')
        self.set_spec_upper_limit(value=upper_limit)
        self.set_selected_concs(selected_cons=selected_cons)
        self.set_testunit_iteration(iteration=iteration)
        self.set_method(method=method)

    def create_quantitative_testunit(self, name='', material_type='', category='', unit='', iteration='1',
                                    method='', upper_limit='', lower_limit='', spec_or_quan='spec'):
        self.base_selenium.LOGGER.info('create_quantitative_testunit')
        self.click_create_new_testunit()
        self.set_testunit_name(name=name)
        self.set_material_type(material_type=material_type)
        self.set_category(category=category)
        self.set_testunit_type(testunit_type='Quantitative')
        self.use_specification_or_quantification(type_to_use=spec_or_quan)
        if spec_or_quan == 'spec':
            self.set_spec_upper_limit(value=upper_limit)
            self.set_spec_lower_limit(value=lower_limit)
            self.set_spec_unit(value=unit)
        elif spec_or_quan == 'quan':
            self.set_quan_upper_limit(value=upper_limit)
            self.set_quan_lower_limit(value=lower_limit)
            self.set_quan_unit(value=unit)
        elif spec_or_quan == 'spec_quan':
            self.set_spec_upper_limit(value=upper_limit)
            self.set_spec_lower_limit(value=lower_limit)
            self.set_spec_unit(value=unit)
            self.set_quan_upper_limit(value=upper_limit)
            self.set_quan_lower_limit(value=lower_limit)
            self.set_quan_unit(value=unit)
        self.base_selenium.set_text(element='test_unit:spec_unit', value=unit)
        self.set_testunit_iteration(iteration=iteration)
        self.set_method(method=method)

    def set_material_type(self, material_type=''):
        self.base_selenium.LOGGER.info(
            'Set material type to be "{}", if it is empty, then it will be random'.format(material_type))
        if material_type:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:material_type_by_id', item_text=material_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:material_type_by_id')
            return self.get_material_type()

    def get_material_type(self):
        return self.base_selenium.get_text(element='test_unit:material_type_by_id').split('\n')

    def set_category(self, category=''):
        self.base_selenium.LOGGER.info(
            'Set category to be "{}", if it is empty, then it will be random'.format(category))
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
        self.base_selenium.set_text(element='test_unit:testunit_name', value=name)

    def get_testunit_name(self):
        self.base_selenium.LOGGER.info('Get Testunit name')
        return self.base_selenium.get_value(element='test_unit:testunit_name').split('\n')[0]

    def set_testunit_number(self, number=''):
        self.base_selenium.LOGGER.info('Set testunit number to be: {}'.format(number))
        self.base_selenium.set_text(element='test_unit:testunit_number', value=number)

    def get_testunit_number(self):
        self.base_selenium.LOGGER.info('Get testunit number')
        return self.base_selenium.get_value(element='test_unit:testunit_number').split('\n')[0].replace("'", "")

    def set_testunit_iteration(self, iteration=''):
        self.base_selenium.LOGGER.info('Set testunit iterations to be: {}'.format(iteration))
        self.base_selenium.set_text(element='test_unit:iteration', value=iteration)

    def get_testunit_iteration(self):
        self.base_selenium.LOGGER.info('Get testunit iterations')
        return self.base_selenium.get_value(element='test_unit:iteration').split('\n')[0]

    def save_and_create_new_version(self, confirm=True):
        self.save(save_btn='general:save_and_complete', logger_msg='Save And Create New Version')
        self.sleep_tiny()
        self.confirm_popup(force=confirm)
        self.sleep_tiny()

    def save_and_return_overview(self):
        self.save(save_btn='general:save_form', logger_msg='Save And update the current version')
        self.sleep_small()
        self.click_overview()
        self.sleep_small()

    def set_testunit_type(self, testunit_type=''):
        self.base_selenium.LOGGER.info('Set testunit type to be {}'.format(testunit_type))
        if testunit_type:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:type', item_text=testunit_type)
        else:
            self.base_selenium.select_item_from_drop_down(
                element='test_unit:type')

    def use_specification_or_quantification(self, type_to_use='spec'):
        self.info('Check to use {}'.format(type_to_use))
        if type_to_use == 'spec':
            spec = self.base_selenium.find_element_in_element(destination_element='general:span',
                                                              source_element='test_unit:use_specification')
            spec.click()
        elif type_to_use == 'quan':
            quan = self.base_selenium.find_element_in_element(destination_element='general:span',
                                                              source_element='test_unit:use_quantification')
            quan.click()
        elif type_to_use == "spec_quan":
            spec = self.base_selenium.find_element_in_element(destination_element='general:span',
                                                              source_element='test_unit:use_specification')
            spec.click()
            quan = self.base_selenium.find_element_in_element(destination_element='general:span',
                                                              source_element='test_unit:use_quantification')
            quan.click()

    def set_spec_upper_limit(self, value=''):
        self.base_selenium.LOGGER.info('Set specification upper limit to be {}'.format(value))
        self.sleep_tiny()
        self.base_selenium.set_text(element='test_unit:spec_upper_limit', value=value)

    def clear_spec_upper_limit(self):
        self.base_selenium.LOGGER.info('Clear specification upper limit')
        self.base_selenium.clear_text(element='test_unit:spec_upper_limit')

    def set_spec_lower_limit(self, value=''):
        self.info('Set specification lower limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:spec_lower_limit', value=value)

    def set_spec_unit(self, value=''):
        self.base_selenium.LOGGER.info('Set specification unit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:spec_unit', value=value)

    def set_quan_upper_limit(self, value=''):
        self.info('Set quantification upper limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:quan_upper_limit', value=value)

    def set_quan_lower_limit(self, value=''):
        self.info('Set quantification lower limit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:quan_lower_limit', value=value)

    def set_quan_unit(self, value=''):
        self.info('Set quantification unit to be {}'.format(value))
        self.base_selenium.set_text(element='test_unit:quan_unit', value=value)

    def get_spec_upper_limit(self):
        self.info('Get testunit specification upper limit')
        return self.base_selenium.get_value(element='test_unit:spec_upper_limit').split('\n')[0]

    def get_spec_lower_limit(self):
        self.info('Get testunit specification lower limit')
        return self.base_selenium.get_value(element='test_unit:spec_lower_limit').split('\n')[0]

    def get_spec_unit(self):
        self.info('Get testunit specification unit')
        return self.base_selenium.get_value(element='test_unit:spec_unit').split('\n')[0]

    def get_spec_unit_preview(self):
        self.info('Get testunit specification unit preview')
        return self.base_selenium.get_attribute(element='test_unit:spec_unit_preview',attribute='textContent').split('\n')[0]

    def get_quan_upper_limit(self):
        self.info('Get testunit quantification upper limit')
        return self.base_selenium.get_value(element='test_unit:quan_upper_limit').split('\n')[0]

    def get_quan_lower_limit(self):
        self.info('Get testunit quantification lower limit')
        return self.base_selenium.get_value(element='test_unit:quan_lower_limit').split('\n')[0]

    def get_quan_unit(self):
        self.base_selenium.LOGGER.info('Get testunit qunatification unit')
        return self.base_selenium.get_value(element='test_unit:quan_unit').split('\n')[0]

    def set_selected_concs(self, selected_cons=''):
        self.base_selenium.LOGGER.info('Set selected cons : {}'.format(selected_cons))
        self.base_selenium.select_item_from_drop_down(element='test_unit:selected_cons', item_text=selected_cons)

    def clear_cons(self):
        self.base_selenium.LOGGER.info('Clear selected concentrations')
        self.base_selenium.clear_items_in_drop_down(element='test_unit:selected_cons')

    def set_qualitative_value(self, value=''):
        value = value or self.generate_random_number()
        qualitative_value = self.base_selenium.find_element_in_element(destination_element='general:input',
                                                                       source_element='test_unit:qualitative_value')
        qualitative_value.send_keys(value)

    def check_for_quantitative_fields(self):
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:use_specification')
        
        if element_exist:
            self.base_selenium.LOGGER.info('checkbox for specification does exist')
        else:
            self.base_selenium.LOGGER.info('checkbox for specification is not shown, report a BUG')
            return False

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_upper_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('upper limit for specification does exist')
        else:
            self.base_selenium.LOGGER.info('upper limit for specification is not shown, report a BUG')
            return False

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_lower_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('lower limit for specification does exist')
        else:
            self.base_selenium.LOGGER.info('lower limit for specification is not shown, report a BUG')
            return False
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_unit')
        if element_exist :
            self.base_selenium.LOGGER.info('unit for specification does exist')
        else:
            self.base_selenium.LOGGER.info('unit for specification is not shown, report a BUG')
            return False
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:use_quantification')
        if element_exist :
            self.base_selenium.LOGGER.info('checkbox for quantification does exist')
        else:
            self.base_selenium.LOGGER.info('checkbox for quantification is not shown, report a BUG')
            return False
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_upper_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('upper limit for quantification does exist')
        else:
            self.base_selenium.LOGGER.info('upper limit for quantification is not shown, report a BUG')
            return False

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_lower_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('lower limit for quantification does exist')
        else:
            self.base_selenium.LOGGER.info('lower limit for quantification is not shown, report a BUG')
            return False

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_unit')
        if element_exist :
            self.base_selenium.LOGGER.info('unit for quantification does exist')
        else:
            self.base_selenium.LOGGER.info('unit for quantification is not shown, report a BUG')
            return False

        # ------------------------------------------------------------------------------------------------
        self.base_selenium.LOGGER.info('checking for fields that does not suppoe to be shown in quantitative')
        # ------------------------------------------------------------------------------------------------

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:selected_cons')
        if element_exist :
            self.base_selenium.LOGGER.info('Concentration field for quantitative mibi is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('Concentration field for quantitative mibi does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:qualitative_value')
        if element_exist :
            self.base_selenium.LOGGER.info('Qualitative value is not shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('Qualitative value does exist')

            
        return True

    def check_for_qualitative_fields(self):
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_unit')
        if element_exist :
            self.base_selenium.LOGGER.info('checkbox for specification does exist')
        else:
            self.base_selenium.LOGGER.info('unit field for specification is not shown, report a BUG')
            return False

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:qualitative_value')
        if element_exist :
            self.base_selenium.LOGGER.info('Qualitative value does exist')
        else:
            self.base_selenium.LOGGER.info('Qualitative value is not shown, report a BUG')
            return False
        
        # ------------------------------------------------------------------------------------------------
        self.base_selenium.LOGGER.info('checking for fields that does not suppoe to be shown in qualitative')
        # ------------------------------------------------------------------------------------------------

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:use_specification')
        if element_exist:
            self.base_selenium.LOGGER.info('checkbox for specification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('checkbox for specification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_upper_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('upper limit for specification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('upper limit for specification does not exist')
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:use_quantification')
        if element_exist :
            self.base_selenium.LOGGER.info('checkbox for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('checkbox for quantification does not exist')
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_upper_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('upper limit for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('upper limit for quantification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_lower_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('lower limit for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('lower limit for quantification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_unit')
        if element_exist :
            self.base_selenium.LOGGER.info('unit for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('unit for quantification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:selected_cons')
        if element_exist :
            self.base_selenium.LOGGER.info('Concentration field for quantitative mibi is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('Concentration field for quantitative mibi does not exist')

        return True

    def check_for_quantitative_mibi_fields(self):
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_upper_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('upper limit field for quantative mibi does exist')
        else:
            self.base_selenium.LOGGER.info('upper limit field for quantitative mibi is not shown, report a BUG')
            return False

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_unit')
        if element_exist :
            self.base_selenium.LOGGER.info('Unit field for quantitative mibi does exist')
        else:
            self.base_selenium.LOGGER.info('Unit field for quantitative mibi is not shown, report a BUG')
            return False
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:selected_cons')
        if element_exist :
            self.base_selenium.LOGGER.info('Concentration field for quantitative mibi does exist')
        else:
            self.base_selenium.LOGGER.info('Concentration field for quantitative mibi is not shown, report a BUG')
            return False

        # ------------------------------------------------------------------------------------------------
        self.base_selenium.LOGGER.info('checking for fields that does not suppoe to be shown in quantitative mibi')
        # ------------------------------------------------------------------------------------------------

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:use_specification')
        if element_exist:
            self.base_selenium.LOGGER.info('checkbox for specification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('checkbox for specification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:spec_lower_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('lower limit for specification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('lower limit for specification does not exist')
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:use_quantification')
        if element_exist :
            self.base_selenium.LOGGER.info('checkbox for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('checkbox for quantification does not exist')
        
        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_upper_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('upper limit for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('upper limit for quantification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_lower_limit')
        if element_exist :
            self.base_selenium.LOGGER.info('lower limit for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('lower limit for quantification does not exist')

        element_exist = self.base_selenium.check_element_is_exist(element='test_unit:quan_unit')
        if element_exist :
            self.base_selenium.LOGGER.info('unit for quantification is shown, report a BUG')
            return False
        else:
            self.base_selenium.LOGGER.info('unit for quantification does not exist')

        return True

    def get_testunit_specification_type(self):
        
        specification_checkbox_value = self.base_selenium.find_element(element='test_unit:specification_checkbox').is_selected()

        quantification_checkbox_value = self.base_selenium.find_element(element='test_unit:quantification_checkbox').is_selected()

        self.base_selenium.LOGGER.info(specification_checkbox_value)
        self.base_selenium.LOGGER.info(quantification_checkbox_value)
        if specification_checkbox_value and quantification_checkbox_value:
            return 'spec_quan'
        elif specification_checkbox_value:
            return 'spec'
        elif quantification_checkbox_value:
            return 'quan'

    def switch_from_spec_to_quan(self, lower_limit, upper_limit):
        self.sleep_tiny()
        self.use_specification_or_quantification(type_to_use='spec') #to deslect spec
        self.use_specification_or_quantification(type_to_use='quan') #to select quan
        self.sleep_tiny()
        self.set_quan_lower_limit(value=lower_limit)
        self.sleep_tiny()
        self.set_quan_upper_limit(value=upper_limit)
        self.sleep_tiny()
        self.save(save_btn='general:save_form', logger_msg='Save testunit', sleep=True)

    def switch_from_quan_to_spec(self, lower_limit, upper_limit):
        self.sleep_tiny()
        self.use_specification_or_quantification(type_to_use='quan')
        self.use_specification_or_quantification(type_to_use='spec')
        self.sleep_tiny()
        self.set_spec_lower_limit(value=lower_limit)
        self.sleep_tiny()
        self.set_spec_upper_limit(value=upper_limit)
        self.sleep_tiny()
        self.save(save_btn='general:save_form', logger_msg='Save testunit', sleep=True)

    def map_testunit_to_testplan_format(self, testunit, order=0):
        testunit_formated = {}
        testunit_formated['id'] = testunit['id']
        testunit_formated['comment'] = testunit['comment']
        testunit_formated['testUnitTypeId'] = testunit['type']['id']
        testunit_formated['method'] = testunit['method']
        testunit_formated['typeName'] = testunit['typeName']
        testunit_formated['name'] = testunit['name']
        testunit_formated['unit'] = testunit['unit']
        testunit_formated['number'] = testunit['number']
        testunit_formated['category'] = testunit['category']['name']
        testunit_formated['iterations'] = testunit['iterations']
        testunit_formated['order'] = order
        testunit_formated['testunitVersion'] = testunit['version']

        if testunit_formated['testUnitTypeId'] == 1:
            return self.map_qualtiative_testunit(testunit_formated=testunit_formated, testunit=testunit)
        elif testunit_formated['testUnitTypeId'] == 2:
            return self.map_quantiative_testunit(testunit_formated=testunit_formated, testunit=testunit)
        elif testunit_formated['testUnitTypeId'] == 3:
            return self.map_mibi_testunit(testunit_formated=testunit_formated, testunit=testunit)

    def map_qualtiative_testunit(self, testunit_formated, testunit):
            testunit_formated['useSpec'] = False
            testunit_formated['useQuantification'] = False
            testunit_formated['upperLimit'] = ''
            testunit_formated['mibiValue'] = ''
            testunit_formated['quantificationUpperLimit'] = ''
            testunit_formated['quantificationLowerLimit'] = ''
            testunit_formated['concentrations'] = []
            testunit_formated['textValue'] = testunit['textValue']
            temp_arr = []
            for value in testunit['textValue'].split(','):
                temp_arr.append({
                    'value': value,
                    'display': value
                })
            testunit_formated['textValueArray'] = temp_arr
            return testunit_formated
    
    def map_quantiative_testunit(self, testunit_formated, testunit):
            testunit_formated['useSpec'] = testunit['useSpec']
            testunit_formated['useQuantification'] = testunit['useQuantification']
            testunit_formated['mibiValue'] = ''
            testunit_formated['lowerLimit'] = testunit['lowerLimit']
            testunit_formated['upperLimit'] = testunit['upperLimit']
            testunit_formated['quantificationLowerLimit'] = testunit['quantificationLowerLimit']
            testunit_formated['quantificationUpperLimit'] = testunit['quantificationUpperLimit']
            testunit_formated['concentrations'] = []
            testunit_formated['textValue'] = ''
            return testunit_formated
    
    def map_mibi_testunit(self, testunit_formated, testunit):
            testunit_formated['useSpec'] = False
            testunit_formated['useQuantification'] = False
            testunit_formated['upperLimit'] = ''
            testunit_formated['mibiValue'] = testunit['upperLimit']
            testunit_formated['quantificationUpperLimit'] = ''
            testunit_formated['quantificationLowerLimit'] = ''
            testunit_formated['concentrations'] = testunit['concentrationsNames']
            testunit_formated['textValue'] = ''
            return testunit_formated

    def open_test_unit_edit_page_by_id(self, id):
        url_str = "{}testUnits/edit/" + str(id)
        test_units_url = url_str.format(self.base_selenium.url)
        self.base_selenium.get(url=test_units_url)
