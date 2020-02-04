from api_testing.apis.base_api import BaseAPI
import json


class ContactsAPI(BaseAPI):
    def get_all_contacts(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['contacts_api']['list_all_contacts'])
        _payload = {"sort_value": "companyNo",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def get_first_record_with_data_in_attribute(self, attribute):
        contacts_request = self.get_all_contacts().json()
        if (contacts_request['status'] != 1) or (contacts_request['count'] == 0):
            return False
        contacts_records = contacts_request['contacts']
        for contact in contacts_records:
            if contact[attribute] != '':
                return contact[attribute]
    
    def get_table_fields(self, component_id):
        api = '{}{}{}/'.format(self.url, self.END_POINTS['contacts_api']['get_table_fields'], component_id)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        parsed_response = response.json()
        if parsed_response['status'] == 1:
            return parsed_response['fields']
        else:
            return []

    def get_contact_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['form_data'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['contact']
        else:
            return False
    
    def archive_contacts(self, ids=['1']):
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['archive_contacts'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_contacts(self, ids=['1']):
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['restore_contacts'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='restore_success':
            return True
        else:
            return False
    
    def delete_archived_contact(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['contacts_api']['delete_contact'], str(id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_contact(self, id=1):
        if self.archive_contacts(ids=[str(id)]):
            if self.delete_archived_contact(id=id):
                return True
            else:
                self.restore_contacts(ids=[str(id)])
                return False
        else:
            return False

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
        _payload = {
            'departments' : [],
            'departmentArray' : [],
            'persons' : [],
            'country' : '',
            'dynamicFieldsValues' : []
        }

        
        payload = self.update_payload(_payload, **kwargs)
        api = '{}{}'.format(self.url, self.END_POINTS['contacts_api']['create_contact']) 
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=payload, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        
        if data['status'] == 1:
            return payload
        else:
            return data['message']

            
