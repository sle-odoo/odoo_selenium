# -*- coding: utf-8 -*-

from page_objects.common import PageObject
from page_objects.common import wait_rpc_done


class Breadcrumbs(PageObject):

    @wait_rpc_done()
    def go_to_previous(self):
        breadcrumb = self.driver.find_element_by_class_name("breadcrumb")
        breadcrumb_paths = breadcrumb.find_elements_by_tag_name("li")
        previous_index = None

        for index, breadcrumb_path in enumerate(breadcrumb_paths):
            class_name = breadcrumb_path.get_attribute("class")
            if class_name == "active":
                previous_index = index - 1
                break

        breadcrumb_paths[previous_index].click()

    def go_to_first(self):
        pass

    def get_current_step_value(self):
        breadcrumb = self.driver.find_element_by_class_name("breadcrumb")
        breadcrumb_paths = breadcrumb.find_elements_by_tag_name("li")
        return breadcrumb_paths[-1].text
