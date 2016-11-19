# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject, wait_rpc_done


class AppSwitcher(PageObject):

    @property
    def root(self):
        try:
            return self.driver.find_element_by_class_name("o_application_switcher")
        except NoSuchElementException:
            return None

    def is_opened(self):
        return self.root is not None

    @wait_rpc_done()
    def click_on_menu(self, menu_text):
        self.root.find_element_by_link_text(menu_text).click()

    @wait_rpc_done()
    def open(self):
        if not self.is_opened():
            self.driver.find_element_by_class_name("o_menu_toggle").click()
