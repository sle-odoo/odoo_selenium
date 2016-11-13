# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class UserMenu(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_user_menu")

    @wait_rpc_done()
    def click(self, text):
        self.root.find_element_by_tag_name("a").click()
        user_menu_entries = self.root\
            .find_element_by_class_name("dropdown-menu")\
            .find_elements_by_xpath("*")
        for user_menu_entry in user_menu_entries:
            if user_menu_entry.text == text:
                user_menu_entry.click()
                return

        raise NoSuchElementException(msg='Usermenu entry "%s" was not found' % text)
