from ui_testing.pages.contacts_page import Contacts
from random import randint
import time


class Contact(Contacts):

    def set_contact_name(self, name=''):
        # case contact name was not provided, it generates random text to be the contact name
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if name == '':
            name = self.generate_random_text()
        
        self.base_selenium.set_text(element="contact:name", value=name)
        
        return name

    def set_contact_number(self, no=''):
        # case contact no was not provided, it generates random text to be the contact no
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        # random text function is used in case of number because of a requirement from the client that it should support text
        if no == '':
            no = self.generate_random_text()

        self.base_selenium.set_text(element="contact:no", value=no)
        
        return no

    def set_contact_address(self, address=''):
        # case contact address was not provided, it generates random text to be the contact address
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if address == '':
            address = self.generate_random_text()

        self.base_selenium.set_text(element="contact:address", value=address)
        
        return address

    def set_contact_postalcode(self, postalcode=''):
        # case contact postalcode was not provided, it generates random text to be the contact postalcode
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if postalcode == '':
            postalcode = self.generate_random_text()

        self.base_selenium.set_text(element="contact:postalcode", value=postalcode)
        
        return postalcode

    def set_contact_location(self, location=''):
        # case contact location was not provided, it generates random text to be the contact location
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if location == '':
            location = self.generate_random_text()

        self.base_selenium.set_text(element="contact:location", value=location)
        
        return location

    def set_contact_country(self, country=''):
        if country == '':
            self.base_selenium.select_item_from_drop_down(element='contact:country')
        else:
            self.base_selenium.select_item_from_drop_down(element='contact:country', item_text=country)
        return self.get_contact_country()

    def set_contact_email(self, email=''):
        # case contact email was not provided, it generates random text to be the contact email
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if email == '':
            email = self.generate_random_email()

        self.base_selenium.set_text(element="contact:email", value=email)
        
        return email

    def set_contact_phone(self, phone=''):
        # case contact phone was not provided, it generates random text to be the contact phone
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if phone == '':
            phone = self.generate_random_text()

        self.base_selenium.set_text(element="contact:phone", value=phone)
        
        return phone

    def set_contact_skype(self, skype=''):
        # case contact skype was not provided, it generates random text to be the contact skype
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if skype == '':
            skype = self.generate_random_text()

        self.base_selenium.set_text(element="contact:skype", value=skype)
        
        return skype

    def set_contact_website(self, website=''):
        # case contact website was not provided, it generates random text to be the contact website
        # returns the value of the name in case i generated a random text, so i have the value to be used later
        if website == '':
            website = self.generate_random_website()

        self.base_selenium.set_text(element="contact:website", value=website)
        
        return website

    # to be fixed
    def set_contact_departments(self, departments=[]):
        
        return departments
    # to be fixed
    def set_contact_type(self, contacttype=''):
        
        return contacttype

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
        return []
    
    # to be fixed
    def get_contact_type(self):
        return []