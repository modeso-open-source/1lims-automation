from ui_testing.pages.base_pages import BasePages

class Contacts(BasePages):
    def __init__(self):
        super().__init__()
        self.contacts_url = "{}contacts".format(self.base_selenium.url)


    def get_contacts_page(self):
        self.base_selenium.get(url=self.contacts_url)
        self.sleep_small()

    def get_random_contact(self):
        row = self.get_random_table_row(table_element='contacts:contacts_table')
        self.open_edit_page(row=row)