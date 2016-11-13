# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done
from page_objects.user_menu import UserMenu


class Menu(PageObject):

    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self.user_menu = UserMenu(self.driver)

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_main_navbar")

    def _find_top_menu(self, top_menu_text):
        top_menu = None

        top_menu_items = self.root\
            .find_element_by_class_name("o_menu_sections")\
            .find_elements_by_xpath('*')
        for top_menu_item in top_menu_items:
            if top_menu_item.text == top_menu_text:
                top_menu = top_menu_item
                break

        if not top_menu:
            raise NoSuchElementException(msg='Top menu "%s" was not found' % top_menu_text)

        return top_menu

    @wait_rpc_done()
    def click_dropdown(self, top_menu_text, menu_text):
        top_menu = self._find_top_menu(top_menu_text)
        ActionChains(self.driver).move_to_element(top_menu).click(top_menu).perform()

        # now that submenus are displayed, we can interact with them
        menu = None
        menu_items = top_menu\
            .find_element_by_class_name("dropdown-menu")\
            .find_elements_by_xpath("*")
        for menu_item in menu_items:
            if menu_item.text == menu_text:
                menu = menu_item
                break

        if not menu:
            raise NoSuchElementException(msg='Menu "%s" was not found' % top_menu_text)

        menu.click()

    def click(self, top_menu_text):
        self._find_top_menu(top_menu_text).click()
