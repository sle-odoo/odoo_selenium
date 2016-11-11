# -*- coding: utf-8 -*-

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class Menu(PageObject):

    def mouse_on_top_menu(self, menu_text):
        self.driver.find_element_by_link_text(menu_text).move_to_element()

    def click_on_top_menu(self, menu_text):
        self.driver.find_element_by_link_text(menu_text).click()

    @wait_rpc_done()
    def click_on_menu(self, menu_text):
        self.driver.find_element_by_link_text(menu_text).click()
