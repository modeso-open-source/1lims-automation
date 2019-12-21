from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip


class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.contact_page.get_contacts_page()

    def test_06_create_contact_with_person(self):
        contact_data = self.contact_page.create_update_contact()

        self.base_selenium.LOGGER.info('filter by contact no.: {} to get the record'.format(contact_data['no']))
        first_contact_record = self.contact_page.search(value=contact_data['no'])[0]

        self.base_selenium.LOGGER.info('open the record in edit to compare the data')
        self.contact_page.open_edit_page(row=first_contact_record, xpath='//span[@class="mr-auto ng-star-inserted"]/a')

        contact_data_after_create = self.contact_page.get_full_contact_data()
        self.base_selenium.LOGGER.info('contact no is {}, and it should be {}'.format(contact_data_after_create['no'], contact_data['no']) )
        self.assertEqual(contact_data_after_create['no'], contact_data['no'])

        self.base_selenium.LOGGER.info('contact name is {}, and it should be {}'.format(contact_data_after_create['name'], contact_data['name']) )
        self.assertEqual(contact_data_after_create['name'], contact_data['name'])

        self.base_selenium.LOGGER.info('contact address is {}, and it should be {}'.format(contact_data_after_create['address'], contact_data['address']) )
        self.assertEqual(contact_data_after_create['address'], contact_data['address'])

        self.base_selenium.LOGGER.info('contact postalcode is {}, and it should be {}'.format(contact_data_after_create['postalcode'], contact_data['postalcode']) )
        self.assertEqual(contact_data_after_create['postalcode'], contact_data['postalcode'])

        self.base_selenium.LOGGER.info('contact location is {}, and it should be {}'.format(contact_data_after_create['location'], contact_data['location']) )
        self.assertEqual(contact_data_after_create['location'], contact_data['location'])

        self.base_selenium.LOGGER.info('contact country is {}, and it should be {}'.format(contact_data_after_create['country'], contact_data['country']) )
        self.assertEqual(contact_data_after_create['country'], contact_data['country'])

        self.base_selenium.LOGGER.info('contact email is {}, and it should be {}'.format(contact_data_after_create['email'], contact_data['email']) )
        self.assertEqual(contact_data_after_create['email'], contact_data['email'])

        self.base_selenium.LOGGER.info('contact phone is {}, and it should be {}'.format(contact_data_after_create['phone'], contact_data['phone']) )
        self.assertEqual(contact_data_after_create['phone'], contact_data['phone'])

        self.base_selenium.LOGGER.info('contact skype is {}, and it should be {}'.format(contact_data_after_create['skype'], contact_data['skype']) )
        self.assertEqual(contact_data_after_create['skype'], contact_data['skype'])

        self.base_selenium.LOGGER.info('contact website is {}, and it should be {}'.format(contact_data_after_create['website'], contact_data['website']) )
        self.assertEqual(contact_data_after_create['website'], contact_data['website'])        

        self.base_selenium.LOGGER.info('contact departments is {}, and it should be {}'.format(contact_data_after_create['departments'], contact_data['departments']) )
        self.assertEqual(contact_data_after_create['departments'], contact_data['departments'])

        self.base_selenium.LOGGER.info('contact contact_type is {}, and it should be {}'.format(contact_data_after_create['contact_type'], contact_data['contact_type']) )
        self.assertEqual(contact_data_after_create['contact_type'], contact_data['contact_type'])

        self.base_selenium.LOGGER.info('navigate to persons page to compare the data')
        self.contact_page.get_contact_persons_page()

        contact_persons_data_after_create = self.contact_page.get_contact_persons_data()

        person_counter = 0
        for contact_person in contact_persons_data_after_create:
            current_contact_person = contact_data["contact_persons"][person_counter]
            self.base_selenium.LOGGER.info('contact person #{} name is: {}, and it should be: {}'.format(person_counter, contact_person['name'], current_contact_person['name']))
            self.assertEqual(contact_person['name'], current_contact_person['name'])
            self.base_selenium.LOGGER.info('contact person #{} position is: {}, and it should be: {}'.format(person_counter, contact_person['position'], current_contact_person['position']))
            self.assertEqual(contact_person['position'], current_contact_person['position'])
            self.base_selenium.LOGGER.info('contact person #{} email is: {}, and it should be: {}'.format(person_counter, contact_person['email'], current_contact_person['email']))
            self.assertEqual(contact_person['email'], current_contact_person['email'])
            self.base_selenium.LOGGER.info('contact person #{} phone is: {}, and it should be: {}'.format(person_counter, contact_person['phone'], current_contact_person['phone']))
            self.assertEqual(contact_person['phone'], current_contact_person['phone'])
            self.base_selenium.LOGGER.info('contact person #{} skype is: {}, and it should be: {}'.format(person_counter, contact_person['skype'], current_contact_person['skype']))
            self.assertEqual(contact_person['skype'], current_contact_person['skype'])
            self.base_selenium.LOGGER.info('contact person #{} info is: {}, and it should be: {}'.format(person_counter, contact_person['info'], current_contact_person['info']))
            self.assertEqual(contact_person['info'], current_contact_person['info'])
            person_counter = person_counter +1

    def test_07_create_contact_person_from_edit_update_old_value(self):
        """
        Contact: Edit Approach: make sure that you can add contact person from the edit mode 
        LIMS-6388
        """

        self.base_selenium.LOGGER.info('open random contact record to add a new contact persons to it')
        first_contact_record = self.contact_page.get_random_contact_row()
        self.contact_page.open_edit_page(row=first_contact_record)

        self.base_selenium.LOGGER.info('acquire contact data to compare it after updating the persons')
        contact_data = self.contact_page.get_full_contact_data()

        self.base_selenium.LOGGER.info('Open contact persons page')
        self.contact_page.get_contact_persons_page()
        self.base_selenium.LOGGER.info('add new record to contact persons')
        contact_persons_after_update = self.contact_page.create_update_contact_person(save=True)

        self.base_selenium.LOGGER.info('Refresh to compare the data before and after refresh')
        self.base_selenium.refresh()

        contact_data_after_refresh = self.contact_page.get_full_contact_data()
        self.base_selenium.LOGGER.info('Compare contact data after refresh')

        self.base_selenium.LOGGER.info('contact no is {}, and it should be {}'.format(contact_data_after_refresh['no'], contact_data['no']) )
        self.assertEqual(contact_data_after_refresh['no'], contact_data['no'])

        self.base_selenium.LOGGER.info('contact name is {}, and it should be {}'.format(contact_data_after_refresh['name'], contact_data['name']) )
        self.assertEqual(contact_data_after_refresh['name'], contact_data['name'])

        self.base_selenium.LOGGER.info('contact address is {}, and it should be {}'.format(contact_data_after_refresh['address'], contact_data['address']) )
        self.assertEqual(contact_data_after_refresh['address'], contact_data['address'])

        self.base_selenium.LOGGER.info('contact postalcode is {}, and it should be {}'.format(contact_data_after_refresh['postalcode'], contact_data['postalcode']) )
        self.assertEqual(contact_data_after_refresh['postalcode'], contact_data['postalcode'])

        self.base_selenium.LOGGER.info('contact location is {}, and it should be {}'.format(contact_data_after_refresh['location'], contact_data['location']) )
        self.assertEqual(contact_data_after_refresh['location'], contact_data['location'])

        self.base_selenium.LOGGER.info('contact country is {}, and it should be {}'.format(contact_data_after_refresh['country'], contact_data['country']) )
        self.assertEqual(contact_data_after_refresh['country'], contact_data['country'])

        self.base_selenium.LOGGER.info('contact email is {}, and it should be {}'.format(contact_data_after_refresh['email'], contact_data['email']) )
        self.assertEqual(contact_data_after_refresh['email'], contact_data['email'])

        self.base_selenium.LOGGER.info('contact phone is {}, and it should be {}'.format(contact_data_after_refresh['phone'], contact_data['phone']) )
        self.assertEqual(contact_data_after_refresh['phone'], contact_data['phone'])

        self.base_selenium.LOGGER.info('contact skype is {}, and it should be {}'.format(contact_data_after_refresh['skype'], contact_data['skype']) )
        self.assertEqual(contact_data_after_refresh['skype'], contact_data['skype'])

        self.base_selenium.LOGGER.info('contact website is {}, and it should be {}'.format(contact_data_after_refresh['website'], contact_data['website']) )
        self.assertEqual(contact_data_after_refresh['website'], contact_data['website'])        

        self.base_selenium.LOGGER.info('contact departments is {}, and it should be {}'.format(contact_data_after_refresh['departments'], contact_data['departments']) )
        self.assertEqual(contact_data_after_refresh['departments'], contact_data['departments'])

        self.base_selenium.LOGGER.info('contact contact_type is {}, and it should be {}'.format(contact_data_after_refresh['contact_type'], contact_data['contact_type']) )
        self.assertEqual(contact_data_after_refresh['contact_type'], contact_data['contact_type'])

        self.contact_page.get_contact_persons_page()
        contact_persons_after_refresh = self.contact_page.get_contact_persons_data()

        self.base_selenium.LOGGER.info('compare contact persons data after refresh')

        person_counter = 0
        for contact_person in contact_persons_after_refresh:
            current_contact_person = contact_persons_after_update[person_counter]
            self.base_selenium.LOGGER.info('contact person #{} name is: {}, and it should be: {}'.format(person_counter, contact_person['name'], current_contact_person['name']))
            self.assertEqual(contact_person['name'], current_contact_person['name'])
            self.base_selenium.LOGGER.info('contact person #{} position is: {}, and it should be: {}'.format(person_counter, contact_person['position'], current_contact_person['position']))
            self.assertEqual(contact_person['position'], current_contact_person['position'])
            self.base_selenium.LOGGER.info('contact person #{} email is: {}, and it should be: {}'.format(person_counter, contact_person['email'], current_contact_person['email']))
            self.assertEqual(contact_person['email'], current_contact_person['email'])
            self.base_selenium.LOGGER.info('contact person #{} phone is: {}, and it should be: {}'.format(person_counter, contact_person['phone'], current_contact_person['phone']))
            self.assertEqual(contact_person['phone'], current_contact_person['phone'])
            self.base_selenium.LOGGER.info('contact person #{} skype is: {}, and it should be: {}'.format(person_counter, contact_person['skype'], current_contact_person['skype']))
            self.assertEqual(contact_person['skype'], current_contact_person['skype'])
            self.base_selenium.LOGGER.info('contact person #{} info is: {}, and it should be: {}'.format(person_counter, contact_person['info'], current_contact_person['info']))
            self.assertEqual(contact_person['info'], current_contact_person['info'])
            person_counter = person_counter +1