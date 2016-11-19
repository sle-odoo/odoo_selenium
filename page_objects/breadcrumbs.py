# -*- coding: utf-8 -*-

from page_objects.common import PageObject, wait_rpc_done


class Breadcrumbs(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("breadcrumb")

    def get_active_path(self):
        breadcrumb_paths = self.root.find_elements_by_tag_name("li")
        return next(path for path in breadcrumb_paths if path.get_attribute("class") == "active")

    @wait_rpc_done()
    def previous_path_click(self):
        breadcrumb_paths = self.root.find_elements_by_tag_name("li")
        active_path = self.get_active_path()
        active_path_index = breadcrumb_paths.index(active_path)
        breadcrumb_paths[active_path_index - 1].click()

    def get_current_path(self):
        return self.get_active_path().text
