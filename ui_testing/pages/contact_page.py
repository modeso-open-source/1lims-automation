from ui_testing.pages.contacts_page import Contacts
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ui_testing.countries import countries


class Contact(Contacts):
    def set_contact_name(self, name=''):
        # case contact name was not provided, it generates random text to be the contact name
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        name = name or self.generate_random_text()
        self.info('set contact name to be {}', name)
        self.base_selenium.set_text(element="contact:name", value=name)
        return name

    def set_contact_number(self, no=''):
        # case contact no was not provided, it generates random text to be the contact no
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        # random text function is used in case of number because of a requirement from the client that it should support text
        no = no or self.generate_random_text()
        self.info('set contact no to be {}', no)
        self.base_selenium.set_text(element="contact:no", value=no)
        
        return no

    def set_contact_address(self, address=''):
        # case contact address was not provided, it generates random text to be the contact address
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        address = address or self.generate_random_text()

        self.info('set contact address to be {}', address)
        self.base_selenium.set_text(element="contact:address", value=address)
        
        return address

    def set_contact_postalcode(self, postalcode=''):
        # case contact postalcode was not provided, it generates random text to be the contact postalcode
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        postalcode = postalcode or  self.generate_random_text()

        self.info('set contact postalcode to be {}', postalcode)
        self.base_selenium.set_text(element="contact:postalcode", value=postalcode)
        
        return postalcode

    def set_contact_location(self, location=''):
        # case contact location was not provided, it generates random text to be the contact location
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        location = location or self.generate_random_text()

        self.info('set contact location to be {}', location)
        self.base_selenium.set_text(element="contact:location", value=location)
        
        return location

    def set_contact_country(self, country=''):
        if country == '':
            self.base_selenium.select_item_from_drop_down(element='contact:country')
        else:
            self.base_selenium.select_item_from_drop_down(element='contact:country', item_text=country)
        
        contact_country = self.get_contact_country()
        self.info('set contact country to be {}', contact_country)
        return contact_country

    def set_contact_email(self, email=''):
        # case contact email was not provided, it generates random text to be the contact email
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        email = email or self.generate_random_email()

        self.info('set contact email to be {}', email)
        self.base_selenium.set_text(element="contact:email", value=email)
        
        return email

    def set_contact_phone(self, phone=''):
        # case contact phone was not provided, it generates random text to be the contact phone
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        phone = phone or self.generate_random_text()

        self.info('set contact phone to be {}', phone)
        self.base_selenium.set_text(element="contact:phone", value=phone)
        
        return phone

    def set_contact_skype(self, skype=''):
        # case contact skype was not provided, it generates random text to be the contact skype
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        skype = skype or self.generate_random_text()

        self.info('set contact skype to be {}', skype)
        self.base_selenium.set_text(element="contact:skype", value=skype)
        
        return skype

    def set_contact_website(self, website=''):
        # case contact website was not provided, it generates random text to be the contact website
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        website = website or self.generate_random_website()

        self.info('set contact website to be {}', website)
        self.base_selenium.set_text(element="contact:website", value=website)
        
        return website

    def set_contact_departments(self, departments=[]):
        counter = 0
        department_list = []
        for department in departments:
            value = department or self.generate_random_text()
            department_list.append(value)
            departments_field = self.base_selenium.find_element_in_element(destination_element='general:input',
                                                                        source_element='contact:departments')
            departments_field.send_keys(value)
            departments[counter] = value
            counter = counter +1
            departments_field.send_keys(Keys.ENTER)

        self.info('set contact departments to be {}', departments)
        return self.get_contact_departments()

    def set_contact_type(self, contact_types=['isSupplier']):
        for contact_type in contact_types :
            self.base_selenium.click(element='contact:contacttype-'+contact_type)

        self.info('set contact type to be {}', contact_types)
        return self.get_contact_type()

    def get_contact_number(self):
        return self.base_selenium.get_value(element="contact:no")

    def get_contact_name(self):
        return self.base_selenium.get_value(element="contact:name")
    
    def get_contact_address(self):
        return self.base_selenium.get_value(element="contact:address")
    
    def get_contact_postalcode(self):
        return self.base_selenium.get_value(element="contact:postalcode")
    
    def get_contact_location(self):
        return self.base_selenium.get_value(element="contact:location")

    def get_contact_country(self):
        return self.base_selenium.get_text(element='contact:country').split('\n')[0]

    def get_contact_email(self):
        return self.base_selenium.get_value(element="contact:email")
    
    def get_contact_skype(self):
        return self.base_selenium.get_value(element="contact:skype")
    
    def get_contact_phone(self):
        return self.base_selenium.get_value(element="contact:phone")
    
    def get_contact_website(self):
        return self.base_selenium.get_value(element="contact:website")

    def get_departments_tags(self):
        return self.base_selenium.find_elements(element='contact:departments_tag')

    def get_department_tag(self, departments_tags=[], counter=0):
        return departments_tags[counter].find_element_by_xpath("//div[@class='tag__text inline' and @title='"+departments_tags[counter].text+"']")

    def get_contact_departments(self):
        departments_tags = self.get_departments_tags()
        departments = []
        counter = 0
        for tag in departments_tags:
            temp_department = self.get_department_tag(departments_tags=departments_tags, counter=counter)
            departments.append(temp_department.text)
            counter = counter +1
        if counter > 0 :
            return ', '.join(departments)
        else:
            return '-'
    
    def get_contact_type(self):
        isClient = self.base_selenium.find_element(element="contact:is_client_checkbox").is_selected()
        isSupplier = self.base_selenium.find_element(element="contact:is_supplier_checkbox").is_selected()
        isLaboratory = self.base_selenium.find_element(element="contact:is_laboratory_checkbox").is_selected()

        contact_types = [3]
        counter = 0
        no_type = True
        if isSupplier:
            contact_types[counter] = 'Contact'
            counter = counter +1
            no_type = False
        if isClient:
            contact_types[counter] = 'Client'
            counter = counter +1
            no_type = False
        if isLaboratory:
            contact_types[counter] = 'Laboratory'
            counter = counter +1
            no_type = False
            
        if no_type:
            return  '-'
        else:
            return ', '.join(contact_types)

    def create_update_contact(self, create=True, no='', name='', address='',
                              postalcode='', location='', country='', email='',
                              phone='', skype='', website='', contact_types=['isClient'],
                              departments=[''], contact_persons=True, save=True):

        if create:
            self.info('Create new contact.')
            self.base_selenium.click(element='contacts:new_contact')
            self.info('Wait until data are loaded')
            self.sleep_small()

        # get the data from the return type
        contact_no = self.set_contact_number(no=no)
        contact_name = self.set_contact_name(name=name)
        contact_address = self.set_contact_address(address=address)
        contact_postalcode = self.set_contact_postalcode(postalcode=postalcode)
        contact_location = self.set_contact_location(location=location)
        contact_country = self.set_contact_country(country=country)
        contact_email = self.set_contact_email(email=email)
        contact_phone = self.set_contact_phone(phone=phone)
        contact_skype = self.set_contact_skype(skype=skype)
        contact_website = self.set_contact_website(website=website)
        self.set_contact_type(contact_types=contact_types)
        contact_departments = self.set_contact_departments(departments=departments)

        self.info('wait to make sure that all data are written correctly')
        self.sleep_tiny()
        
        self.info('acquiring contact data')
        contact_data = {
            "Contact No": contact_no,
            "Contact Name": contact_name,
            "Address": contact_address,
            "Postal Code": contact_postalcode,
            "Location": contact_location,
            "Country": contact_country,
            "Email": contact_email,
            "Phone": contact_phone,
            "Skype": contact_skype,
            "Website": contact_website,
            "Departments": contact_departments,
            "Type": self.get_contact_type()
            }

        if contact_persons:
            self.get_contact_persons_page()
            contact_person_data = self.create_update_contact_person()
            contact_data['contact_persons'] = contact_person_data
        else:
            contact_data['contact_persons'] = []

        self.info('Saving the contact created')
        if save:
            self.save(save_btn='contact:save')
        return contact_data

    def get_full_contact_data(self):
        self.info('Collecting contact data')
        return {
            "Contact No": self.get_contact_number(),
            "Contact Name": self.get_contact_name(),
            "Address": self.get_contact_address(),
            "Postal Code": self.get_contact_postalcode(),
            "Location": self.get_contact_location(),
            "Country": self.get_contact_country(),
            "Email": self.get_contact_email(),
            "Phone": self.get_contact_phone(),
            "Skype": self.get_contact_skype(),
            "Website": self.get_contact_website(),
            "Departments": self.get_contact_departments(),
            "Type": self.get_contact_type()
        }

    def get_contact_persons_page(self):
        self.info('switch to persons page')
        self.base_selenium.scroll()
        self.base_selenium.click(element='contact:contact_persons')
        self.wait_until_page_is_loaded()
        self.sleep_tiny()

    def create_update_contact_person(self, create=True, indexToEdit=-1, name='', position='',
                                     email='', phone='', skype='', info='', title='',save=False):
        if create:
            self.base_selenium.click(element='contact:add_another_item')

        contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')

        if not create or indexToEdit == -1:
            indexToEdit = len(contact_persons_table_records)-1
            contact_persons_table_records[indexToEdit].click()
            self.sleep_small()
            contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')

        row_cells_elements = self.base_selenium.get_row_cells_elements_related_to_header(
            row=contact_persons_table_records[indexToEdit], table_element='contact:contact_persons_table')

        self.info(' Set contact person title : {}'.format(title))
        self.base_selenium.update_item_value(item=row_cells_elements['Title:'], item_text=title)

        name = name or self.generate_random_text()
        
        self.info(' Set contact person name : {}'.format(name))
        self.base_selenium.update_item_value(item=row_cells_elements['Contact Person: *'], item_text=name)
        
        position = position or self.generate_random_text()
        
        self.info(' Set contact person position : {}'.format(position))
        self.base_selenium.update_item_value(item=row_cells_elements['Position:'], item_text=position)
        
        email = email or self.generate_random_email()
        
        self.info(' Set contact person email : {}'.format(email))
        self.base_selenium.update_item_value(item=row_cells_elements['Email:'], item_text=email)
        
        phone = phone or self.generate_random_text()
        
        self.info(' Set contact person phone : {}'.format(phone))
        self.base_selenium.update_item_value(item=row_cells_elements['Phone:'], item_text=phone)
        
        skype = skype or self.generate_random_text()
        
        self.info(' Set contact person skype : {}'.format(skype))
        self.base_selenium.update_item_value(item=row_cells_elements['Skype:'], item_text=skype)
        
        info = info or self.generate_random_text()
        
        self.info(' Set contact person info : {}'.format(info))
        self.base_selenium.update_item_value(item=row_cells_elements['Info:'], item_text=info)

        self.info('Acquire contact persons data')
        contact_person_data = self.get_contact_persons_data(navigate_to_person_page=False)
        
        if save:
            self.save(save_btn='contact:save')

        return contact_person_data
        
    def get_contact_persons_data(self, navigate_to_person_page=True):
        if navigate_to_person_page:
            self.get_contact_persons_page()
        contact_persons_arr = []
        webdriver.ActionChains(self.base_selenium.driver).send_keys(Keys.ESCAPE).perform()
        self.info('collecting persons data')
        contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')
        self.sleep_medium()
        if contact_persons_table_records[0].text == 'No Results Found':
            self.info("contact persons table is empty")
            return contact_persons_arr
        if len(contact_persons_table_records) >= 1:
            for person in contact_persons_table_records:
                row_data = self.base_selenium.get_row_cells_elements_related_to_header(
                    row=person, table_element='contact:contact_persons_table')
                contact_persons_arr.append({
                    'title': row_data['Title:'].text,
                    'name': row_data['Contact Person: *'].text,
                    'position': row_data['Position:'].text,
                    'email': row_data['Email:'].text,
                    'phone': row_data['Phone:'].text,
                    'skype': row_data['Skype:'].text,
                    'info': row_data['Info:'].text
                })
        else:
            self.info("contact persons table is empty")
        return contact_persons_arr

    def get_contact_persons_count(self):
        contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')
        return len(contact_persons_table_records)
    
    def delete_contact_person(self, index=0, save=False):
        contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')
        if index < len(contact_persons_table_records):
            delete_button = contact_persons_table_records[index].find_element('contact:row_delete_button')
            if delete_button:
                delete_button.click()

        else:
            delete_button = contact_persons_table_records[0].find_element('contact:delete_person_button')
            if delete_button:
                delete_button.click()

        if save:
            self.save(save_btn='contact:save')

    def delete_contact_persons(self, save=True):
        rows = self.base_selenium.get_table_rows(element='contact:contact_persons_table')
        for row in rows:
            self.base_selenium.click(element='contact:row_delete_button')

        if save:
            self.save(save_btn='contact:save')

    def check_contact_persons_table_is_empty(self):
        contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')
        if contact_persons_table_records[0].text == 'No Results Found':
            return True
        else:
            return False

    def compare_contact_main_data(self, data_before_save, data_after_save):
        self.info('Comparing contact main data')
        for key in data_before_save:
            if key != 'contact_persons':
                if key not in data_after_save:
                    return False
                self.info('contact {} is {}, and it should be {}'.format(key, data_after_save[key], data_before_save[key]) )        
                if data_before_save[key] != data_after_save[key]:
                        return False
        return True

    def compare_contact_persons_data(self, data_before_save, data_after_save):
        self.info('compare contact persons data after refresh')
        person_counter = 0
        for contact_person in data_after_save:
            current_contact_person = data_before_save[person_counter]
            for key in current_contact_person:
                if key not in contact_person:
                    return False
                self.info('contact person #{} {} is: {}, and it should be: {}'.format(person_counter, key, contact_person[key], current_contact_person[key]) )        
                if current_contact_person[key] != contact_person[key]:
                        return False
            person_counter = person_counter +1

        return True

    def update_department_list(self, departments=[]):
        self.info('updating departments list')
        departments_tags = self.get_departments_tags()
        counter=0
        actions = webdriver.ActionChains(self.base_selenium.driver)
        for department in departments:
            if counter < len(departments_tags):
                # needs to be done through xpath as it is generated dynamically during runtime
                temp_department = self.get_department_tag(departments_tags=departments_tags, counter=counter)
                actions.double_click(temp_department).perform()
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
                actions.send_keys(department).perform()
                webdriver.ActionChains(self.base_selenium.driver).send_keys(Keys.ENTER).perform()
                self.sleep_tiny()
                counter = counter+1
            else:
                self.set_contact_departments(departments=[department])
        
        self.sleep_tiny()
        self.save(save_btn='contact:save')
        return self.get_contact_departments()

    def get_country_data(self, id):
        return list(filter(lambda x: x['id'] == id, countries))[0]

    def get_contact_persons_data_ids(self):
        self.get_contact_persons_page()
        contact_persons_arr = []
        webdriver.ActionChains(self.base_selenium.driver).send_keys(Keys.ESCAPE).perform()
        self.info('Collecting persons data')
        contact_persons_table_records = self.base_selenium.get_table_rows(element='contact:contact_persons_table')
        if self.check_contact_persons_table_is_empty() != True:
            for person in contact_persons_table_records:
                row_data = self.base_selenium.get_row_cells_id_dict_related_to_header(
                    row=person, table_element='contact:contact_persons_table')
                contact_persons_arr.append({
                    'title': row_data['gender'],
                    'name': row_data['name'],
                    'position': row_data['position'],
                    'email': row_data['email'],
                    'phone': row_data['phone'],
                    'skype': row_data['skype'],
                    'info': row_data['moreInfo']
                })

        return contact_persons_arr

    def navigate_to_contact_person_tab_get_data(self):
        self.get_contact_persons_page()
        self.sleep_small()
        contact_person_data_first_contact = self.get_contact_persons_data_ids()[0]
        return contact_person_data_first_contact
