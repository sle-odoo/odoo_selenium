# -*- coding: utf-8 -*-

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class KanbanView(PageObject):

    def is_opened(self):
        return self.driver.find_element_by_class_name("o_kanban_view") is not None

    @wait_rpc_done()
    def click_on_vignette(self, vignette_number):
        vignettes = self.driver.find_elements_by_class_name("o_kanban_record")
        vignettes[vignette_number].click()

    @wait_rpc_done()
    def click_on_button_in_vignette(self, vignette_number):
        vignettes = self.driver.find_elements_by_class_name("o_kanban_record")
        vignette = vignettes[vignette_number - 1]
        vignette.find_element_by_tag_name("button").click()

    @wait_rpc_done()
    def create(self):
        self.driver.find_element_by_class_name("o-kanban-button-new").click()
