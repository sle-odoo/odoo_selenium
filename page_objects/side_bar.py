# -*- coding: utf-8 -*-

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class SideBar(PageObject):

    @wait_rpc_done()
    def click_on_action(self, action_name):
        # open the drop-down
        self.driver.find_element_by_class_name("o_cp_sidebar").click()

        # click on the action
        self.driver\
            .find_element_by_class_name("o_cp_sidebar")\
            .find_element_by_link_text(action_name)\
            .click()
