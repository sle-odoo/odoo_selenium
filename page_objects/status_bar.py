# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from page_objects.common import PageObject


class StatusBar(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_form_statusbar")

    def click(self, button_text):
        found = False
        buttons = self.root.find_elements_by_tag_name("button")
        for index, button in enumerate(buttons):
            if button.text == button_text:
                button.click()
                found = True

        if not found:
            raise NoSuchElementException(msg='Button "%s" was not found' % button_text)
        else:
            # FIXME
            self.driver.implicitly_wait(5)
