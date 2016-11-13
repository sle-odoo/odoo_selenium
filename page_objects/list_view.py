# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class ListView(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_list_view")

    def is_opened(self):
        return self.driver.find_element_by_class_name("o_list_view") is not None

    @wait_rpc_done()
    def create(self):
        self.driver.find_element_by_class_name("o_list_buttons")\
            .find_element_by_class_name("o_list_button_add")\
            .click()

    def select_rows(self, *args):
        pass

    def select_all_rows(self):
        self.root\
            .find_element_by_class_name("o_list_record_selector")\
            .find_element_by_tag_name("input")\
            .click()

    @wait_rpc_done()
    def click_on_row(self, row_index):
        rows = self.root\
            .find_element_by_tag_name("tbody")\
            .find_elements_by_tag_name("tr")
        rows[row_index -1].click()


    @wait_rpc_done()
    def click_on_row_and_type(self, row_index, text):
        rows = self.root \
            .find_element_by_tag_name("tbody") \
            .find_elements_by_tag_name("tr")
        row = rows[row_index - 1]

        row.click()
        cell = self.driver.switch_to_active_element()
        cell.send_keys(text)
        cell.send_keys(Keys.ENTER)