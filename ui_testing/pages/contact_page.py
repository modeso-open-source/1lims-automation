from ui_testing.pages.contacts_page import Contacts
from random import randint
from selenium.webdriver.common.keys import Keys
import time


class Contact(Contacts):

    def set_contact_name(self, name=''):
        # case contact name was not provided, it generates random text to be the contact name
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if name == '':
            name = self.generate_random_text()
        
        self.base_selenium.LOGGER.info('set contact name to be {}', name)
        self.base_selenium.set_text(element="contact:name", value=name)
        
        return name

    def set_contact_number(self, no=''):
        # case contact no was not provided, it generates random text to be the contact no
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        # random text function is used in case of number because of a requirement from the client that it should support text
        if no == '':
            no = self.generate_random_text()

        self.base_selenium.LOGGER.info('set contact no to be {}', no)
        self.base_selenium.set_text(element="contact:no", value=no)
        
        return no

    def set_contact_address(self, address=''):
        # case contact address was not provided, it generates random text to be the contact address
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if address == '':
            address = self.generate_random_text()

        self.base_selenium.LOGGER.info('set contact address to be {}', address)
        self.base_selenium.set_text(element="contact:address", value=address)
        
        return address

    def set_contact_postalcode(self, postalcode=''):
        # case contact postalcode was not provided, it generates random text to be the contact postalcode
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if postalcode == '':
            postalcode = self.generate_random_text()

        self.base_selenium.LOGGER.info('set contact postalcode to be {}', postalcode)
        self.base_selenium.set_text(element="contact:postalcode", value=postalcode)
        
        return postalcode

    def set_contact_location(self, location=''):
        # case contact location was not provided, it generates random text to be the contact location
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if location == '':
            location = self.generate_random_text()

        self.base_selenium.LOGGER.info('set contact location to be {}', location)
        self.base_selenium.set_text(element="contact:location", value=location)
        
        return location

    def set_contact_country(self, country=''):
        if country == '':
            self.base_selenium.select_item_from_drop_down(element='contact:country')
        else:
            self.base_selenium.select_item_from_drop_down(element='contact:country', item_text=country)
        
        contact_country = self.get_contact_country()
        self.base_selenium.LOGGER.info('set contact country to be {}', contact_country)
        return contact_country

    def set_contact_email(self, email=''):
        # case contact email was not provided, it generates random text to be the contact email
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if email == '':
            email = self.generate_random_email()

        self.base_selenium.LOGGER.info('set contact email to be {}', email)
        self.base_selenium.set_text(element="contact:email", value=email)
        
        return email

    def set_contact_phone(self, phone=''):
        # case contact phone was not provided, it generates random text to be the contact phone
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if phone == '':
            phone = self.generate_random_text()

        self.base_selenium.LOGGER.info('set contact phone to be {}', phone)
        self.base_selenium.set_text(element="contact:phone", value=phone)
        
        return phone

    def set_contact_skype(self, skype=''):
        # case contact skype was not provided, it generates random text to be the contact skype
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if skype == '':
            skype = self.generate_random_text()

        self.base_selenium.LOGGER.info('set contact skype to be {}', skype)
        self.base_selenium.set_text(element="contact:skype", value=skype)
        
        return skype

    def set_contact_website(self, website=''):
        # case contact website was not provided, it generates random text to be the contact website
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if website == '':
            website = self.generate_random_website()

        self.base_selenium.LOGGER.info('set contact website to be {}', website)
        self.base_selenium.set_text(element="contact:website", value=website)
        
        return website

    def set_contact_departments(self, departments=[]):
        counter = 0
        for department in departments:
            value = department or self.generate_random_text()
            departments_field = self.base_selenium.find_element_in_element(destination_element='general:input',
                                                                        source_element='contact:departments')
            departments_field.send_keys(value)
            departments[counter] = value
            counter = counter +1
            departments_field.send_keys(Keys.ENTER)

        self.base_selenium.LOGGER.info('set contact departments to be {}', departments)
        return departments

    def set_contact_type(self, contact_types=['isSupplier']):
        for contact_type in contact_types :
            self.base_selenium.click(element='contact:contacttype-'+contact_type)

        self.base_selenium.LOGGER.info('set contact type to be {}', contact_types)
        return contact_types

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

    # to be fixed
    def get_contact_departments(self):
        departments_tags = self.base_selenium.find_element_by_xpath("//div[@class='ng2-tags-container']").find_elements_by_tag_name('tag')
        departments = []
        counter = 0
        for tag in departments_tags:
            departments.append(tag.find_element_by_xpath("//div[@class='tag__text inline']").text)
            counter = counter +1
        if counter > 0 :
            return ', '.join(departments)
        else:
            return '-'
    
    def get_contact_type(self):
        isClient = self.base_selenium.find_element_by_xpath(xpath="//label[@id='isClient']//input[@type='checkbox']").is_selected()
        isSupplier = self.base_selenium.find_element_by_xpath(xpath="//label[@id='isSupplier']//input[@type='checkbox']").is_selected()
        isLaboratory = self.base_selenium.find_element_by_xpath(xpath="//label[@id='isLaboratory']//input[@type='checkbox']").is_selected()

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

    def create_update_contact(self, create=True, no='', name='', address='', postalcode='', location='', country='', email='', phone='', skype='', website='', contact_types=['isClient'], departments=['']):

        if create:
            self.base_selenium.LOGGER.info(' + Create new contact.')
            self.base_selenium.click(element='contacts:new_contact')

            self.base_selenium.LOGGER.info('Wait untill data are loaded')
            self.sleep_tiny()

        self.set_contact_number(no=no)
        self.set_contact_name(name=name)
        self.set_contact_address(address=address)
        self.set_contact_postalcode(postalcode=postalcode)
        self.set_contact_location(location=location)
        self.set_contact_country(country=country)
        self.set_contact_email(email=email)
        self.set_contact_phone(phone=phone)
        self.set_contact_skype(skype=skype)
        self.set_contact_website(website=website)
        self.set_contact_type(contact_types=contact_types)
        contact_departments = self.set_contact_departments(departments=departments)

        self.base_selenium.LOGGER.info('wait to make sure that all data are writtent correctly')
        self.sleep_tiny()
        
        self.base_selenium.LOGGER.info('acquiring contact data')
        contact_data = {
            "no": self.get_contact_number(),
            "name": self.get_contact_name(),
            "address": self.get_contact_address(),
            "postalcode": self.get_contact_postalcode(),
            "location": self.get_contact_location(),
            "country": self.get_contact_country(),
            "email": self.get_contact_email(),
            "phone": self.get_contact_phone(),
            "skype": self.get_contact_skype(),
            "website": self.get_contact_website(),
            "departments": self.get_contact_departments(),
            "contact_type": self.get_contact_type()
        }

        self.base_selenium.LOGGER.info('Saving the contact created')
        self.save(save_btn='contact:save')
        return contact_data

    def get_full_contact_data(self):
        return {
            "no": self.get_contact_number(),
            "name": self.get_contact_name(),
            "address": self.get_contact_address(),
            "postalcode": self.get_contact_postalcode(),
            "location": self.get_contact_location(),
            "country": self.get_contact_country(),
            "email": self.get_contact_email(),
            "phone": self.get_contact_phone(),
            "skype": self.get_contact_skype(),
            "website": self.get_contact_website(),
            "departments": self.get_contact_departments(),
            "contact_type": self.get_contact_type()
        }
