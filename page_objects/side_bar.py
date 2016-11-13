# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject


class SideBar(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_cp_sidebar")

    def click_on_action(self, action_name):
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.visibility_of(self.root))

        self.root.click()
        self.driver\
            .find_element_by_class_name("o_cp_sidebar")\
            .find_element_by_link_text(action_name)\
            .click()
