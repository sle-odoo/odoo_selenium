# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject


class Wizard(PageObject):

    def is_opened(self):
        return self.driver.find_element_by_class_name("modal") is not None

    def click_on_footer_buttons(self, button_text):
        buttons = self.driver\
            .find_element_by_xpath(
                "//html//body[contains(@class, 'o_web_client')]" +
                "/div[contains(@class, 'modal') and contains(@class, 'in')]" +
                "/div[contains(@class, 'modal-dialog')" +
                "]/div/div[@class='modal-footer']")\
            .find_elements_by_tag_name("button")

        for index, button in enumerate(buttons):
            if button.text == button_text:
                button_to_click_index = index
                break
        try:
            buttons[button_to_click_index].click()
        except (IndexError, ValueError):
            raise NoSuchElementException(msg='Button "%s" was not found' % button_text)

        # FIXME: cannot use `page_objects.common.wait_rpc_done` because clicking on a
        # footer button does not trigger the display of the "loading" widget. We'll
        # wait for the disappearance of the button instead, but when we click on a
        # footer button that does not close the wizard (print wizard) this should be
        # adapted
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.staleness_of(buttons[button_to_click_index]))
