from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory
import json, os, random


class ContactsAPIFactory(BaseAPI):
    @api_factory('get')
    def get_all_contacts(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['contacts_api']['list_all_contacts'])
        _payload = {"sort_value": "companyNo",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        return api, _payload

    @api_factory('get')
    def get_table_fields(self, component_id):
        api = '{}{}{}/'.format(self.url, self.END_POINTS['contacts_api']['get_table_fields'], component_id)
        return api, {}

    @api_factory('get')
    def get_contact_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['form_data'], str(id))
        return api, {}

    @api_factory('put')
    def archive_contacts(self, ids=['1']):
        """
        if success, response['message'] == 'delete_success'
        :param ids:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['archive_contacts'], ','.join(ids))
        return api, {}

    @api_factory('put')
    def restore_contacts(self, ids=['1']):
        """
        if success, response['message']=='restore_success'
        :param ids:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['restore_contacts'], ','.join(ids))
        return api, {}

    @api_factory('delete')
    def delete_archived_contact(self, id=1):
        """
        if success, response['message']=='hard_delete_success'
        :param id:
        :return:
        """
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['delete_contact'], str(id))
        return api, {}

    @api_factory('post')
    def create_contact(self, **kwargs):
        """
        minimum require parameters:
            Param: companyNo: denoted company no
            Param: name: denotes contact name
        Param: departments: array denotes the contact's departments and each element consist of
        {
            "display": department displayed name,
            "value": department saved value,
            "id": in case of update put department id, in case of create put 'new',
            "text": text of the department display,
        }
        Param: address: denotes contact address
        Param: postalCode: denotes contact postal code
        Param: location: denotes contact location
        Param: selectedCountry: denotes contact selected country and it is object
        {
            "id": country id,
            "text": country displayed text,
            "code": country code
        }
        Param: email: denotes contact email
        Param: phone: denotes contact phone
        Param: skype: denotes contact skype
        Param: website: denotes contact website
        Param: isLaboratory: True/False
        Param: isSupplier: True/False
        Param: isClient: True/False
        Param: country: text of the selected country

        contact persons parameters
        Param: persons: array and each element consist of the following
            Param: "name": contact person name
            Param: "position": contact person position
            Param: "email": contact person email
            Param: "phone": contact person phone
            Param: "skype": contact person skype
            Param: "moreInfo": contact person information field
        """
        random_contact_departments = self.generate_random_string()
        _payload = {
            "departments": [
                {
                    "display": random_contact_departments,
                    "value": random_contact_departments,
                    "id": "new",
                    "text": random_contact_departments
                }
            ],
            "departmentArray": [],
            "persons": [],
            "email": {"text": "", "recipient": 0},
            "companyNo": self.generate_random_number(),
            "name": self.generate_random_string(),
            "isSupplier": "true",
            "country": "",
            "dynamicFieldsValues": []
        }
        payload = self.update_payload(_payload, **kwargs)
        api = '{}{}'.format(self.url, self.END_POINTS['contacts_api']['create_contact'])
        return api, payload


class ContactsAPI(ContactsAPIFactory):
    def get_all_contacts_json(self, **kwargs):
        response, _ = self.get_all_contacts(**kwargs)
        return response['contacts']

    def get_first_record_with_data_in_attribute(self, attribute):
        contacts_request, _ = self.get_all_contacts()
        if (contacts_request['status'] != 1) or (contacts_request['count'] == 0):
            return ''
        contacts_records = contacts_request['contacts']
        for contact in contacts_records:
            if contact[attribute]:
                return contact[attribute]

    def delete_active_contact(self, id=1):
        if self.archive_contacts(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_contact(id=id)[0]['message'] == 'hard_delete_success':
                return True
            else:
                self.restore_contacts(ids=[str(id)])
                return False
        else:
            return False

    def get_contacts_with_department(self):
        api, contacts_data = self.get_all_contacts()
        contacts = api['contacts']
        contacts_with_department = [contact for contact in contacts if contact['departments']]
        return contacts_with_department

    def get_departments_in_contact(self, contact_name):
        _filter = '{{"quickSearch":"{}","columns":["companyName","departments","skype","number",' \
                  '"email","postalCode","modifiedBy","website","createdAt","address","country",' \
                  '"modifiedAt","type","phone","location"]}}'.format(contact_name)

        api, contacts_data = self.get_all_contacts(filter=_filter)
        if api['status'] == 1 and api['count'] == 1:
            return api['contacts'][0]['departments'].split(', ')
        elif api['status'] == 1 and api['count'] > 1:
            for contact in api['contacts']:
                if contact['name'] == contact_name:
                    return contact['departments'].split(', ')

    def get_department_contact_list(self, contact_list=[]):
        selected_contacts = sorted(contact_list, key=str.lower)
        departments_list_with_contacts = []
        for contact in selected_contacts:
            departments = self.get_departments_in_contact(contact)
            if departments and departments != ['']:
                contact_dict = {'contact': contact,
                                'departments': departments}
                departments_list_with_contacts.append(contact_dict)
        return departments_list_with_contacts

    def get_department_and_contact_lists(self, no_of_contacts=3):
        contact_list = random.sample(self.get_contacts_with_department(), k=no_of_contacts)
        contact_names_list = [contact['name'] for contact in contact_list]
        departments_list_with_contacts = self.get_department_contact_list(contact_names_list)
        return contact_names_list, departments_list_with_contacts

    def create_contact_with_person(self, gender='Mr.'):
        person_name = self.generate_random_string()
        person = {'gender': {'id': 0, 'text': "Mr."}, "name": person_name, "position": 0,
                  "email": {"text": "", "recipient": 0},
                  "phone": 0, "skype": 0, "moreInfo": 0}
        if gender == 'Ms':
            person['gender'] = {'id': 1, 'text': "Ms"}
        payload = {"persons": [person], "departments": []}
        return self.create_contact(**payload)

    def create_contact_with_multiple_departments(self):
        random_contact_department1 = self.generate_random_string()
        random_contact_department2 = self.generate_random_string()
        random_contact_department3 = self.generate_random_string()
        dep1 = {
            "display": random_contact_department1,
            "value": random_contact_department1,
            "id": "new",
            "text": random_contact_department1
        }
        dep2 = {
            "display": random_contact_department2,
            "value": random_contact_department2,
            "id": "new",
            "text": random_contact_department2
        }
        dep3 = {
            "display": random_contact_department3,
            "value": random_contact_department3,
            "id": "new",
            "text": random_contact_department3
        }
        payload = {"departments": [dep1, dep2, dep3]}

        return self.create_contact(**payload)

    def set_configuration(self):
        self.info('set contact configuration')
        config_file = os.path.abspath('api_testing/config/contacts.json')
        with open(config_file, "r") as read_file:
            payload = json.load(read_file)
        super().set_configuration(payload=payload)
