from api_testing.apis.base_api import BaseAPI
from api_testing.apis.base_api import api_factory


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
            "companyNo": self.generate_random_number(),
            "name": self.generate_random_string(),
            "isSupplier": "true",
            "country": "",
            "dynamicFieldsValues": []
            }

        api = '{}{}'.format(self.url, self.END_POINTS['contacts_api']['create_contact'])
        return api, {}


class ContactsAPI(ContactsAPIFactory):
    def get_first_record_with_data_in_attribute(self, attribute):
        contacts_request, _ = self.get_all_contacts()
        if (contacts_request['status'] != 1) or (contacts_request['count'] == 0):
            return False
        contacts_records = contacts_request['contacts']
        for contact in contacts_records:
            if contact[attribute] != '':
                return contact[attribute]

    def delete_active_contact(self, id=1):
        if self.archive_contacts(ids=[str(id)])[0]['message'] == 'delete_success':
            if self.delete_archived_contact(id=id)[0]['message']=='hard_delete_success':
                return True
            else:
                self.restore_contacts(ids=[str(id)])
                return False
        else:
            return False