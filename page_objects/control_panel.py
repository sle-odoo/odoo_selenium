# -*- coding: utf-8 -*-

from page_objects.common import PageObject
import page_objects


class ControlPanel(PageObject):

    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)

        self.search_view = page_objects.search_view.SearchView(self.driver)
        self.sidebar = page_objects.side_bar.SideBar(self.driver)
        self.breadcrumbs = page_objects.breadcrumbs.Breadcrumbs(self.driver)
        self.pager = page_objects.pager.Pager(self.driver)
        self.view_switcher = page_objects.view_switcher.ViewSwitcher(self.driver)
