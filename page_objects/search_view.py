# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys

from page_objects.common import PageObject, wait_rpc_done


class SearchView(PageObject):

    @wait_rpc_done()
    def type_and_enter(self, text):
        si = self.driver.find_element_by_class_name("o_searchview_input")
        si.send_keys(text)
        si.send_keys(Keys.ENTER)
