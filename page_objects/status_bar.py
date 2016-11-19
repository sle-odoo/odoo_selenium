# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject, wait_rpc_done


class StatusBar(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_form_statusbar")

    @wait_rpc_done()
    def click(self, button_text):
        buttons = self.root\
            .find_element_by_class_name("o_statusbar_buttons")\
            .find_elements_by_tag_name("button")
        # if all buttons are hidden, it means we're in mobile mode and have to
        # open the dropdown
        if all(not button.is_displayed() for button in buttons):
            self.root \
                .find_element_by_class_name("o_statusbar_buttons")\
                .find_element_by_class_name("dropdown-toggle")\
                .click()
        button = next((button for button in buttons if button.text == button_text), None)
        if not button:
            raise NoSuchElementException(msg='Button "%s" was not found.' % button_text)
        button.click()
