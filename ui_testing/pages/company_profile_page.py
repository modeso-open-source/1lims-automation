from ui_testing.pages.base_pages import BasePages


class CompanyProfile(BasePages):
    def __init__(self):
        super().__init__()
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.company_profile_url = "{}settings#companyProfile".format(
            self.base_selenium.url)

    def get_company_profile_page(self):
        self.base_selenium.get(url=self.company_profile_url)
        self.wait_until_page_is_loaded()

    def get_field_value(self, field_name, field_type='text'):
        field_value = self.base_selenium.get_value(
            element='company_profile:{}_field'.format(field_name))
        if field_type == 'drop_down':
            field_value = self.base_selenium.get_text(
                element='company_profile:{}_field'.format(field_name)).split('\n')[0]
        return field_value

    
    def set_field_value(self, field_name, field_type='text', item_text='', empty=False):
        if item_text == '' and field_type == 'text' and empty == False:
            item_text = self.generate_random_text()

        if field_type == 'drop_down':
            self.base_selenium.select_item_from_drop_down(
                element='company_profile:{}_field'.format(field_name), item_text=item_text)
        else:
            self.base_selenium.set_text(
                element='company_profile:{}_field'.format(field_name), value=item_text)

    def update_company_profile(self):
        self.base_selenium.LOGGER.info(' + Update the company profile.')

        # the values to be added
        company_profile= {
            'name': self.generate_random_text(),
            'street_name': self.generate_random_text(),
            'street_number': self.generate_random_number(),
            'postal_code': self.generate_random_number(),
            'location': self.generate_random_text(),
            'country': None,
        }

        # set the fields values
        self.set_field_value(field_name='name', item_text=company_profile['name'])
        self.set_field_value(field_name='street_name', item_text=company_profile['street_name'])
        self.set_field_value(field_name='street_number', item_text=company_profile['street_number'])
        self.set_field_value(field_name='postal_code', item_text=company_profile['postal_code'])
        self.set_field_value(field_name='location', item_text=company_profile['location'])
        self.set_field_value(field_name='country', field_type='drop_down')

        # get the values from the form to get the form format for (drop down / number) fields 
        company_profile['country'] = self.get_field_value(field_name='country', field_type='drop_down')
        company_profile['street_number'] = self.get_field_value(field_name='street_number', field_type='text')
        company_profile['postal_code'] = self.get_field_value(field_name='postal_code', field_type='text')

        # save
        self.save(True)
        self.base_selenium.LOGGER.info(' + Company name : {}'.format(company_profile['name']))

        return company_profile
