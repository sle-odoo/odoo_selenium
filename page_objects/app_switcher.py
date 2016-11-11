# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class AppSwitcher(PageObject):

    def is_opened(self):
        try:
            self.driver.find_element_by_class_name("o_application_switcher")
        except NoSuchElementException:
            return False
        else:
            return True

    @wait_rpc_done()
    def click_on_menu(self, menu_text):
        self.driver.find_element_by_link_text(menu_text).click()

    def open(self):
        if self.is_opened():
            return
        self.driver.find_element_by_class_name("o_menu_toggle").click()
