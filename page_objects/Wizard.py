# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class Wizard(PageObject):

    def is_opened(self):
        return self.driver.find_element_by_class_name("modal") is not None

    @wait_rpc_done()
    def click_on_footer_buttons(self, button_text):
        button_to_click_index = None
        buttons = self.driver\
            .find_element_by_class_name("modal")\
            .find_element_by_class_name("modal-footer")\
            .find_elements_by_tag_name("button")

        for index, button in enumerate(buttons):
            if button.text == button_text:
                button_to_click_index = index
                break
        try:
            buttons[button_to_click_index].click()
        except (IndexError, ValueError):
            raise NoSuchElementException(msg='Button "%s" was not found' % button_text)
