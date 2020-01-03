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
                self.restore_contacts(ids=[id])
                return False
        else:
            return False
