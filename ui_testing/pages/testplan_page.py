from ui_testing.pages.testplans_page import TestPlans


class TstPlan(TestPlans):
    def get_no(self):
        self.base_selenium.wait_until_element_located("test_plan:no")
        return self.base_selenium.get_value(element="test_plan:no")

    def set_no(self, no):
        self.base_selenium.set_text(element="test_plan:no", value=no)

    def get_article(self):
        articles = self.base_selenium.get_text(element="test_plan:article").split(' No')
        article_list = []
        for article in articles:
            if "×" in article:
                article_list.append(article.replace("×", ""))
        return article_list

    def set_article(self, article='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='test_plan:article')
            return self.get_article()
        else:
            self.base_selenium.select_item_from_drop_down(element='test_plan:article', item_text=article)

    def clear_article(self):
        if self.get_article():
            self.base_selenium.clear_items_in_drop_down(element='test_plan:article')

    def clear_material_types(self):
        if self.get_material_type():
            self.base_selenium.clear_items_in_drop_down(element='test_plan:material_type')
            self.sleep_tiny()

    def get_material_type(self):
        return self.base_selenium.get_text(element='test_plan:material_type').split('\n')[0]

    def set_material_type(self, material_type='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='test_plan:material_type')
            return self.get_material_type()
        else:
            self.base_selenium.select_item_from_drop_down(element='test_plan:material_type', item_text=material_type)

    def get_test_plan(self):
        return self.base_selenium.get_text(element='test_plan:test_plan')

    def set_test_plan(self, name='', random=False):
        name = self.generate_random_text() if random else name
        self.base_selenium.set_text_in_drop_down(ng_select_element='test_plan:test_plan', text=name)
        return name

    def search_test_unit_not_set(self, test_unit=''):
        self.info('navigate to testplan second step')
        self.navigate_to_testunits_selection_page()
        self.sleep_tiny()
        self.base_selenium.click('test_plan:add_new_item')
        self.sleep_small()
        is_option_exist = self.base_selenium.select_item_from_drop_down(element='test_plan:test_unit',
                                                                        item_text=test_unit)
        self.base_selenium.click(element='test_plan:cancel_add_testunit')
        self.base_selenium.click(element='test_plan:back_button')
        return is_option_exist

    def set_test_unit(self, test_unit='', **kwargs):
        self.navigate_to_testunits_selection_page()
        self.sleep_tiny()
        self.base_selenium.click('test_plan:add_new_item')
        self.sleep_tiny()
        self.base_selenium.select_item_from_drop_down(element='test_plan:test_unit',
                                                      item_text=test_unit, avoid_duplicate=True)
        if 'upper' in kwargs:
            self.info('set upper : {}'.format(kwargs['upper']))
            elems = self.base_selenium.find_elements('general:col_6')
            upper = self.base_selenium.find_element_in_element(source=elems[4], destination_element='general:input')
            upper.clear()
            upper.send_keys(kwargs['upper'])
        if 'lower' in kwargs:
            self.info('set lower : {}'.format(kwargs['lower']))
            elems = self.base_selenium.find_elements('general:col_6')
            lower = self.base_selenium.find_element_in_element(source=elems[5], destination_element='general:input')
            lower.clear()
            lower.send_keys(kwargs['lower'])
        self.sleep_small()
        self.base_selenium.click('test_plan:check_btn')
        self.sleep_tiny()

    def get_testunit_in_testplan_title_multiple_line_properties(self):
        dom_element = self.base_selenium.find_element(element='test_plan:testunit_title')
        multiple_line_properties = dict()
        multiple_line_properties['textOverflow'] = self.base_selenium.driver.execute_script('return '
                                                                                            'window'
                                                                                            '.getComputedStyle('
                                                                                            'arguments[0], '
                                                                                            '"None").textOverflow',
                                                                                            dom_element)
        multiple_line_properties['lineBreak'] = self.base_selenium.driver.execute_script('return '
                                                                                         'window'
                                                                                         '.getComputedStyle('
                                                                                         'arguments[0], '
                                                                                         '"None").lineBreak',
                                                                                         dom_element)

        return multiple_line_properties

    def get_test_unit_limits(self):
        self.base_selenium.click('test_plan:next')
        elems = self.base_selenium.find_elements('general:col_6')
        upper = self.base_selenium.find_element_in_element(source=elems[4], destination_element='general:input')
        lower = self.base_selenium.find_element_in_element(source=elems[5], destination_element='general:input')
        return upper.get_attribute('value'), lower.get_attribute('value')

    def get_test_unit_category(self):
        self.navigate_to_testunits_selection_page()
        self.sleep_small()
        return self.base_selenium.get_text(element='test_plan:test_unit_category')


    def create_new_test_plan(self, name='', material_type='', article='', test_unit='', save=True, **kwargs):
        self.info('create new test plan')
        self.test_plan_name = name or self.generate_random_text()
        self.material_type = material_type
        self.article = article
        self.click_create_test_plan_button()
        self.sleep_small()
        self.set_test_plan(name=self.test_plan_name)
        if self.material_type:
            self.info('2ith {} material type'.format(material_type))
            self.set_material_type(material_type=self.material_type)
        else:
            self.info('with random material type')
            self.material_type = self.set_material_type(random=True)
        self.sleep_tiny()

        if self.article:
            self.info('with {} article'.format(article))
            self.set_article(article=article)
        else:
            self.article = self.set_article(random=True)
        self.sleep_tiny()

        if test_unit:
            self.info('With {} test unit'.format(test_unit))
            self.set_test_unit(test_unit=test_unit, **kwargs)
            self.sleep_tiny()
            if save:
                self.save(save_btn='test_plan:save_and_complete')

        if save:
            self.save(save_btn='test_plan:save_btn')
            self.wait_until_page_is_loaded()

        self.info('test plan name : {}'.format(self.test_plan_name))
        return self.test_plan_name

    def is_material_type_existing(self, material_type):
        self.set_material_type(material_type)
        return self.base_selenium.check_item_partially_in_items(element='test_plan:material_type',
                                                                item_text=material_type)

    def is_article_existing(self, article):
        self.set_article(article=article)
        return self.base_selenium.check_item_partially_in_items(element='test_plan:article', item_text=article)

    def navigate_to_testunits_selection_page(self):
        self.info('Navigating to testplan create/update step 2')
        self.sleep_tiny()
        self.base_selenium.scroll()
        self.base_selenium.click(element='test_plan:testunits_selection')
        self.sleep_tiny()

    def get_all_testunits_in_testplan(self, navigate_to_test_unit_selection=True):
        # returns all testunits in testplan
        if navigate_to_test_unit_selection:
            self.navigate_to_testunits_selection_page()
        testunits = []
        self.info('Getting the testunits data')
        rows = self.base_selenium.get_table_rows(element='test_plan:testunits_table')
        for row in rows:
            row_data = self.base_selenium.get_row_cells(row)
            row_data_text = []
            for r in row_data:
                row_data_text.append(r.text)
            testunits.append(row_data_text)

        return testunits

    def delete_the_first_testunit_from_the_tableview(self):
        self.info('Deleting the first testunit from the testunits table')
        self.base_selenium.click(element='test_plan:row_delete_button')
        self.sleep_tiny()

    def check_if_deleted_testunit_is_available(self, all_testunits, deleted_test_unit):
        deleted_test_unit_found = 0
        for testunit in all_testunits:
            current_testunit_name = testunit[0]
            if (current_testunit_name == deleted_test_unit):
                deleted_test_unit_found = 1
        return deleted_test_unit_found

    def switch_test_units_to_row_view(self):
        self.info('Switching from card view to table view')
        self.base_selenium.click(element='test_plan:table_card_switcher')

    def save_and_confirm_popup(self):
        self.save(save_btn='test_plan:save_btn', sleep=True)
        # press 'Ok' on the popup
        self.info('Accepting the changes made')
        self.base_selenium.click(element='test_plan:ok')
        self.sleep_small()

    def save_confirm_popup_and_wait(self):
        self.save(save_btn='test_plan:save_btn', sleep=True)
        # press 'Ok' on the popup
        self.info('Accepting the changes made')
        self.base_selenium.click(element='test_plan:ok')
        self.sleep_small()
        self.base_selenium.refresh()
        self.wait_until_page_is_loaded()

    def delete_all_testunits(self):
        rows = self.base_selenium.get_table_rows(element='test_plan:testunits_table')
        for row in rows:
            self.base_selenium.click(element='test_plan:row_delete_button')

    def duplicate_testplan(self, change=[]):
        """
        Changes the fields in the testplan after choosing the duplicate option on
        a specific testplan
        """
        for c in change:
            self.info('Changing the {} field'.format(c))
            if c == 'name':
                duplicated_test_plan_name = self.generate_random_text()
                self.set_test_plan(name=duplicated_test_plan_name)
                self.sleep_tiny()
        self.sleep_small()
        no = self.get_no()
        self.save(save_btn='test_plan:save_btn')
        self.wait_until_page_is_loaded()
        return no

    def get_testunit_category_iterations(self, testplan_name, testunit_name):
        self.get_test_plan_edit_page(testplan_name)
        self.set_test_unit(testunit_name)
        testunit_category = self.base_selenium.get_text(element='test_plan:test_unit_category')
        testunit_iteration = self.base_selenium.get_value(element='test_plan:test_unit_iteration')

        return testunit_category, testunit_iteration

    '''
    Update the testunits field searchable in the database
    '''

    def get_and_update_testunits_dropdown_field(self, cursor, db, searchable):
        testunits_select_query_from_testplans = (
            "SELECT searchable FROM `field_data` WHERE componentId = 5 AND name = 'testUnits'")
        cursor.execute(testunits_select_query_from_testplans)
        old_testunits_searchable_from_testplans = str(cursor.fetchone()[0])

        testunits_searchable_update_query_in_testplans = (
                "UPDATE `field_data` SET `searchable`= '" + searchable + "' WHERE componentId = 5 AND name = 'testUnits'")
        cursor.execute(testunits_searchable_update_query_in_testplans)
        db.commit()

        return old_testunits_searchable_from_testplans

    def update_upper_lower_limits_of_testunit(self, id):
        self.get_test_plan_edit_page_by_id(id)
        self.navigate_to_testunits_selection_page()
        new_upper = self.generate_random_number(lower=50, upper=100)
        new_lower = self.generate_random_number(lower=1, upper=49)
        self.base_selenium.set_text('test_plan:testunit_quantification_upper_limit', str(new_upper))
        self.base_selenium.set_text('test_plan:testunit_quantification_lower_limit', str(new_lower))
        self.sleep_small()
        self.save(save_btn='test_plan:save_btn')
        return new_lower, new_upper

    def get_testunit_quantification_limit(self, testunits, testunit_display_name):
        for testunit in testunits:
            if (testunit_display_name in testunit['Test Unit Name']):
                quantification_limit = testunit['Quantification Limit']
                return quantification_limit
