# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject, wait_rpc_done


class KanbanView(PageObject):

    @property
    def root(self):
        kanban_views = self.driver.find_elements_by_class_name("o_kanban_view")
        return next((kanban_view for kanban_view in kanban_views if kanban_view.is_displayed()), None)

    def is_opened(self):
        return self.root is not None

    @wait_rpc_done()
    def create(self):
        self.driver.find_element_by_class_name("o-kanban-button-new").click()

    def get_vignettes(self):
        vignettes = self.root.find_elements_by_class_name("o_kanban_record")
        # a kanban view always contain invisible vignettes so that if there
        # aren't enough vignettes on the last line, they do not grow (flex
        # display)
        return [vignette for vignette in vignettes if vignette.is_displayed()]

    def get_vignette(self, vignette_index):
        vignettes = self.get_vignettes()
        if len(vignettes) < vignette_index - 1:
            raise NoSuchElementException(msg='Vignette with index %s was not found '
                                             '(not enough vignettes in the displayed kanban view).' % vignette_index)
        return vignettes[vignette_index - 1]

    @wait_rpc_done()
    def vignette_click(self, vignette_index):
        self.get_vignette(vignette_index).click()

    @wait_rpc_done()
    def button_in_vignette_click(self, vignette_index):
        self.get_vignette(vignette_index)\
            .find_element_by_tag_name("button")\
            .click()

    def vignette_contains(self, vignette_index, expected_text):
        return expected_text in self.get_vignette(vignette_index).text

    def wait_until_vignette_is_visible_and_contains(self, vignette_index, expected_text):
        wait = WebDriverWait(self.driver, 30)

        def _wait_until_vignette_is_visible_and_contains(driver):
            if len(self.get_vignettes()) >= vignette_index:
                return self.vignette_contains(vignette_index, expected_text)
            return False

        wait.until(_wait_until_vignette_is_visible_and_contains)
