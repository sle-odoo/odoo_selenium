# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject, wait_rpc_done


class SideBar(PageObject):

    @property
    def root(self):
        try:
            return self.driver.find_element_by_class_name("o_cp_sidebar")
        except NoSuchElementException:
            return None

    def is_opened(self):
        return self.root is not None

    @wait_rpc_done()
    def click(self, action_name):
        self.root.click()
        self.root\
            .find_element_by_link_text(action_name)\
            .click()
