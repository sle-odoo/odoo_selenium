# -*- coding: utf-8 -*-

from page_objects.common import PageObject, wait_rpc_done


class ViewSwitcher(PageObject):

    @wait_rpc_done()
    def to_list(self):
        self.driver.find_element_by_class_name("o_cp_switch_list").click()
