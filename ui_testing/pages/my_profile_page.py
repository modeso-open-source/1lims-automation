from ui_testing.pages.base_pages import BasePages
from random import randint


class MyProfile(BasePages):
    def __init__(self):
        super().__init__()
        # self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.my_profile_url = "{}settings#myProfile".format(self.base_selenium.url)
        
    def get_my_profile_page(self):
        self.base_selenium.LOGGER.info('Get my profile page.')
        self.base_selenium.get(url=self.my_profile_url)
        self.wait_until_page_is_loaded()

    def change_password(self, current_password, new_password, save=False):
        self.base_selenium.LOGGER.info('Change the password')
        
        # change the password value
        self.base_selenium.set_text(
            'my_profile:current_password_field', current_password)
        self.base_selenium.set_text(
            'my_profile:new_password_field', new_password)
        self.base_selenium.set_text(
            'my_profile:confirm_password_field', new_password)

        if save:
            self.save(True)
            self.base_selenium.LOGGER.info('New password saved')
        else:
            self.cancel(force=True)
            self.base_selenium.LOGGER.info('New password Canceled')

    def chang_lang(self, lang):
        self.base_selenium.LOGGER.info('Change language to {}'.format(lang))
        self.base_selenium.select_item_from_drop_down(element='my_profile:language_field', item_text=lang)
        self.wait_until_page_is_loaded()

    def upload_logo(self, file_name, drop_zone_element, save=True, remove_current_file=False):
        super().upload_file(file_name, drop_zone_element, remove_current_file)
        if save:
            self.save(save_btn="my_profile:save_button")
            self.base_selenium.wait_until_element_is_not_displayed("general:alert_confirmation")
            self.base_selenium.driver.execute_script("document.querySelector('.dz-details').style.opacity = 'initial';")
            uploaded_file_name = self.base_selenium.find_element(element='general:uploaded_file_name').text
            return uploaded_file_name
        else:
            self.cancel(True)
