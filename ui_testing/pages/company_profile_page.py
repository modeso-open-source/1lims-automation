from ui_testing.pages.base_pages import BasePages

class CompanyProfile(BasePages):
    def __init__(self):
        super().__init__()
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.company_profile_url = "{}settings#companyProfile".format(self.base_selenium.url)

    def get_company_profile_page(self):
        self.base_selenium.get(url=self.company_profile_url)
        self.sleep_small()

    def get_field_value(self, field_name, field_type='text'):
        field_value = self.base_selenium.get_text(
            element='company_profile:{}_field'.format(field_name))
        if field_type == 'drop_down':
            field_value = field_value.split('\n')[0]
        return field_value

    def set_field_value(self, field_name, field_type='text', item_text=''):
        if field_type == 'drop_down':
            self.base_selenium.select_item_from_drop_down(
                element='company_profile:{}_field'.format(field_name), item_text=item_text)
        else:
            self.base_selenium.set_text(
                element='company_profile:{}_field'.format(field_name), value=self.generate_random_text())

    def click_on_cancel(self):
        # click on cancel
        self.base_selenium.click(element='company_profile:cancel_button')
        # confirm the pop up message
        self.confirm_popup()
        # wait till the browser redirect
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        # go back to the company profile
        self.get_company_profile_page()