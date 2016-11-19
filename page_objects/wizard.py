# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject, wait_rpc_done


class Wizard(PageObject):

    @property
    def root(self):
        # we have to be somewhat strict here because there may be modals in the
        # dom that aren't wizard
        modals = self.driver.find_elements_by_xpath(
            "//html//body[contains(@class, 'o_web_client')]"
            "/div[contains(@class, 'modal') and contains(@class, 'in') and not(contains(@class, 'backdrop'))]")
        return next((modal for modal in modals if modal.is_displayed()), None)

    def is_opened(self):
        return self.root is not None

    @wait_rpc_done()
    def click_on_footer_buttons(self, button_text):
        buttons = self.root\
            .find_element_by_xpath(
                "./div[contains(@class, 'modal-dialog')]"
                "/div/div[@class='modal-footer']")\
            .find_elements_by_tag_name("button")
        button = next((button for button in buttons if button.text == button_text), None)
        if not button:
            raise NoSuchElementException(msg='Button "%s" was not found.' % button_text)
        button.click()

    def wait_is_closed(self):
        wait = WebDriverWait(self.driver, 10)

        def _wait_until_wizard_is_closed(driver):
            return self.root is None

        wait.until(_wait_until_wizard_is_closed)
