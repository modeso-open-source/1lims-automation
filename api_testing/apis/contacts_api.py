from api_testing.apis.base_api import BaseAPI


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

