# -*- coding: utf-8 -*-

from page_objects.common import PageObject
import page_objects


class ControlPanel(PageObject):

    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)

        self.search_view = page_objects.SearchView.SearchView(self.driver)
        self.sidebar = page_objects.SideBar.SideBar(self.driver)
        self.breadcrumbs = page_objects.Breadcrumbs.Breadcrumbs(self.driver)
        self.pager = page_objects.Pager.Pager(self.driver)
        self.view_switcher = page_objects.ViewSwitcher.ViewSwitcher(self.driver)
